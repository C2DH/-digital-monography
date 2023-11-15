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
CONFIG_NAME = "config.yaml"
STATIC_DIR_NAMES = ["images", "videos", "csv"]
