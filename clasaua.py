# -*- coding: utf-8 -*-


import os
import re
import sys
from pathlib import Path
from lib.clasaua import Clasaua


def clasaua():
    print("Launcher clasaua function")
    arguments = sys.argv
    app_file_path = re.sub(r'(-script\.py|-script\.pyw|\.exe)?$', '', arguments[0])
    if len(arguments) > 1:
        file_path = arguments[1]
        if os.path.isfile(file_path):
            file_path = file_path


            if getattr(sys, "frozen", False):
                # onefile ou onedir (PyInstaller runtime)
                app_path_folder = Path(sys.executable).parent
                print("frozen, app_path_folder, Path(sys.executable).parent:", app_path_folder)
                internal_path_folder = Path(sys._MEIPASS)
                print("frozen, internal_path_folder, Path(sys._MEIPASS)", app_path_folder)
            else:
                # execución en dev
                app_path_folder = Path(__file__).resolve().parent
                internal_path_folder = app_path_folder
                print("dev, internal and app path folder: ", app_path_folder)

            # check logos in work_path_folder
            images = (
                'logo_foot.png',
                'logo_left.png',
                'logo_right.png')
            images_in_app_path_folder = True
            for image in images:
                image_path = app_path_folder / image
                print("image_path: {}".format(str(image_path)))
                if not image_path.is_file():
                    images_in_app_path_folder = False
            if images_in_app_path_folder:
                images_in_app_path_folder = str(app_path_folder)
            print("images_in_app_path_folder: ", images_in_app_path_folder)
            Clasaua(app_path_folder=app_path_folder, file_path=file_path, work_path_folder=images_in_app_path_folder)
        else:
            print("Clasifications file path not exists.")
    else:
        print("Please specify the ODS file with the classification.")


if __name__ == "__main__":
    print("Launcher main")
    sys.exit(clasaua())
