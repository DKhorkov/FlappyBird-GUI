A FlappyBird game, where user can choose bird color, pipes color, 
day or night background or choose his own picture for background, 
size of screen, music, number of lives and difficulty. Also there
is a Database, where all users data is saves (last configs and record).

For creating executable file, use next command in head directory:
pyinstaller --onefile --windowed --icon=images/favicon.ico game.py 

Executable file need to be put in head directory to all other
images and sound objects for correct work.