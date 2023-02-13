@ECHO OFF

ECHO Installing your exe in dist folder.......

pyinstaller main.py --name monodon_app --noconsole --onefile --icon=Imagenes\monodon_logo.ico --add-data "Imagenes\*.jpg;Imagenes" --add-data "Imagenes\monodon_background.png;Imagenes" --add-data "Imagenes\monodon_logo.ico;Imagenes"
ECHO Installation completed succesfully

PAUSE