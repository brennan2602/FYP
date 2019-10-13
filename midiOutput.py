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
timeinc = -1
np.savetxt("verify.txt", arr, fmt="%s")

for time in arr:
    timeinc = timeinc+1
    notesinc = -1
    for vel in arr[timeinc]:
        notesinc=notesinc+1
        if vel != 0:
            #print("velocity-",vel, " sampleNum(time)-" , xinc, " note-" ,yinc)
            print(" note-" ,notesinc, " sampleNum(time)-" , timeinc,"velocity-",vel )
        
    #if x != 0:
     #   print(inc , " " , x)