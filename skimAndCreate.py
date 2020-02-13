import numpy as np
import pretty_midi
import glob

def piano_roll_to_pretty_midi(piano_roll, fs=1, program=0):
    '''Convert a Piano Roll array into a PrettyMidi object
     with a single instrument.
    Parameters
    ----------
    piano_roll : np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    program : int
        The program number of the instrument.
    Returns
    -------
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.
    '''
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm

def get_piano_roll(midifile):
	#midi_data = pretty_midi.PrettyMIDI('test.midi')
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	print(piano_roll.shape)
	return piano_roll

def decode(test):
    test=test[:-1]
    output=test.split("\n")
    #print(output)
    res = len(output)
    arr=np.zeros((128,res))
    #print(arr.shape)
    timeindex=0
    for x in output:
        newx=x.replace(")(", "-")
        newx=newx.replace("(","")
        newx=newx.replace(")","")
        noteGroup = newx.split("-")
        for n in noteGroup:
            if n != "#":
                #print(n)
                s=len(n.split(","))
                #print(s)
                if s==2:
                    note,velocity = n.split(",")
                    if velocity.count("#")>0 or velocity.count('.')>1:
                        velocity=0
                        note = 0
                    elif note.count("#")>0 or note.count('.')>1:
                        note=0
                        velocity = 0
                    note=float(note)

                    if int(note)>126:
                        note =0
                        velocity = 0
                    if velocity=="":
                        velocity=0
                        note = 0
                    if int(float(velocity))>126:
                        velocity=0
                        note = 0
                    arr[int(note),timeindex]=velocity
                    #print(note,velocity)
        timeindex=timeindex+1
    #arr=arr.T
    return arr

def encode(arr):
    timeinc=0
    outString=""
    for time in arr:
        notesinc = -1
        if np.all(time==0):
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1
            if vel != 0:
                noteRep=str(notesinc)+"-"+ str(vel)+"_"
                noteRep="("+str(notesinc)+","+ str(vel)+")"
                outString=outString+noteRep
        outString=outString+"\n"
        timeinc = timeinc+1
    return outString

def encodeNotes(arr):
    timeinc=0
    outString=""
    for time in arr:
        notesinc = -1
        if np.all(time==0):
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1
            if vel != 0:
                #noteRep=str(notesinc)+"-"+ str(vel)+"_"
                noteRep=str(notesinc) + " "
                outString=outString+noteRep
        outString=outString+"\n"
        timeinc = timeinc+1
    return outString




# with open(r"C:\Users\brenn\Desktop\FYP_DATA\generated\LSTM\combined\5 songs\25epo\generated.txt") as text:
#     linesGenerated = text.readlines()

#file1 = open("skimmed.txt", "a")


def midiToArray(midifile):
    pr = get_piano_roll(midifile)
    arr = pr.T
    outString = encodeNotes(arr)
    lines=outString.split("\n")
    encodedWithAll=encode(arr)
    linesWithAll = encodedWithAll.split("\n")
    print(lines)
    print("len="+str(len(lines)))
    # stringRep=""
    # for l in lines:
    #     stringRep=stringRep+l
    # print(stringRep)
    return lines,linesWithAll#stringRep


def skimFile(linesGenerated,linesGeneratedAll,linesInDataset):
    newLines = []
    i=1
    for l in linesGenerated:

        print("checking line: "+str(i))
        #print(l)
        i+=1
        if linesInDataset.count(str(l)+"\n")>0:
            newLines.append(str(linesGeneratedAll[i-1])+"\n")
            print("match -"+str(l))
            #file1.write(l)
        else:
            print("no match -"+l)

    inDataset=len(newLines)/(len(linesGenerated)-1) #last sample always blank
    print(inDataset)
    stringRep=""
    for l in newLines:
        stringRep=stringRep+l
    print(stringRep)
    return stringRep#newLines

with open(r"C:\Users\brenn\PycharmProjects\RNN2\FullyEncoded\fulldataNotes.txt") as text:
    linesInDataset = text.readlines()

midiArray,midiArrayWithAll=midiToArray(r"C:\Users\brenn\Desktop\generatedData\generated\LSTM\split\alt song\25epo\piano.midi")
skimmed=skimFile(midiArray,midiArrayWithAll,linesInDataset)
decoded = decode(skimmed)
fs = 20
pm = piano_roll_to_pretty_midi(decoded, fs=fs, program=2)
pm.write("skimmedPiano.midi")



