# from __future__ import division
# import sys
# import argparse
import numpy as np
import pretty_midi
#import librosa

def get_piano_roll(midifile):
    #midi_data = pretty_midi.PrettyMIDI('test.midi')
    midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
    piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
    piano_roll = piano_midi.get_piano_roll(fs=60)
    print(piano_roll.shape)
    return piano_roll


    
pr = get_piano_roll("test.midi")
#sec200 = pr[:,:]
#print(sec200)
arr = pr[:,-250:]
arr = arr.T

np.savetxt("verify.txt", arr, fmt="%s")

#this will print out times where notes are being played in the format note*time*velocity*:note*time*velocity etc the : represents another note being played at the same time
#timeinc = -1
# for time in arr:
    # timeinc = timeinc+1
    # notesinc = -1
    # print(" ")
    # for vel in arr[timeinc]:
        # notesinc=notesinc+1
        # if vel != 0:
            # #print("velocity-",vel, " sampleNum(time)-" , xinc, " note-" ,yinc)
            # #print(" note-" ,notesinc, " sampleNum(time)-" , timeinc,"velocity-",vel, end = '' )
            # print(notesinc,timeinc,vel,":" , sep='*',end = '')

#this will print out in format :*note*velocity:note*velocity-time where : represents the start of a note "object" where no notes are played only -time is printed
timeinc=0
for time in arr:
    notesinc = -1
    
    for vel in arr[timeinc]:
        notesinc=notesinc+1
        if vel != 0:
            #print("velocity-",vel, " sampleNum(time)-" , xinc, " note-" ,yinc)
            #print(" note-" ,notesinc, " sampleNum(time)-" , timeinc,"velocity-",vel, end = '' )
            print(":",notesinc,vel, sep='*',end = '')       
    print("-",timeinc, sep ="")        
    timeinc = timeinc+1        
            