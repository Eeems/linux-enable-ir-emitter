#!/usr/bin/env python3

from yaml import load, FullLoader
from os import system


def create_systemd(command):
    file_content = "[Unit]\nDescription=enable ir emitter\nAfter=multi-user.target suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target\n\n[Service]\nType=oneshot\nExecStart=/usr/local/bin/{}\n\n[Install]\nWantedBy=multi-user.target suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target\n".format(command[2:])

    file = open("enable-ir-emitter.service", "w")
    file.write(file_content)
    file.close()

    system("sudo cp enable-ir-emitter /usr/local/bin")
    system("sudo cp enable-ir-emitter.service /etc/systemd/system")
    system("sudo systemctl enable --now enable-ir-emitter")


if __name__ == "__main__":
    system("gcc enable-ir-emitter-template.c -o enable-ir-emitter")

    with open("config.yaml") as config_file:
        config_list = load(config_file, Loader=FullLoader)

    i = 0
    for config in config_list:
        print("Configuration #{} ...".format(i))

        data = config["data"]
        data_size = data.count(" ") + 1
        unit = config["unit"]
        selector = config["selector"]

        command = "./enable-ir-emitter -dataSize {} -data {} -unit {} -selector {}".format(data_size, data, unit, selector)
        res = system(command)

        check = ""
        if not res:
            while check not in ("yes", "no", "y", "n"):
                check = input("A configuration has been found, do you want to test now ? Yes/No ? ").lower()

            if check in ("yes", "y"):
                check = ""
                system("python3 capture.py 2 5")
            else:
                check = ""
                print("OK, please test if the emitter of your infrared camera works by yourself.")

            while check not in ("yes", "no", "y", "n"):
                check = input("Does it work ? Yes/No ? ").lower()

            if check in ("yes", "y"):
                check = ""
                while check not in ("yes", "no", "y", "n"):
                    check = input("Do you want to automatically activate the emitter at system startup ? Yes/No ? ").lower()

                if check in ("yes", "y"):
                    print("Creation of the systemd service ... (administrator commands will be executed)")
                    create_systemd(command)
                else:
                    print("No problem, here is the command: ", command)
                break

        i += 1
