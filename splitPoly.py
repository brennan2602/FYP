import numpy as np
import pretty_midi
import glob

#This file reads in the midi file converts it to a text file of a monophonic version
#The highest note currently being played is what is written into the encoded file


def get_piano_roll(midifile):
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	return piano_roll

#different to encode in other scripts due to breaking from loop once first (highest note) is found
def encode(arr):
    timeinc=0
    outString=""

    for time in arr:
        i=0
        max=0
        for t in np.flip(time): #flips column of array so you are starting from note 127
            if t >0:
                max=t #first value found that isn't 0 is the max for that column
                      #max also tells us the velocity at that note
                break
            i+=1 #how far you had to move from 127
        if i==128: # looped the whole way through 128-0 and nothing found so nothing is being played
            temp="#"
        else:
            i=127-i # getting the actual note being played by taking steps from 127 away from 127
            temp="("+str(i)+","+str(max)+")" #writing combined encoding for note at this time step
        print(temp)
        file1.write(temp+"\n")
    return outString

file1 = open("Schubert_-_Allegretto_in_C_Minor_D.915_Mono.txt", "a") #file to write monophonic version to
pr = get_piano_roll("Schubert_-_Allegretto_in_C_Minor_D.915.mid") #reading in the polyphonic version of the song
arr = pr.T
encode(arr)
file1.close()