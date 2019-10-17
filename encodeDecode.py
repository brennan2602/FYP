import numpy as np
import pretty_midi

def get_piano_roll(midifile):
	#midi_data = pretty_midi.PrettyMIDI('test.midi')
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=25)
	print(piano_roll.shape)
	return piano_roll


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
		outString=outString+"_"
		timeinc = timeinc+1
	return outString

def decode(test):
	test=test[:-1]
	output=test.split("_")
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
				note,velocity = n.split(",")
				arr[int(note),timeindex]=velocity
		timeindex=timeindex+1
	arr=arr.T
	return arr

pr = get_piano_roll("test.midi")
arr = pr#[:,-250:]
arr = arr.T
np.savetxt("verify.txt", arr, fmt="%s")
outString= encode(arr)
print(outString)
decoded=decode(outString)


np.savetxt("verify.txt", arr, fmt="%s")
np.savetxt("verify2.txt", decoded, fmt="%s")
if np.array_equal(arr, decoded):#decoded==arr:
	print("works")
else:
	print("no luck")
	print(decoded)
	print("\n" ,arr)