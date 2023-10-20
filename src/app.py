import datetime
import json
import logging
import sys

today = datetime.date.today().isoformat()
# TODO: add timezone aware timestamps and log filenames
logging.basicConfig(
    filename=f"/home/app_user/logs/{today}.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s::%(name)s::%(levelname)s::%(message)s",
)

data = [{idx: v} for idx, v in enumerate(sys.argv[1:])]

with open(
    f"/home/app_user/data/data_{datetime.datetime.today().isoformat()}.json", "w"
) as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

logging.warning("Done")
