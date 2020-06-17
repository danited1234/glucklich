import os
import sys 
import json
import pygame
from pygame import mixer
import inquirer
from inquirer.themes import GreenPassion
from pydub import AudioSegment
import ast
#making a function so if the user wants to change directory in config file in line 2 they can change it from there
files=[]
path=[]
def reading_config():
    filename="config.json"
    with open(filename,"r") as f:
        lines=f.readlines()
        line1=lines[1][6:].strip()
        #os.chdir(line1)
    return line1
#sometimes pygame doesnt play mp3 files correctly so we have to convert file into wav format
def Convert(audio_file):
    sound=AudioSegment.from_file(audio_file,format="mp3")
    sound.export(".test.wav",format="wav")
    return
#Convert()
def clear_terminal():
    clear_screen=os.system("cls" if os.name=="nt" else "clear")
    return clear_screen
# the main function that plays the audio file and provides the fucntionality to pause, unpause and quit the program by using the inquirer library
def play_music(audio_file):
    #this part of the script plays the song or any audio that the user selects
    pygame.mixer.init()
    mixer.music.load(audio_file)
    mixer.music.play()
    active=True
    while active:
        print(f"Currently playing {audio_file}")
        questions=[
            inquirer.Checkbox("p,u,q",message="Do you want to pause or unpause",choices=['Pause','Unpause','Quit'])
        ]
        answers=inquirer.prompt(questions,theme=GreenPassion())
        for keys,values in answers.items():
            temps=(keys,values)
            listodict=temps
            listtostring=' '.join(map(str,temps))
            finalstrings=listtostring[5:].strip()
            stringtolist=ast.literal_eval(finalstrings)
            if len(stringtolist)==1:
                if "Pause" in stringtolist:
                    mixer.music.pause()
                    clear_terminal()
                elif "Unpause" in stringtolist:
                    mixer.music.unpause()
                    clear_terminal()
                elif "Quit" in stringtolist:
                    print(f"Thank you for using the program")
                    os.system("unlink .test.wav")
                    active=False
                    sys.exit()
                else:
                    print(f"We did not find the commad")
            elif len(stringtolist)>1:
                    print(f"We can only take upto one choice")
            else:
                    print(f"We did not recognize the command")
    return
# this function provides the functionality that the user entered 
def finding_files():
    clear_terminal()
        # for finding all the files that in the path that the user has entered in the config.json file
    for FolderNames,Subfolder,Filenames in os.walk(reading_config()):
        for filenames in Filenames:
            if filenames.endswith(".wav") or filenames.endswith(".mp3"):
                paths=f"{FolderNames}/{filenames}"
                global path
                path.append(paths)
                global files 
                files.append(filenames)
    return
# for changing directories if the audio file is another directory or subfolder of a folder
def changing_dir(Music_file):
    for direcotories in path:
        if Music_file in direcotories:
            direcotory=os.path.dirname(direcotories)
            os.chdir(direcotory)
    return
def main():
    q=[
        inquirer.Checkbox("Music Files",message="Select Music files that you want to play",choices=files)
        ]
    answers=inquirer.prompt(q,theme=GreenPassion())
    for key,value in answers.items():
        temp=(key,value)
        DictToList=temp
    listToString=' '.join(map(str,temp))
    finalString=listToString[12:]
    stringToList=ast.literal_eval(finalString)
    if len(stringToList)>=2:
        for songs in stringToList:
            changing_dir(stringToList)
            if songs.endswith(".mp3"):
                Convert(songs)
                play_music(".test.wav")
                os.system("unlink .test.wav")
            else:
                changing_dir(songs)
                play_music(songs)
    elif len(stringToList)==1:
        single_audio=' '.join(map(str,stringToList))
        changing_dir(single_audio)
        if single_audio.endswith(".mp3"):
            Convert(single_audio)
            play_music(".test.wav")
            os.system("unlink .test.wav")
        elif single_audio.endswith(".wav"):
            play_music(single_audio)
        else:
            print(f"We dont support the extension {single_audio.endwith}")
            sys.exit()
    else:
            print("Something went wrong")
    return
finding_files()
main()