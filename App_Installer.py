import subprocess
import os

subprocess.call(r"pyinstaller GUI.py --name monodon_app --noconsole --onefile "
                r"--icon=Imagenes\monodon_logo.ico --add-data Imagenes\*.jpg;Imagenes "
                r"--add-data Imagenes\monodon_background.png;Imagenes "
                r"--add-data Imagenes\monodon_logo.ico;Imagenes")
os.remove("main.spec")
os.remove("monodon_app.spec")

