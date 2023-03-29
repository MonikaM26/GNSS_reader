from GUI.GUI import  GUI
import time
from config.pconfig import read_config

CONFIG_PATH = "config"
GNSS_CONFIG = f"{CONFIG_PATH}/gnss_config.yaml"
GNSS_BASE_MODE = "test"


def main():

    thrmng = GUI(
        gnss_base_config = read_config(GNSS_CONFIG)["base"][GNSS_BASE_MODE]
    )
    while True:
        if thrmng.stop_program == True:
            break
        thrmng.check_status()
        time.sleep(2)


if __name__ == '__main__':
    main()
