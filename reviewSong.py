import numpy as np
import pretty_midi
import glob

def get_piano_roll(midifile):
	#midi_data = pretty_midi.PrettyMIDI('test.midi')
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	#print(piano_roll.shape)
	return piano_roll


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

# with open('generatedNotes.txt') as f:
#     lines = f.readlines()
# outString=""
# for l in lines:
#     if len(l.strip()) != 0:
#         outString=outString+l

def getSilences(test):
    test=test[:-1]
    output=test.split("\n")
    res = len(output)
    maxcounter=0
    counter=0
    silenceCount=0
    for x in output:
        if x == "#":
            counter=counter+1
            silenceCount+=1
        if x != "#":
            counter=0
        if counter>maxcounter:
            maxcounter=counter
    return maxcounter,silenceCount

def getPercentSilence(gen,silences):
    test = gen
    test = test[:-1]
    output = test.split("\n")
    res = len(output)
    percent=silences/res
    return percent

# def getRange(test):
#     test=test[:-1]
#     notes=[]
#     test= test.replace("#","")
#     test=test.replace("\n","")
#     output=test.split(" ")
#     for x in output:
#         #print(x)
#         if x != "#" and x!="0":
#             note = x.strip("\n")
#             notes.append(note)
#     #print(notes)
#     maxVal = max(notes[:-1])
#     minVal = min(notes[:-1])
#     rangeNotes=int(maxVal)-int(minVal)
#     return rangeNotes, maxVal, minVal
#
# def getAvgNotes(test,silences):
#     test=test[:-1]
#     notes=[]
#     numSamples = test.split("\n")
#     test= test.replace("#","")
#     test=test.replace("\n","")
#     output=test.split(" ")
#     for x in output:
#         if x != "#":
#             notes.append(x)
#     res = len(numSamples)
#     print(res,len(notes),silences)
#     avgNotes=len(notes)/res
#     adjNotes=len(notes)/(res-silences)
#     return avgNotes,adjNotes

def getStatsNotes(test):
    test=test[:-1]
    #print(test)
    notes=[]
    output = test.split("\n")
    #print(output)
    #test= test.replace("#","")
    #test=test.replace("\n","")
    maxPerSamp=0
    #print(len(output))
    silenceSamp=0
    notesPlayed=0
    maxNotes=0
    maxVal=0
    minVal=127
    for x in output:
        samp=x.split(" ")
        samp=samp[:-1]
        while "0" in samp:
            samp.remove("0")
        if len(samp)==0:
            silenceSamp+=1
        notesPlayed=notesPlayed+len(samp)
        if len(samp)>0:
            minimum=min(samp)
            maximum=max(samp)
            if int(minimum)<minVal:
                minVal=int(minimum)
            if int(maximum)>maxVal:
                maxVal=int(maximum)
        if len(samp)>maxNotes:
            maxNotes=len(samp)
            #print(samp)
    # print(minVal)
    # print(maxVal)
    # print(silenceSamp)
    # print(maxNotes)
    #print(notesPlayed)
    rangeNotes=maxVal-minVal
    #totalSamples=len(output)
    avgNotes = notesPlayed / len(output)
    #print(avgNotes)
    adjNotes=notesPlayed /(len(output)-silenceSamp)
    #print(adjNotes)
    #print(len(output),notesPlayed,silenceSamp)
    return rangeNotes, maxVal, minVal,maxNotes,avgNotes,adjNotes



        #print(samp)
        #len(samp)


    #for x in output:
     #   print(x)
        #print(x," ---> ", len(x))
    #     numNotes=len(x)
    #     if numNotes>maxPerSamp:
    #         maxPerSamp=numNotes
    # print(maxPerSamp)
    #     if x != "#":
    #         notes.append(x)
    # res = len(numSamples)
    # avgNotes=len(notes)/res
    # adjNotes=len(notes)/(res-silences)
    # return avgNotes,adjNotes


files=glob.glob(r"*.midi")
print(files)
for f in files:
    #outString=""
    # x= f.split("\\")[-1]
    # #print(x)
    # fileName=f+"\\"+x
    print(f)
    pr = get_piano_roll(f)
    arr = pr.T
    outString= encode(arr)

    
    #print(outString)
    # maxsilences,silences= getSilences(outString)
    # print("longest silence is ",maxsilences,"samples long")
    # percentSilence= getPercentSilence(outString,silences)
    # print("silence covers:",round(percentSilence,4),"%")
    # noteRange, maxVal,minVal= getRange(outString)
    # print("notes span range:",noteRange)
    # print("max note value:",maxVal)
    # print("min note value:",minVal)
    # avgNotes,adjAvg= getAvgNotes(outString,silences)
    # print("average number of notes per sample:",round(avgNotes,4))
    # print("average number of notes per sample (adjusted to remove silence samples):",round(adjAvg,4))
    # print("\n")



    maxsilences, silences = getSilences(outString)
    noteRange, maxVal, minVal, maxNotes, avgNotes, adjAvg =getStatsNotes(outString)
    percentSilence= getPercentSilence(outString,silences)
    print("longest silence is ",maxsilences,"samples long")
    print("silence covers:",round(percentSilence,4),"%")
    print("notes span range:",noteRange)
    print("max note value:",maxVal)
    print("min note value:",minVal)
    print("average number of notes per sample:",round(avgNotes,4))
    print("average number of notes per sample (adjusted to remove silence samples):",round(adjAvg,4))
    print("max number of notes played in a sample:",maxNotes)
    print("\n")

