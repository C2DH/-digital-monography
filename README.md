# Digital-monography
Platform for scholars of digital humanities to publish their digital work

# Repository status 

| Alert |
| ----------- | 
| Please be informed that the repository was moved to GitLab. Contact maintainers for further information. |

# Building and running the Docker image

## Building

In order to use the tools, you have to set up all of the services that handle each step of the workflow. The following command will **build** and **start** all of those services.

```sh
docker compose up -d
```

## Workflow

The workflow performs operations on source files uploaded by a user. The source can be
* a) a path to a local directory on a disk or
* b) a url to a zip archive of a github repository.

As an example, the commands listed below take as exemplary input (a) the usage documentation of this system and (b) the book "For a new hermeneutics of practice in digital public history" hosted on GitHub. Note however, that in the second case (b) only the first command takes the url as an argument and the rest take the name of the "data/input" directory where the package was unzipped.

### Transform .docx to .md

```sh
docker compose exec main python src/docx2md.py "docs/usage"
```

You can also point to a github zip archive.

```sh
docker compose exec main python src/docx2md.py "https://api.github.com/repos/kaminski-pawel/for-a-new-hermeneutics-of-practice-in-digital-public-history/zipball/v0.1.0"
```

### Run markdown verification

For now, the project is using [markdownlint](https://github.com/DavidAnson/markdownlint) via the [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli). Note that this linter only supports _Markdown/CommonMark files_. It won't be able to verify the _MyST_ specification.

```sh
docker compose run mdlint "/home/app_user/data/md/usage/*.md"
```

`markdownlint-cli` supports advanced globbing patterns like `**/*.md` ([more information](https://github.com/isaacs/node-glob/blob/main/README.md#glob-primer)).

```sh
docker compose run mdlint "/home/app_user/data/md/usage/**/*.md"
```

You might also want to redirect stdout and stderr to a log file.

```sh
docker compose run mdlint "/home/app_user/data/md/usage/*.md" >> "logs/md_linting.log" 2>&1
```

### Transform .md to .ipynb

```sh
docker compose exec main python src/md2ipynb.py "docs/usage"
```

or in case of github repository:

```sh
docker compose exec main python src/md2ipynb.py "data/kaminski-pawel-for-a-new-hermeneutics-of-practice-in-digital-public-history-8cffccd"
```

### Transform .ipynb to .html (experimental, might break)

```sh
docker compose exec main python src/_ipynb2html.py "docs/usage"
```

### Transform ... to JATS .xml

[myst-to-jats](https://github.com/executablebooks/mystmd/tree/main/packages/myst-to-jats) can convert a MyST AST to JATS XML.

### Transform .html to .pdf (experimental, might break)

```sh
docker compose exec main python src/_html2pdf.py "docs/usage"
```

## Running tests

```sh
docker compose exec main pytest tests
```

## Running modes

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

To stop running containers and remove them, use

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

# Reading .ipynb files

## Set up

Please remember that in order to benefit from additional MyST features you should read .ipynb files using the [Jupyter Lab](https://jupyterlab.readthedocs.io/en/latest/) and the [`jupyterlab_myst` extension](https://github.com/executablebooks/jupyterlab-myst).

Detailed installation instructions can be found in the [official MyST guide](https://mystmd.org/guide/quickstart-jupyter-lab-myst). In short, it should be sufficient to install Jupyter Lab and the `jupyterlab_myst` extension.

```sh
pip install jupyterlab
pip install jupyterlab_myst
```

## Opening a file

In order to open .ipynb files, run the Jupyter Lab (and not the Jupyter Notebook) using the `jupyter lab` command in the directory in which the .ipynb files are located.

```sh
jupyter lab
```

## Usefull extensions

* pandoc, for example for 'Saving and Exporting Notebook As PDF'
* TeX Live, for example for 'Saving and Exporting Notebook As PDF'
