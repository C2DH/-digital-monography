import datetime
import json
import os
import subprocess
import sys

print ("This is the name of the script: ", sys.argv[0])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))

data = [{idx: v} for idx, v in enumerate(sys.argv[1:])]

with open(f"/home/app_user/data/data_{datetime.datetime.today().isoformat()}.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
