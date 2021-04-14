import numpy as np
import pandas as pd
from Sweeping import *
from Dictionaries import * 
from PulseFiles import *
import pyvisa as visa

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


def Init(instrument,AWG):

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

def FileL(instrument,File,id):

    """
    This functions loads the csv file "File" into the AWG as a Segment whose Id is id.

    This function uses the TRAC Subsystem of the AWG, alongside with SCPI. The AWG may create a segment whose length is larger than the data size to
    account for the granularity, but that does not alters any value within the sample data.
    """
    #precision mode for now, vector size in samples is multiple of 48
    instrument.write('TRAC1:DWID WPR')
    instrument.query('*OPC?')
    instrument.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=r'{Fil}'.format(Fil=File)))
    instrument.query('*OPC?')



def AtS(instrument,id,pulse_array0,AWG,marker,step):
    
    """ This 'Array to segment' takes np pulse arrays and exports them as csv files, then it loads these files to the instrument.

    The importing from np arrays into csv files is done with the CSV_PD function from Pulsefiles module.
    The loading of this new csv file into the instrument as a new segment is perfomed with the FileL function.
    'instrument' correspond to the visa resource instrument object associated with our Instrument.
    'id' corresponds to an positive integer, which will be the Segemet id within the Instrument.
    """
    #creating the csv file using CSV_PD function
    new_csv, SegMark = CSV_PD(pulse_array0, AWG, marker ,step)

    #sending the csv file to the instrument
    FileL(instrument, new_csv, id)
    print('Current Segment Catalogue is {g}  [(segment id, Segment size)]'.format(g = instrument.query('TRAC:CAT?')))

    return new_csv, SegMark






def SeqF(instrument,file0,file1,loop):

    """ Creates a sequence in the instrument by the data in file0 and file1 csv files.

    This function first calls the FileL function to load the file0 and file1 csv files data files as segments into the instrument.
    It then uses the AWG's SEQ subsystem to create a sequence from this two segments.This sequence is set to 1 loop count, auto advance mode
    and starting and ending address correspond to the first and last value of the data files.
    The SCPI query SEQ:DEF:NEW? returns the Sequence Id. as a string and this functions returns it as an int.
    """
    FileL(instrument, file0, 1)
    FileL(instrument, file1, 2)

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
    
    instrument.write('FUNC1:MODE STS')
    instrument.write('STAB1:SEQ:SEL {t}'.format(t = seq_id))

    print('Sequence loaded with the following segment data "{b}"'.format(b = instrument.query('SEQ1:DATA? {c},0,2'.format(c=seq_id))))

    return seq_id


def AtSeq(instrument,pulse_array0,pulse_array1,AWG,step,loop):

    """This function loads 2 numpy pulse data arrays into a sequence in the AWG

    It utilises first the AtS function to creat th CSV files from the pulse_array0/1 numpy arrays
    and then it imports them as segments to the AWG using the SeqF function
    It outputs the sequence id of the newly define sequence, and the data frame of the segments.
    """

    #Creating cvs files and loading them to the AWG
    c, datac= AtS(instrument, 1, pulse_array0, AWG, 1, step)
    b, dataB= AtS(instrument, 2,pulse_array1, AWG, 0, step)
    
    #Importing the csv files to the AWG
    seqid= SeqF(instrument, c, b, loop)


    return seqid, datac, dataB 
  










