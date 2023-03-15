pyinstaller --onefile --noconsole --add-data "./previous.png:."  --add-data "./pause.png:." --add-data "./next.png:." --add-data "./play.png:." main.py --hidden-import="PIL._tkinter_finder"
