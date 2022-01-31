# Front-end

> :bulb: Dev instructions, `npm run build` skipped to shorten container building time. 

## Usage
You can either build the image and run it or directly download an image.
### Build and run
```sh
docker build -t tools_discoverer_fe_dev .
docker run -dp 8080:8080 tools_discoverer_fe_dev
```
The app is available at [http://localhost:8080/](http://localhost:8080/)

### Download a pre-built image
There is a ready to use image in  [DockerHub](https://hub.docker.com/repository/docker/emartps/tools_discoverer_fe_dev)
```sh
docker pull emartps/tools_discoverer_fe_dev
```

