import datetime
import logging
import subprocess

from constants import LOGS_DIR


def config_logging() -> None:
    today = datetime.date.today().isoformat()
    logging.basicConfig(
        filename=f"{LOGS_DIR}/{today}.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s::%(name)s::%(levelname)s::%(message)s",
    )


def exec_subps_and_log(args: list[str], logger: logging.Logger) -> None:
    """
    Execute a child program in a new process with specifying stdout and stderr.
    See docs:
    https://docs.python.org/3.11/library/subprocess.html#subprocess.Popen
    """
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    with process.stdout:
        for line in iter(process.stdout.readline, b""):
            logger.info(line)
