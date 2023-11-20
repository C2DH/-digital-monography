HERO = """

 ┓•  •   ┓                   ┓   
┏┫┓┏┓┓╋┏┓┃  ┏┳┓┏┓┏┓┏┓┏┓┏┓┏┓┏┓┣┓┓┏
┗┻┗┗┫┗┗┗┻┗  ┛┗┗┗┛┛┗┗┛┗┫┛ ┗┻┣┛┛┗┗┫
    ┛                 ┛    ┛    ┛

"""
_V = {
    "MAJOR": 0,
    "MINOR": 1,
    "PATCH": 0,
}
VERSION = ".".join(str(v) for v in [_V["MAJOR"], _V["MINOR"], _V["PATCH"]])
PROJECT_SLUG = "digital-monography"
PROJECT_NAME = PROJECT_SLUG.replace("-", " ").title()
AUTHORS = ["Luxembourg Centre for Contemporary and Digital History (C²DH)"]
DATA_DIR = "/home/app_user/data"
LOGS_DIR = "/home/app_user/logs"
STATIC_DIR = "src/static"
CONFIG_NAME = "config.yaml"
STATIC_DIR_NAMES = ["images", "videos", "csv"]
SYSTEM_SPECIFIC_NAME = "_dgt_mon"
DEFAULT_MYSTMD_CONFIG = {
    "version": 1,
    "project": {"github": "https://github.com/C2DH/digital-monography"},
    "site": {
        "template": "book-theme",
        "logo": f"./images/{SYSTEM_SPECIFIC_NAME}/uni_logo.png",
        "actions": [
            {
                "title": "About C²DH",
                "url": "https://www.c2dh.uni.lu",
            }
        ],
    },
}
