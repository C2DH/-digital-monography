# Digital-monography
Platform for scholars of digital humanities to publish their digital work

# Building and running the Docker image

## Building

To build the image run the following (note that the aim of the `--rm` argument is to remove intermediate containers after the build is done):

```
docker build -t digital-monography-img --rm .
```

## Running

### Running in the TTY mode

```
docker run -it --name digital-monography-cntr --rm digital-monography-img
```

Now you are in a pseudo-tty mode and you can interact with the python script.

To exit the tty mode, type `exit`.

To return to your terminal without terminating the running container, use `ctrl+p` and `ctrl+q` in sequence. Then to go back to the **digital-monography-cntr** container tty, type `docker attach digital-monography-cntr`.

### Running in the detached mode

#TODO
