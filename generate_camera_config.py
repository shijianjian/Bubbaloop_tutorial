#!/usr/bin/env python3

import argparse


def generate_camera_config(rtsp_streams):
    tasks = []
    connections = []
    num_cameras = len(rtsp_streams)

    # Add camera tasks
    for i, rtsp_url in enumerate(rtsp_streams):
        camera_config = {
            "source_type": "rtsp",
            "source_uri": rtsp_url,
            "channel_id": i,
        }

        tasks.append(f'''        (
            id: "cam{i}",
            type: "crate::cu29::tasks::VideoCapture",
            config: {{
                "source_type": "{camera_config["source_type"]}",
                // URL of the RTSP camera
                // rtsp://<username>:<password>@<ip>:<port>/<stream>
                "source_uri": "{camera_config["source_uri"]}",
                "channel_id": {camera_config["channel_id"]},
            }}
        ),''')

        # Add encoder task
        tasks.append(f"""        (
            id: "enc{i}",
            type: "crate::cu29::tasks::ImageEncoder",
        ),""")

        if i == 0:
            # Add broadcast task
            tasks.append("""        (
            id: "broadcast",
            type: "crate::cu29::tasks::ImageBroadcast",
        ),""")

        # Add connections
        connections.extend(
            [
                f'        (src: "cam{i}", dst: "enc{i}", msg: "crate::cu29::msgs::ImageRgb8GstMsg"),',
                f'        (src: "enc{i}", dst: "broadcast", msg: "crate::cu29::msgs::EncodedImage"),',
            ]
        )

    # Add recorder task at the end
    # tasks.append(_get_recorder_config(num_cameras))

    # Generate the complete RON configuration
    config = f"""(
    tasks: [
{chr(10).join(tasks)}
    ],
    cnx: [
{chr(10).join(connections)}
    ],
    logging: (
        slab_size_mib: 1024, // Preallocates 1GiB of memory map file at a time
        section_size_mib: 100, // Preallocates 100MiB of memory map per section for the main logger.
        enable_task_logging: false,
    ),
)
"""
    return config


def _get_recorder_config(num_cameras):
    if num_cameras == 1:
        return """        (
            id: "recorder",
            type: "crate::cu29::tasks::RecorderOne",
            config: {
                "path": "/tmp/",
            }
        ),"""
    elif num_cameras == 2:
        return """        (
            id: "recorder",
            type: "crate::cu29::tasks::RecorderTwo",
            config: {
                "path": "/tmp/",
            }
        ),"""
    elif num_cameras == 3:
        return """        (
            id: "recorder",
            type: "crate::cu29::tasks::RecorderThree",
            config: {
                "path": "/tmp/",
            }
        ),"""
    elif num_cameras == 4:
        return """        (
            id: "recorder",
            type: "crate::cu29::tasks::RecorderFour",
            config: {
                "path": "/tmp/",
            }
        ),"""
    else:
        raise ValueError(f"Unsupported number of cameras: {num_cameras}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate camera configuration .ron file from RTSP streams"
    )
    parser.add_argument(
        "--rtsp_streams",
        nargs="+",
        required=True,
        help="List of RTSP stream URLs (e.g., rtsp://user:pass@ip:port/stream)",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Path to save the generated .ron file",
    )
    args = parser.parse_args()

    # Generate configuration based on provided RTSP streams
    config = generate_camera_config(args.rtsp_streams)
    # filename = f"cameras_{len(args.rtsp_streams)}.ron"
    filename = args.output_path if args.output_path else "cameras_1.ron"

    with open(filename, "w") as f:
        f.write(config)
    print(f"Generated {filename} with {len(args.rtsp_streams)} camera(s)")


if __name__ == "__main__":
    main()
