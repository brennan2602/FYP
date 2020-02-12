import glob
import random
import pretty_midi
import numpy as np

# with open(r'C:\Users\brenn\PycharmProjects\FYP\venv\generatedPureRand.txt') as f: #change to some training data
#     lines = f.readlines()
#     print(lines)

def generateFromData(lines):
    i=0
    outString=""
    while i<=500:
        num = random.randint(1, len(lines))
        line=lines[i]
        numSample= random.randint(1,20)
        for j in range(0, numSample):
            if i<=500:
                outString=outString+line
            i+=1

    print(outString)
    return outString

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

def decode(test):
	test=test[:-1]
	output=test.split("\n")
	#print(output)
	res = len(output)
	arr=np.zeros((128,res))
	print(arr.shape)
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
					print(note,velocity)
		timeindex=timeindex+1
	#arr=arr.T
	return arr

files=glob.glob(r"C:\Users\brenn\PycharmProjects\FYP\venv\encodedFiles\*.txt")
print(files)
for f in files:
    x= f.split("\\")[-1]
    name=x.split(".txt")[0]
    print(name)
    #print(x)
    with open(f) as text:
        lines = text.readlines()
        #print(lines)
    generated = generateFromData(lines)
    decoded = decode(generated)
    fs = 20
    pm = piano_roll_to_pretty_midi(decoded, fs=fs, program=2)
    pm.write("GenWith"+name+".midi")
