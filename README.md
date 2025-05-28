```
sudo docker build -t bubbaloop_base .
```

```
sudo docker run --rm -it -p 3000:3000 bubbaloop_base
```

check the docker container ID XXXX.


Open another terminal then

```
sudo docker exec -it XXXX /bin/bash
```