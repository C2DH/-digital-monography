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

# Static analysis

## Linting

You can run the linter and the type checker while running the container. As of now, linting is executed only manually.

```sh
mypy /src
flake8 /src
```

## Formatting

For now, formatting of the code (incl. import sorting) is meant to be done in your IDE environment.

For example, you can set up the VS Code editor to format the code. VS Code settings that should be uniform for all contributors are set up in the `.vscode/settings.json` file. Some settings can be configured per User in the VS Code settings console - for example you can set the "Format On Save" to true to automatize the formatting process.

Extensions to install on the VS Code marketplace:
* [Black Formatter by Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
* [isort by Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
