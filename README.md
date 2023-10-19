# Digital-monography
Platform for scholars of digital humanities to publish their digital work

# Building and running the Docker image

## Building

To build the image run the following (note that the aim of the `--rm` argument is to remove intermediate containers after the build is done):

```sh
docker compose build
```

## Running

### Running in the TTY mode

```sh
docker compose run --rm main
```

Now you are in a TTY mode and you can interact with the python script.

To exit this mode, type `exit`.

To return to your terminal without terminating the running container, use `ctrl+p` and `ctrl+q` in sequence.

To go back to the container (or rather to attach your terminal to container stdin, stdout and stderr), find out the name of the container with `docker container ls` and attach your terminal with `docker attach <name-of-that-container>`.

### Running in the detached mode

#TODO

## Cleaning

To stop the running container and remove it, use

```sh
docker compose down
```
