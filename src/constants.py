HERO = """\
                                                                                    
____   _       _  _         _                                              _        
|    \ |_| ___ |_|| |_  ___ | |   _____  ___  ___  ___  ___  ___  ___  ___ | |_  _ _ 
|  |  || || . || ||  _|| .'|| |  |     || . ||   || . || . ||  _|| .'|| . ||   || | |
|____/ |_||_  ||_||_|  |__,||_|  |_|_|_||___||_|_||___||_  ||_|  |__,||  _||_|_||_  |
        |___|                                        |___|          |_|       |___|

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
CONFIG_NAME = "config.toml"
STATIC_DIR_NAMES = ["img", "videos", "csv"]
