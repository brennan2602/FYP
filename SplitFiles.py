import numpy as np
import os
from os import path
import shutil
import pandas as pd

data = pd.read_csv('maestro-v2.0.0.csv') #Reading in the CSV which details splits
#Setting up parts of the path that MIDI files are being copied to
dstTrain="\\train\\"
dstVal="\\validate\\"
dstTest="\\test\\"

#print(data.head())
splits = data['split'].tolist() #creating a list of the split values in each row
midi = data['midi_filename'].tolist() #creating a list of filename values in each row

#val = midi[1].split('/')
#val=val[1]
#print(val)

#looping through the midi list
for x in range(0,len(midi),1):
    val = midi[x].split('/')
    val = val[1]
    print(val) # this is the filename (with the leading year folder removed)

    #These if statements check what the split type is for a file by looking at the split value in the for the same row
    #as the filename that is currently being checked in the loop

    if splits[x]=="train":
        dst=dstTrain+val #some path manipulation
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst) #copying to a new directory under the matching split type here train
    if splits[x]=="test":
        dst=dstTest+val #some path manipulation
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst) #copying to a new directory under the matching split type here test
    if splits[x]=="validation":
        dst=dstVal+val
        print(dst)
        os.makedirs(dst)
        shutil.copy(midi[x], dst) #copying to a new directory under the matching split type here validation

