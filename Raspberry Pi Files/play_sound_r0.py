import os
cwd=os.getcwd()
global path
from pydub import AudioSegment
from pydub.playback import play
path_terminator='/home/pi/Desktop/terminator_soundboards/'
path_starwars='/home/pi/Desktop/StarWars_audio'
def play_Strong_with_the_force():
    path_i=os.path.join(path_starwars,'Strong with the force.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
def The_force():
    path_i=os.path.join(path_starwars,'The force.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
def light_saber_on():
    path_i=os.path.join(path_starwars,'light-saber-on.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
def light_saber_off():
    path_i=os.path.join(path_starwars,'light-saber-off.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
def star_wars_theme():
    path_i=os.path.join(path_starwars,'star-wars-theme-song.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
def play_theme():
    path_i=os.path.join(path_terminator,'Theme Song.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)
    
def play_mycpu():
    path_i=os.path.join(path_terminator,'My CPU is intact.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)

def play_Cybernetic():
    path_i=os.path.join(path_terminator,'Cybernetic organism.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)

def play_Hasta():
    path_i=os.path.join(path_terminator,'Hasta la vista.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)

def play_beback():
    path_i=os.path.join(path_terminator,'Ill be back.mp3')
    sound = AudioSegment.from_mp3(path_i)
    play(sound)

def play_sound(rq):
    import threading
    while True:
        try:
            case=rq.get(False)
            if case=='hasta':
                threading.Thread(target=play_Hasta()).start()
            if case=='beback':
                threading.Thread(target=play_beback()).start()
            if case=='cyber':
                threading.Thread(target=play_Cybernetic()).start()
            if case=='cpu':
                threading.Thread(target=play_mycpu()).start()
            if case=='theme':
                threading.Thread(target=play_theme()).start()
            if case=='strongforce':
                threading.Thread(target=play_Strong_with_the_force()).start()
            if case=='star_wars_theme':
                threading.Thread(target=star_wars_theme()).start()
            if case=='light_on':
                threading.Thread(target=light_saber_on()).start()
            if case=='light_off':
                threading.Thread(target=light_saber_off()).start()
            if case=='theforce':
                threading.Thread(target=The_force()).start()
        except:
            pass