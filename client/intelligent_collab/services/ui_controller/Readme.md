# Effects Controller UI


The *Effects Controller UI* is a [ReactJS](https://reactjs.org/) web application that provides the User Interface for the Intelligent Collaboration application

## Install Dependencies

```
npm install
```


## Start the Effects Controller UI

```
npm start
```


## Running with `docker` for `development`

- Build the container
```
docker build -f Dockerfile.dev -t sysstacks/icollab-efx-control:dev .
```

- Run it
```
docker run --rm \
       -p 3000:3000 \
       --name icollab-efx-control sysstacks/icollab-efx-control:dev
```

- Adding local source code  into the container
```
docker run --rm -it \
       -v $(pwd):/app \
       -e CHOKIDAR_USEPOLLING=true \
       -p 3000:3000 \
       --name icollab-efx-control sysstacks/icollab-efx-control:dev
```

## Build and run the `production` container

The following steps are for running a production-like ReactJS web application.
This should be the one we'd be using for releases.

- Build the container

```
docker build -t sysstacks/icollab-efx-control .
```

- Run it

```
docker run -it --rm \
       -p 8080:80 \
       --name icollab-efx-control sysstacks/icollab-efx-control
```