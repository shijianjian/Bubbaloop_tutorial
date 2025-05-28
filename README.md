```
git submodule update --init --recursive
```

```
python generate_camera_config.py  --rtsp_streams rtsp://rtspstream:4j_U0tJ6fGtiaKREnuVnH@zephyr.rtsp.stream/movie  --output_path ./bubbaloop/src/cu29/pipelines/cameras_1.ron
```

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