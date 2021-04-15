import numpy as np
import time
from time import sleep
import pandas as pd
from Sweeping import *
from Dictionaries import * 
from PulseFiles import *
import pyvisa as visa
from datetime import date

def VisaR(AWG,time):

    """ This function sets the pyvisa interface and sets the timeout time.

    This function enables the interaction between the computer and the instrument, throught the pyvisa module.
    Before running this function, please make sure that the AgM8190 Firmware is was properly initialized.
    The Visa Address is given by corresponding key in the AWG dictionary.
    The time should be given in miliseconds.
    It prints the instruments manufacturer, model, serial number.
    It outputs the instruments pyvisa resource object
    """
    rm = visa.ResourceManager()
    inst = rm.open_resource('{visa}'.format( visa = AWG['Visa Resource Name']))
    inst.read_termination = '\n'
    inst.write_termination = '\n'
    inst.timeout = time
    return inst

def Instrument_Settings(instrument):
    f=open("Settings_{dt}.txt".format(dt = date.today()),"w+")
    f.write("{settings}".format( settings= instrument.query('SYST:SET?')))
    f.close()


def Initialization(instrument,AWG):

    """This function sets the initialization of the instrument.

        Instruments output " DC Amp out" is activated and the voltage is set to the value given in the AWG dictionary.
        The Sampling frecuency is set as well, given by the corresponding key.
    """
    instrument.write('INST:COUP:STAT 0') #Decoupling the channels
    instrument.query('*OPC?')
    instrument.write('OUTP1:ROUT DC') #setting the output to DC 
    instrument.query('*OPC?')
    instrument.write('OUTP1 ON') #activating the output "Amp Out"
    instrument.query('*OPC?')
    instrument.write('DC1:VOLT:AMPL {volt}'.format(volt = AWG['Voltage Amplitude']/1000)) #Setting Normilized Voltage amplitude
    instrument.query('*OPC?')
    instrument.write('FREQ:RAST {sr}'.format(sr = AWG['Clock Sample Frecuency']))  #Setting the sample rate
    instrument.query('*OPC?')
    #print(instrument.query('FREQ:RAST?'))
    print('Instruments Sampling Frecuency set to {a}Hz'.format(a = instrument.query('FREQ:RAST?')))
    print('Instruments DC1 Output Voltage set to {V}deciVolts'.format(V = instrument.query('DC1:VOLT:AMPL?')))

def Segment_File(instrument,File,id):

    """
    This functions loads the csv file "File" into the AWG as a Segment with the corresponding id.

    This function uses the TRAC Subsystem of the AWG, alongside with SCPI. The AWG may create a segment whose length is larger than the data size to
    account for the granularity, but that does not alters any value within the sample data.
    """
    #precision mode for now, vector size in samples is multiple of 48
    instrument.write('TRAC1:DWID WPR')
    instrument.query('*OPC?')
    instrument.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=r'{Fil}'.format(Fil=File)))
    instrument.query('*OPC?')



def Segment_Array(instrument,id,pulse_array0,AWG,marker,step):
    
    """ This function takes np pulse arrays as imput and exports them as csv files, then it loads these files to the instrument as segments.

    The importing from np arrays into csv files is done with the CSV_PD function from Pulsefiles module.
    The loading of this new csv file into the instrument as a new segment is perfomed with the Segment_File function.
    'instrument' correspond to the visa resource instrument object associated with our Instrument.
    'id' corresponds to an positive integer, which will be the Segemet id within the Instrument.
    """
    #creating the csv file using CSV_PD function
    new_csv, SegMark = CSV_PD(pulse_array0, AWG, marker ,step)

    #sending the csv file to the instrument
    Segment_File(instrument, new_csv, id)
    print('Current Segment Catalogue is {g}  [(segment id, Segment size)]'.format(g = instrument.query('TRAC:CAT?')))

    return new_csv, SegMark


def Def_Sequence(instrument,loop):

    """This function defines a new Sequence in the AWG and outputs the sequence id.

        The new sequence will have 2 steps, and will only load the two corresponding segments
        that must be prevoiusly defined and loaded in th AWG (either by hand, or with the Segment functions
        in this module).
        The Sequence will have a length of 2, it is specifically designed for creating sequences with segments.
    """
    #Initializing the Sequence Function Mode
    instrument.write('FUNC1:MODE STS')
    instrument.query('*OPC?')

    #Defining new sequence.
    seq_id = int(instrument.query('SEQ1:DEF:NEW? 2'))

    #loading segments into sequences within the Instrment has the following syntaxis:
    #instrument.write('[:SOURce]:SEQuence[1|2]:DATA <sequence_id>, <step> , <segment_id>, <loop_count>,<advance_mode>,<marker_enable>, <start_addr>,<end_addr>

    #Loading Segment 1 to step 0 of Sequence 0
    instrument.write('SEQ1:DATA {seqid},0,1,{l},0,1,0,#hFFFFFFFF'.format(seqid = seq_id, l =loop))
    instrument.query('*OPC?')

    #Loading Segment 2 to step 1 of Sequence 0
    instrument.write('SEQ1:DATA {seqid},1,2,{l},0,1,0,#hFFFFFFFF'.format(seqid = seq_id, l = loop))
    instrument.query('*OPC?')
    
    
    instrument.write('STAB1:SEQ:SEL {t}'.format(t = seq_id))

    print('Sequence loaded with the following segment data "{b}"'.format(b = instrument.query('SEQ1:DATA? {c},0,2'.format(c=seq_id))))

    return seq_id


def Sequence_File(instrument,file0,file1,loop):

    """ Creates a sequence in the instrument by the data in file0 and file1 csv files.

    This function first calls the Segment_File function to load the file0 and file1 csv data files as segments into the instrument.
    It then uses the AWG's SEQ subsystem to create a sequence from this two segments.This sequence is set to 1 loop count, auto advance mode
    and starting and ending address correspond to the first and last value of the data files.
    The SCPI query SEQ:DEF:NEW? returns the Sequence Id. as a string and this functions returns it as an int.
    """
    Segment_File(instrument, file0, 1)
    Segment_File(instrument, file1, 2)

    #Define the corresponding Sequence:
    seq_id = Def_Sequence(instrument,loop)
    return seq_id

def Sequence_Array(instrument,pulse_array0,pulse_array1,AWG,step,loop):

    """This function loads 2 numpy pulse data arrays into a sequence in the AWG

    It utilizes first the Segment_Array function to import as segments the CSV files corresponding to 
    the pulse_array0/1 numpy arrays. Then it imports them as sequence to the AWG using the Sequence_File function.
    It outputs the sequence id of the newly define sequence, and the data frame of the segments.
    """

    #Creating cvs files and loading them to the AWG as segments
    c, datac= Segment_Array(instrument, 1, pulse_array0, AWG, 1, step)
    b, dataB= Segment_Array(instrument, 2,pulse_array1, AWG, 0, step)
    
    #Creating the Sequence within the Instrument
    seqid= Def_Sequence(instrument,loop)


    return seqid, datac, dataB 
  



def Sequence_Loader(instrument,LocationA,LocationB,loop,sleeptime):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence.

    It uses the SeqF function to load the files to the instrument.
    "sleeptime" is the time that the function waits before loading the next sequence, it is in seconds.
    """
    start = time.time()

    for i,j in zip(LocationA, LocationB):
        Sequence_File(instrument,LocationA[i],LocationB[j],loop)
        instrument.query('*OPC?')
        
        instrument.write('INIT:IMM')
        sleep(sleeptime)
        instrument.write('ABOR')
   
    end = time.time()

    print(end-start)   






