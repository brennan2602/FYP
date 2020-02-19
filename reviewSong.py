import numpy as np
import pretty_midi
import glob

#This file reads in the midi files in a directory, converts them to a string representation
#when in a string representation it then gathers some statistics about the structure of the song

def get_piano_roll(midifile):
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	return piano_roll

#uses split encoding scheme (here only encoding the note values)
#works by looping through time increments of the piano roll array and writing the notes being played
#at a given time sample as a number on the corresponding line of a string # is written when no notes played for that
#sample
def encode(arr):
    timeinc=0
    outString=""
    for time in arr:
        notesinc = -1
        #print(time)
        if np.all(time==0):
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1
            if vel != 0:
                noteRep=str(notesinc) + " "
                #print(noteRep)
                outString=outString+noteRep
        outString=outString+"\n"
        timeinc = timeinc+1
    return outString


def getSilences(test):
    test=test[:-1] #removing last line in string (always blank)
    output=test.split("\n") #splitting into array
    res = len(output)
    #initialising counters
    maxcounter=0
    counter=0
    silenceCount=0

    for x in output:
        if x == "#": #when a "#" is seen nothing is being played that sample
            counter=counter+1 #this tracks a streak of silences
            silenceCount+=1 #this tracks total silences
        if x != "#":
            counter=0 #reseting streak
        if counter>maxcounter:
            maxcounter=counter #updating longest silence streak when appropriate
    return maxcounter,silenceCount


#by looking at the length of song and the amount of silences this returns % silence
def getPercentSilence(gen,silences):
    test = gen
    test = test[:-1]
    output = test.split("\n")
    res = len(output)
    percent=silences/res
    return percent


def getStatsNotes(test):
    test=test[:-1] #get rid of blank line at the end
    notes=[]
    output = test.split("\n") #split string on new lines

    #initial values updated while looping through
    maxPerSamp=0
    silenceSamp=0
    notesPlayed=0
    maxNotes=0
    maxVal=0
    minVal=127

    for x in output:
        samp=x.split(" ")
        samp=samp[:-1] #theres a blank result at the end of array from split this indexing removes it
        while "0" in samp:
            samp.remove("0") #sometimes 0 samples exist this removes them as they aren't notes played
        if len(samp)==0:
            silenceSamp+=1 #counting silences
        notesPlayed=notesPlayed+len(samp) #counting notes played
        if len(samp)>0:
            #getting max and min note values at this time step
            minimum=min(samp)
            maximum=max(samp)
            #updating max and min values note values for song if appropriate
            if int(minimum)<minVal:
                minVal=int(minimum)
            if int(maximum)>maxVal:
                maxVal=int(maximum)
        #updating maximum number of notes per sample if appropriate
        if len(samp)>maxNotes:
            maxNotes=len(samp)
    rangeNotes=maxVal-minVal #spread of notes
    avgNotes = notesPlayed / len(output) #average notes per sample
    adjNotes=notesPlayed /(len(output)-silenceSamp) #average notes per sample adjusted to remove silent samples
    return rangeNotes, maxVal, minVal,maxNotes,avgNotes,adjNotes


files=glob.glob(r"*.midi")#point towards directory with midi files (here same folder)
print(files)

for f in files:
    print(f)
    pr = get_piano_roll(f) #gets piano roll representation of the midi file
    arr = pr.T
    outString= encode(arr) #gets a string representation of the midi file
    maxsilences, silences = getSilences(outString) #by passing in the encoded string get longest silence and the total
                                                   #number of samples which are silent
    noteRange, maxVal, minVal, maxNotes, avgNotes, adjAvg =getStatsNotes(outString) # getting some stats by looping
                                                                                    # through encoded data
    percentSilence= getPercentSilence(outString,silences) # get % silence from silence / outString length

    #printing out to the user
    print("longest silence is ",maxsilences,"samples long")
    print("silence covers:",round(percentSilence,4),"%")
    print("notes span range:",noteRange)
    print("max note value:",maxVal)
    print("min note value:",minVal)
    print("average number of notes per sample:",round(avgNotes,4))
    print("average number of notes per sample (adjusted to remove silence samples):",round(adjAvg,4))
    print("max number of notes played in a sample:",maxNotes)
    print("\n")

#NOTE some minor discrepencies vs reading in from generated file directly
#However this does provide a uniform check to use for songs generated by both encoding schemes
#Can also be used to evaluate training file
#uses split encoding to get the text representation for ease of development
