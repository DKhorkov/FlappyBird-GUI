A FlappyBird game, where user can choose bird color, pipes color,
his own picture for background, screen resolution, music, number
of lives and difficulty. Also, there is a Database, where all
user's data is saves (last configs and record).

For creating executable file, use next command in head directory:
pyinstaller --onefile --windowed --icon=images/favicon.ico -n FlappyBird
--distpath <Destination, where exe file would be> main.py


Executable file need to be put in head directory to all other
images and sound objects for correct work.