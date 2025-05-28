import gi
import sys
import os
from gi.repository import Gst, GstRtspServer, GObject, GLib

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

Gst.init(None)

class VideoRTSPMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, video_path, loop=True):
        super(VideoRTSPMediaFactory, self).__init__()
        self.video_path = video_path
        self.loop = loop

    def do_create_element(self, url):
        print(f"[INFO] Starting stream for: {self.video_path}")
        launch_string = (
            f"multifilesrc location={self.video_path} loop={str(self.loop).lower()} ! "
            f"decodebin ! videoconvert ! "
            f"x264enc tune=zerolatency bitrate=512 speed-preset=superfast ! "
            f"rtph264pay config-interval=1 name=pay0 pt=96"
        )
        print(f"[DEBUG] Using pipeline: {launch_string}")
        return Gst.parse_launch(launch_string)

    def on_about_to_finish(self, element):
        print("[DEBUG] Video finished, restarting...")
        element.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

def start_rtsp_server(video_list, base_port=8554, loop=True):
    server = GstRtspServer.RTSPServer()
    server.set_service(str(base_port))

    # Configure server
    server.set_backlog(10)
    server.set_address("0.0.0.0")  # Listen on all interfaces

    # Create mount points
    mounts = server.get_mount_points()
    rtsp_links = []

    print(f"[DEBUG] Starting RTSP server on port {base_port}")
    print(f"[DEBUG] Server address set to 0.0.0.0")

    for idx, video_path in enumerate(video_list):
        if not os.path.exists(video_path):
            print(f"[WARNING] Skipping non-existent file: {video_path}")
            continue

        mount_point = f"/video{idx}"
        print(f"[DEBUG] Creating mount point: {mount_point} for {video_path}")
        
        factory = VideoRTSPMediaFactory(video_path, loop=loop)
        factory.set_shared(True)
        mounts.add_factory(mount_point, factory)
        print(f"[DEBUG] Added mount point {mount_point}")

        # Use container IP for the URL since we're in Docker
        container_ip = os.getenv('CONTAINER_IP', 'localhost')
        url = f"rtsp://{container_ip}:{base_port}{mount_point}"
        rtsp_links.append((video_path, url))

    # Attach the server
    if not server.attach(None):
        print("[ERROR] Failed to attach server")
        return []
    
    print("[DEBUG] Server successfully attached")
    return rtsp_links

if __name__ == "__main__":
    # sudo apt install python3-gi gir1.2-gst-rtsp-server-1.0
    # pip install PyGObject==3.50.0
    if len(sys.argv) < 2:
        print("Usage: python multi_rtsp_server.py <video1> <video2> ...")
        sys.exit(1)

    video_files = sys.argv[1:]
    print(f"[DEBUG] Processing {len(video_files)} video files")
    for video in video_files:
        print(f"[DEBUG] Video file: {video} (exists: {os.path.exists(video)})")
    
    streams = start_rtsp_server(video_files)

    if not streams:
        print("[ERROR] No streams were created")
        sys.exit(1)

    print("\n[✅ RTSP Streams Ready]")
    print("[INFO] Server listening on 0.0.0.0:8554")
    for video_path, link in streams:
        print(f"{os.path.basename(video_path)} → {link}")

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")
