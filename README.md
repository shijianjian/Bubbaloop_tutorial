## Configuration

You may test if you can access the RTSP stream by: ```vlc rtsp://YOUR_RTSP_LINK```. Here are several methods to obtain RTSP steams.

### Via your iPhone

For iPhone, download `IP Camera Lite`. Then, turn on IP Camera server in the bottom.

To obtain username and password, you may click 1) top-right dropdown, 2) settings.

### Via public sources

If your machine and phone are not in the same network, you can use public RTSP streams instead.

You may use a public stream via [rtsp.stream](https://www.rtsp.stream/admin/teststream).


### Input RTSP Streams to the rust config file

```
python generate_camera_config.py --output_path ./bubbaloop/src/cu29/pipelines/cameras_1.ron --rtsp_streams rtsp://XXXX rtsp://YYYY
```

## Start
```
sudo docker build -t bubbaloop_base .
```

```
sudo docker run --rm -it -p 3000:3000 bubbaloop_base
```

check the docker container ID XXXX with `sudo docker ps`. 


Open another terminal then

```
sudo docker exec -it XXXX /bin/bash
```

```
just start-pipeline cameras 0.0.0.0 3000
```

## Visualization

```
cd bubbaloop
```

```
python examples/python-streaming/client.py --host 0.0.0.0 --port 3000 --cameras 0 1
```
