import numpy as np
import time
from time import sleep
from numpy.lib.function_base import average
import pandas as pd
from Sweeping import *
from Dictionaries import * 
from PulseFiles import *
import pyvisa as visa
from datetime import date
import nidaqmx
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType

#The functions within this module are used to interact with the instrument. From initializing settings to loading segments and sequences into it.

def VisaR(AWG_Settings_Dict,time):

    """ This function sets the pyvisa interface and sets the timeout time.

    This function enables the interaction between the computer and the instrument, throught the pyvisa module.
    Before running this function, please make sure that the AgM8190 Firmware is properly initialized.
    The Visa Address is given by corresponding key in the AWG_Settings_Dict dictionary.
    The time should be given in miliseconds.
    It prints the instruments manufacturer, model, serial number.
    It outputs the instruments pyvisa resource object
    """
    rm = visa.ResourceManager()
    inst = rm.open_resource('{visa}'.format( visa = AWG_Settings_Dict['Visa Resource Name']))
    inst.read_termination = '\n'
    inst.write_termination = '\n'
    inst.timeout = time
    return inst

def Instrument_Settings(instrument):
    
    """This function  returns a .txt file with the current instrument settings
    """

    f=open("Settings_{dt}.txt".format(dt = date.today()),"w+")
    f.write("{settings}".format( settings= instrument.query('SYST:SET?')))
    f.close()


def Initialization(instrument,AWG_Settings_Dict):

    """This function sets the initialization of the instrument, using the keys of the AWG_Settings_Dict dictionary.

        Instruments output rout is given by the 'Output Route' key, voltage by 'Voltage Amplitude' and sampling frequency by 'Clock Sample Frecuency'.
        
    """
    instrument.write('INST:COUP:STAT 0') #Decoupling the channels
    instrument.query('*OPC?')
    instrument.write('OUTP:ROUT:SEL {route}'.format( route = AWG_Settings_Dict['Output Rout'])) #setting the output route to the one given by the AWG_Settings_Dict dictionary, keysight technicians recomend DC or DAC, since AC has poor spectral performance 
    instrument.query('*OPC?')
    instrument.write('OUTP1 ON') #activating the output rout.
    instrument.query('*OPC?')
    instrument.write('{route}1:VOLT:AMPL {volt}'.format(volt = AWG_Settings_Dict['Voltage Amplitude']/1000,route = AWG_Settings_Dict['Output Rout'])) #Setting Normilized Voltage amplitude
    instrument.query('*OPC?')
    instrument.write('FREQ:RAST {sr}'.format(sr = AWG_Settings_Dict['Clock Sample Frecuency']))  #Setting the sample rate
    instrument.query('*OPC?')
    instrument.write('ARM:TRIG:LEV {vol}'.format(vol = AWG_Settings_Dict['Trigger In Threshold'] ))#Setting triggering threshold value
    instrument.query('*OPC?')
    instrument.write('ARM:TRIG:IMP HIGH') #triggering channel impedance
    instrument.query('*OPC?')
    instrument.write('SOUR:MARK1:SYNC:VOLT:AMPL 0.17') #Voltage Amplitude for the Sync Mrk Out 1 channel, it has a weird behavior, gives 2.04 V of amplitude
    instrument.write('SOUR:MARK1:SYNC:VOLT:OFFS 0.01') #Voltage Offset for theSync Mrk Out 1 channel, it has a weird behavior
    instrument.write(':SOUR:MARK1:SAMP:VOLT:AMPL 0.17') #Voltage Amplitude for the Sample Marker 1 channel, it was a weir behaviour
    instrument.write(':SOUR:MARK1:SAMP:VOLT:OFFS 0.01') #Voltage Offset for the Sample Marker 1 channel, it was a weir behaviour
    
    #Initializing the Sequence Function Mode
    instrument.write('INIT:GATE1 0')
    instrument.write('INIT:CONT1 0')
    instrument.write('FUNC1:MODE {mode}'.format( mode = AWG_Settings_Dict['Mode']))
    instrument.write(':DAC1:VOLT:OFFS 0.00{value}'.format(value = 3 ))
    instrument.query('*OPC?')

    
    print('Instruments Sampling Frecuency set to {a}Hz'.format(a = instrument.query('FREQ:RAST?')))
    print('Instruments Direct Out {route} Output route Voltage set to {V}Volts'.format(route = AWG_Settings_Dict['Output Rout'] ,V = instrument.query('DAC:VOLT:AMPL?'))) #hard coded which voltage amplitude is returned by the print, must put format within it to call on the value of the dictionary key
    print('AWG_Settings_Dict set to TRIGGERED Mode')
    print('Trigger In threshold value set to {a}V'.format(a = instrument.query('ARM:TRIG:LEV?')))

def Segment_File(instrument,File,id):

    """
    This functions loads the csv file "File" into the instrument as a Segment with the corresponding id.

    This function uses the TRAC Subsystem of the instrument, alongside with SCPI. The instrument may create a segment whose length is larger than the given data size to
    account for the granularity (it must be a multiple of 480), if the given data does not match the granularity, multiple segments will be displayed.
    to fullfil this condition.
    """

    #precision mode for now, vector size in samples is multiple of 48
    instrument.write('TRAC1:DWID WPR')
    instrument.query('*OPC?')
    instrument.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=r'{Fil}'.format(Fil=File)))
    #instrument.write('TRAC1:ADV COND')
    instrument.query('*OPC?')



def Segment_Array(instrument,id,pulse_array0,AWG_Settings_Dict,marker,step):
    
    """ This function takes np pulse arrays as imput and exports them as csv files, then it loads these files to the instrument as segments.

    The importing from np arrays into csv files is done with the CSV_PD function from Pulsefiles module.
    The loading of this new csv file into the instrument as a new segment is perfomed with the Segment_File function.
    'instrument' correspond to the visa resource instrument object associated with our Instrument.
    'id' corresponds to an positive integer, which will be the Segemet id within the Instrument.
    """
    #creating the csv file using CSV_PD function
    new_csv, SegMark = CSV_PD(pulse_array0, AWG_Settings_Dict, marker ,step)

    #sending the csv file to the instrument
    Segment_File(instrument, new_csv, id)
    print('Current Segment Catalogue is {g}  [(segment id, Segment size)]'.format(g = instrument.query('TRAC:CAT?')))

    return new_csv, SegMark


def Def_Sequence(instrument,loop):

    """This function defines a new Sequence in the instrument and outputs the sequence id.

    The new sequence will have 2 steps, and will only load the two corresponding segments
    that must be prevoiusly defined and loaded in th instrument (either by hand, or with the Segment functions
    in this module).
    The Sequence will have a length of 2, it is specifically designed for creating sequences with segments.
    The table entries will set the advancement mode to Conditional.
    """


    #Defining new sequence, The SCPI query SEQ:DEF:NEW? returns the Sequence Id. as a string and this functions returns it as an int.
    seq_id = int(instrument.query('SEQ1:DEF:NEW? 2'))
    #instrument.write('SEQ:ADV {seqid},REP'.format(seqid = seq_id))


    #loading segments into sequences within the Instrment has the following syntaxis:
    #instrument.write('[:SOURce]:SEQuence[1|2]:DATA <sequence_id>, <step> , <segment_id>, <loop_count>,<advance_mode>,<marker_enable>, <start_addr>,<end_addr>

    #Loading Segment 1 to step 0 of Sequence 0
    instrument.write('SEQ1:DATA {seqid},0,1,{l},0,1,0,#hFFFFFFFF'.format(seqid = seq_id, l =loop))
    instrument.query('*OPC?')

    #Loading Segment 2 to step 1 of Sequence 0
    instrument.write('SEQ1:DATA {seqid},1,2,{l},0,1,0,#hFFFFFFFF'.format(seqid = seq_id, l = loop))
    instrument.query('*OPC?')
    
    instrument.write('SEQ:ADV {seqid}, COND'.format(seqid = seq_id)) #advancement condition
    instrument.query('*OPC?')
    #print('Sequence advancement method is {met}'.format(met = instrument.query('SEQ:ADV? 0')))
    
    instrument.write('STAB1:SEQ:SEL {t}'.format(t = seq_id))
    instrument.query('*OPC?')

    print('Sequence loaded with the following segment data "{b}"'.format(b = instrument.query('SEQ1:DATA? {c},0,2'.format(c=seq_id))),'and the advancement method is {met}'.format(met = instrument.query('SEQ:ADV? 0')))

    return seq_id


def Sequence_File(instrument,file0,file1,loop):

    """ Creates a sequence in the instrument by the data in file0 and file1 csv files.

    This function first calls the Def_Sequence function to load the file0 and file1 csv data files as segments into the instrument.
    It then uses the instrument's SEQ subsystem to create a sequence from this two segments.This sequence is set to have "loop" loop count, auto advance mode
    and starting and ending address correspond to the first and last value of the data files.
    
    """
    Segment_File(instrument, file0, 1)
    Segment_File(instrument, file1, 2)

    #Define the corresponding Sequence:
    seq_id = Def_Sequence(instrument,loop)
    return seq_id

def Sequence_Array(instrument,pulse_array0,pulse_array1,AWG_Settings_Dict,step,loop):

    """This function loads 2 numpy pulse data arrays into a sequence in the instrument

    It utilizes first the Segment_Array function to import as segments the CSV files corresponding to 
    the pulse_array0/1 numpy arrays. Then it imports them as sequence to the instrument using the Sequence_File function.
    It outputs the sequence id of the newly define sequence, and the data frame of the segments.
    pulse_array0 will have marker values = 1 and pulse_array1 will have marker values = 0.
    """

    #Creating cvs files and loading them to the instrument as segments
    c, datac= Segment_Array(instrument, 1, pulse_array0, AWG_Settings_Dict, 1, step)
    b, dataB= Segment_Array(instrument, 2,pulse_array1, AWG_Settings_Dict, 0, step)
    
    #Creating the Sequence within the Instrument
    seqid= Def_Sequence(instrument,loop)


    return seqid, datac, dataB 
  


def Sequence_Pulse_List(PulseList1,PulseList2,P,p,t,N,instrument,AWG_Settings_Dict,loop):

    """This function takes pulse sequences lists as imput and with the given parameters loads them into the instrument at sweeping step p.

    This function combines the Sweep function with the Sequence_array function.
    """

    #creating the numpy array from the PulseList1
    pulses1,time = Sweep(PulseList1,P,p,t,N)

    #creating the numpy array from the PulseList2
    pulses2, time = Sweep(PulseList2,P,p,t,N)

    #Loading the pulse numpy arrays into a sequence in the instrument.
    seqid, dataframepulses1, dataframepulses2 = Sequence_Array(instrument,pulses1,pulses2,AWG_Settings_Dict,p,loop)

    return seqid, dataframepulses1, dataframepulses2, time





def Sequence_Loader_File(instrument,LocationA,LocationB,loop,sleeptime):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence. FOR SWEEPING

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
    "sleeptime" is the time that the function waits before loading the next sequence, it is in seconds.
    """
    

    for i,j in zip(LocationA, LocationB):
        Sequence_File(instrument,LocationA[i],LocationB[j],loop)
        instrument.query('*OPC?')
        instrument.write('INIT:IMM')
        sleep(sleeptime)
        instrument.write('ABOR')

    instrument.write('ABOR')
   

def Sequence_Loader_File_Dummy(instrument,LocationA,LocationB,loop,sleeptime,N,start,AWG_Settings_Dict):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence.

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
    "sleeptime" is the time that the function waits before loading the next sequence, it is in seconds.
    Includes dummy run to avoid loading time
    """

    #instrument.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=r'{Fil}'.format(Fil=File)))

    #strnng for the file location of the dummy sequence
    strnga=r'{directory}\SegmentA_{a}_{b}.csv'.format(directory = AWG_Settings_Dict['Data Directory'], a=N, b= start)
    strngb=r'{directory}\SegmentB_{a}_{b}.csv'.format(directory = AWG_Settings_Dict['Data Directory'], a=N, b= start)

    #dummy loading 
    Sequence_File(instrument,'{sega}'.format(sega=strnga),'{segb}'.format(segb=strngb),1)
    instrument.query('*OPC?')
    instrument.write('INIT:IMM')
    sleep(sleeptime)
    instrument.write('ABOR')
    print('Dummy Segment loading ended')


    for i,j in zip(LocationA, LocationB):
        Sequence_File(instrument,LocationA[i],LocationB[j],loop)
        instrument.query('*OPC?')
        instrument.write('INIT:IMM')
        sleep(sleeptime)
        instrument.write('ABOR')

    instrument.write('ABOR')

  
def Sequence_File_List(PulseList1,PulseList2,P,t,N,start,stop,AWG_Settings_Dict):

    """ Given two pulse schemes lists, this functions iterates the pulse scheme from start to stop.

        This function firts creates the corresponding pulse sequence data given the PulseLists using the Sweep_iteration_csv function
        
    """

    #SegmentA of the sequence
    Loc1,DF1,timm = Sweep_Iteration_CSV_List(PulseList1,P,t,N,start,stop,AWG_Settings_Dict,1)

    #SegmentB of the Sequence
    Loc2,DF2,timm = Sweep_Iteration_CSV_List(PulseList2,P,t,N,start,stop,AWG_Settings_Dict,0)

    return Loc1, Loc2, DF1,DF2,timm


def Sequence_Loader_List(PulseList1,PulseList2,P,t,N,start,stop,instrument,AWG_Settings_Dict,loop,sleeptime):

    """ Given two pulse schemes lists, this functions iterates over them from start to stop and loads the corresponding sequence to the instrument

        This function firts creates the corresponding pulse sequence data given the PulseLists using the Sweep_iteration_csv function
        it thens loads them sequentially into the instrument using the Sequence_Loader_File function.
    """

    #SegmentA of the sequence
    Loc1,DF1,timm = Sweep_Iteration_CSV_List(PulseList1,P,t,N,start,stop,AWG_Settings_Dict,1)

    #SegmentB of the Sequence
    Loc2,DF2,timm = Sweep_Iteration_CSV_List(PulseList2,P,t,N,start,stop,AWG_Settings_Dict,0)


    #Loading the sequence iteratively into the instrument
    Sequence_Loader_File(instrument, Loc1, Loc2, loop, sleeptime)

    return DF1,DF2,timm





def Sequence_Loader_List_D(PulseList1,PulseList2,P,t,N,start,stop,instrument,AWG_Settings_Dict,loop,sleeptime):

    """ Given two pulse schemes lists, this functions iterates over them from start to stop and loads the corresponding sequence to the instrument

        This function firts creates the corresponding pulse sequence data given the PulseLists using the Sweep_iteration_csv function
        it thens loads them sequentially into the instrument using the Sequence_Loader_File function.
    """

    #SegmentA of the sequence
    Loc1,DF1,timm = Sweep_Iteration_CSV_List(PulseList1,P,t,N,start,stop,AWG_Settings_Dict,1)

    #SegmentB of the Sequence
    Loc2,DF2,timm = Sweep_Iteration_CSV_List(PulseList2,P,t,N,start,stop,AWG_Settings_Dict,0)


    #Loading the sequence iteratively into the instrument
    Sequence_Loader_File_Dummy(instrument,Loc1,Loc2,loop,sleeptime,N,start,AWG_Settings_Dict)

    return DF1,DF2,timm

def Trigger_Pulse(daq,channel,amp,duration):
    """This function generates a constant voltage pulse, with amplitude amp, over the time duration with the DAQ Box.
    
    This uses the nidaqmx API for interacting with the NI DAQ box, after the time duraion ends, the voltage amplitude is set to 0
    The name of the DAQ box (daq) as well as the channel must be provided. Maximum amp value is 4
    """
    trig_task =  nidaqmx.Task()
    trig_task.ao_channels.add_ao_voltage_chan('{a}/{b}'.format(a = daq, b = channel),'triggering',-4,4)
    trig_task.start()

    trig_task.write(amp)
    time.sleep(duration)
    trig_task.stop()
    
    trig_task.start()
    trig_task.write(0)
    print('Triggering Pulse Stopped')

    trig_task.stop()
    trig_task.close()


def Trigger_Segment1(instrument,file_location,segid,DAQ,channel,voltage,playingtime):
    """This function will load one segment to the instrument and set it up to triggered mode, then it will start it, trigger it and stop it. Whole duration of this will be
        given by the sleep parameter.
        
        This function calls the Segment_File function and the Trigger_Pulse function.
    """
    #loading the segment to instrument
    Segment_File(instrument,'{loc}'.format(loc = file_location),segid)

    #Setting up the triggering settings
    instrument.write('TRAC:SEL {id}'.format(id = segid))
    instrument.write('TRAC:ADV COND')
    instrument.write('INIT:GATE1 0')
    instrument.write('INIT:CONT1 0')
    instrument.write('ARM:TRIG:IMP HIGH')
    instrument.write('ARM:TRIG:LEV {vol}'.format(vol = voltage - 0.5))
    instrument.query('*OPC?')
    instrument.write('INIT:IMM')

    #Setting up the triggering voltage from the DAQ
    time.sleep(10)
    Trigger_Pulse('{daq}'.format(daq = DAQ),'{chn}'.format(chn = channel),voltage,11)

    #setting instrument playing time
    time.sleep(playingtime)
    instrument.write('ABOR')

def Sequence_Triggered(Pulse_ListA,Pulse_ListB,P,p,t,N,instrument,AWG_Settings_Dict,loop,DAQ,channel,voltage,playingtime):
    """This functions has the set up parameters to put the instrument in Triggered mode, it then creates and loads the pulse schemes into the 
        instrument, it then sets up the DAQ parameters to trigger the instrument for a given duration of time
    """
    #loading the segment to instrument
    seqid, dataframepulses1, dataframepulses2, timee = Sequence_Pulse_List(Pulse_ListA,Pulse_ListB,P,p,t,N,instrument,AWG_Settings_Dict,loop)


    #Setting up the triggering settings
    
    instrument.write('INIT:GATE1 0')
    instrument.write('INIT:CONT1 0')
    instrument.write('ARM:TRIG:IMP HIGH')
    instrument.write('ARM:TRIG:LEV {vol}'.format(vol = voltage - 0.5))
    instrument.query('*OPC?')
    instrument.write('INIT:IMM')

    #Setting up the triggering voltage from the DAQ
    time.sleep(10)
    print('Triggering Pulse Started')
    Trigger_Pulse('{daq}'.format(daq = DAQ),'{chn}'.format(chn = channel),voltage,11)
    print('Triggering Pulse Stopped')

    #setting instrument playing time
    time.sleep(playingtime)
    print('Sequence Stopped')
    instrument.write('ABOR')

    return dataframepulses1, dataframepulses2, timee



def Triggered_Sequence_Setup(Pulse_ListA,Pulse_ListB,P,p,t,N,instrument,AWG_Settings_Dict,loop):
    """Given a pulse scheme, this function loads it into the instrument and enables it to recieve a trigger in order to play
       the correspondent wave function.

        The function first calls the Sequence_Pulse_List function to load the pulse scheme into the instrument, then it configures 
        the corresponding instrument subsystem settings to set it up to trigger mode.

        Voltage is the voltage parameter given in volts, the maximum values for safe operations are -10V and 10V.

        The funciton returns the dataframes of the pulses in the sequence, and the time interval for them
    """
    #loading the segment to instrument
    seqid, dataframepulses1, dataframepulses2, timee = Sequence_Pulse_List(Pulse_ListA,Pulse_ListB,P,p,t,N,instrument,AWG_Settings_Dict,loop)


    #Setting up the triggering settings
    
    #instrument.write('INIT:GATE1 0')
    #instrument.write('INIT:CONT1 0')
    #instrument.query('*OPC?')
    #instrument.write('INIT:IMM')
    #instrument.query('*OPC?')
    #print('AWG initialized')



    return dataframepulses1, dataframepulses2, timee




def DAQ_Measuringhalf(DAQ_settings,playingtime):
    """This function starts sets up the DAQ box in order to collect data for a time duration given by "playing time"
      It then uses the DAQ box to trigger the instrument into playing a waveform.

      playingtime should be in seconds.
      
    """
    #Calculating the number of samples given the samplig frecuency and playying time
    samples = DAQ_settings['Sampling Frequency'] * playingtime 
    time = np.linspace(0,playingtime,int(samples))

    #setting the measuring task
    measuring_task = nidaqmx.Task()
    
    #voltage measuring channel
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Voltage'],max_val= DAQ_settings['Maximum Voltage'])

    #Sampling configuration
    measuring_task.timing.cfg_samp_clk_timing(DAQ_settings['Sampling Frequency'], source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=int(samples))

    measuring_task.start()

    data = np.array(measuring_task.read(int(samples,timeout=50.0)))

    measuring_task.stop()
    measuring_task.close()

    return data,time
    

def DAQ_Measuringms(DAQ_settings,sr,playingtime,instrument):
    """This function starts sets up the DAQ box in order to collect data for a time duration given by "playing time"
      It then uses the DAQ box to trigger the instrument into playing a waveform.

      playingtime should be in seconds.
      triggerinvoltage should be in volts.
    """
    instrument.write('INIT:IMM')
    time.sleep(5)



    #Calculating the number of samples given the samplig frecuency and playing time
    samples = int(sr * playingtime*1e-3) 
    measuring_time = np.linspace(0,playingtime,samples)

    #setting the tasks
    measuring_task = nidaqmx.Task()
    trig_task =  nidaqmx.Task()
   


    #Channels Configuration
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Voltage'],max_val= DAQ_settings['Maximum Voltage'])
    trig_task.ao_channels.add_ao_voltage_chan('{a}/{b}'.format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Output']),'triggering',-4,4)

    #Sampling configuration measuring channel
    measuring_task.timing.cfg_samp_clk_timing(sr, active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=samples)
    #trig_task.timing.cfg_samp_clk_timing(DAQ_settings['Sampling Frequency'], samps_per_chan=samples)
    #source = "measuring_task/SampleClock"

    trig_task.start()
    measuring_task.start()
    

    
    trig_task.write(1.5)
    #time.sleep(3)
    data = np.array(measuring_task.read(samples,timeout=50.0))


    
    #time.sleep(3)
    print('Triggering Pulse Stoped')
    trig_task.write(0)

    
    
    

    trig_task.stop()
    measuring_task.stop()

    measuring_task.close()
    trig_task.close()


    instrument.write('ABOR')

    return data, measuring_time


def DAQ_Measuring(DAQ_settings,sr,playingtime,instrument):
    """This function starts sets up the DAQ box in order to collect data for a time duration given by "playing time"
      It then uses the DAQ box to trigger the instrument into playing a waveform.

      playingtime should be in seconds.
      triggerinvoltage should be in volts.
    """
    instrument.write('INIT:IMM')
    time.sleep(5)


    #Calculating the number of samples given the samplig frecuency and playing time
    samples = int(sr * playingtime) 
    measuring_time = np.linspace(0,playingtime,samples)

    #setting the tasks
    measuring_task = nidaqmx.Task()
    trig_task =  nidaqmx.Task()
   


    #Channels Configuration
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Voltage'],max_val= DAQ_settings['Maximum Voltage'])
    trig_task.ao_channels.add_ao_voltage_chan('{a}/{b}'.format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Output']),'triggering',-4,4)

    #Sampling configuration measuring channel
    measuring_task.timing.cfg_samp_clk_timing(sr, samps_per_chan=samples)
    #trig_task.timing.cfg_samp_clk_timing(DAQ_settings['Sampling Frequency'], samps_per_chan=samples)
    #source = "measuring_task/SampleClock"

    trig_task.start()
    measuring_task.start()
    

    
    trig_task.write(1.5)
    #time.sleep(3)
    data = np.array(measuring_task.read(samples,timeout=50.0))


    
    #time.sleep(3)
    print('Triggering Pulse Stoped')
    trig_task.write(0)

    
    
    

    trig_task.stop()
    measuring_task.stop()

    measuring_task.close()
    trig_task.close()


    instrument.write('ABOR')

    return data, measuring_time

#miliseconds

def Sequence_Loader_File_DAQ_dictionaryms(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence and measures them withthe daq, for ms segime output is dictionary

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
 
    """
    #measurement_data = np.zeros(2,len(fileA))
    measurement_data = {}



    for i,j in zip(fileA, fileB):
        Sequence_File(instrument,fileA[i],fileB[j],1)
        measurement_data['Data for step {a}'.format(a =i)], measurement_data['Time interval step {a}'.format(a =i)] = DAQ_Measuringms(DAQ_settings,sampling_rate,playingtime,instrument)
        #measurement_data['Time interval step {a}'.format(a =i)] = DAQ_Measuringms(DAQ_settings,sampling_rate,playingtime,instrument)[1]
        #instrument.write('INIT:IMM')
        #time.sleep(2)
        #instrument.query('*OPC?')
        #measurement_data['data result for step {a}and{b}'.format(a =i, b = j)] = DAQ_Measuringmsl(DAQ_settings,sampling_rate,playingtime,instrument)
        instrument.write('ABOR')

    return measurement_data
#miliseconds

def Sequence_Loader_File_DAQms_np(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence and measures them withthe daq, for ms segime output is numpy array

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
 
    """
    measurement_data = np.zeros((len(fileA),2),  dtype=object)
    #measurement_data = {}

    for i,j,k in zip(fileA, fileB,range(0,len(fileA))):
        Sequence_File(instrument,fileA[i],fileB[j],1)
        measurement_data[k][0], measurement_data[k][1] = DAQ_Measuringms(DAQ_settings,sampling_rate,playingtime,instrument)
        print('Data acquired for Step {step}'.format(step = k ))
        #instrument.write('ABOR')

    return measurement_data
    
def Sequence_Loader_File_DAQ_dictionary(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence and measures them withthe daq, for ms segime output is dictionary

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
 
    """
    #measurement_data = np.zeros(2,len(fileA))
    measurement_data = {}



    for i,j in zip(fileA, fileB):
        Sequence_File(instrument,fileA[i],fileB[j],1)
        measurement_data['Data for step {a}'.format(a =i)], measurement_data['Time interval step {a}'.format(a =i)] = DAQ_Measuring(DAQ_settings,sampling_rate,playingtime,instrument)
        #measurement_data['Time interval step {a}'.format(a =i)] = DAQ_Measuringms(DAQ_settings,sampling_rate,playingtime,instrument)[1]
        #instrument.write('INIT:IMM')
        #time.sleep(2)
        #instrument.query('*OPC?')
        #measurement_data['data result for step {a}and{b}'.format(a =i, b = j)] = DAQ_Measuringmsl(DAQ_settings,sampling_rate,playingtime,instrument)
        instrument.write('ABOR')

    return measurement_data

def Sequence_Loader_File_DAQ_np(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB):
    
    """ This function loads the csv data files from the Location dictionaries into the instrument as a sequence and measures them withthe daq, for ms segime output is numpy array

    LocationA is a dictionary, whose elements are the file paths to the csv files that are going to be loaded as SegmentA into the sequence.
    LocationB is a dictionary, whose elemnts re the filepaths to the csv files that are going to be loaded as SegmentB into the sequence
    It uses the Sequence_File function to load the csv files to the instrument.
 
    """
    measurement_data = np.zeros((len(fileA),2),  dtype=object)
    #measurement_data = {}

    for i,j,k in zip(fileA, fileB,range(0,len(fileA))):
        Sequence_File(instrument,fileA[i],fileB[j],1)
        measurement_data[k][0], measurement_data[k][1] = DAQ_Measuring(DAQ_settings,sampling_rate,playingtime,instrument)
        print('Data acquired for Step {step}'.format(step = k ))
        #instrument.write('ABOR')

    return measurement_data

def DAQ_Measuring_Markers(DAQ_settings,sr,playingtime,instrument):

    """This function starts sets up the DAQ box in order to collect data for a time duration given by "playing time"
      It then uses the DAQ box to trigger the instrument into playing a waveform.

      playingtime should be in seconds.
      triggerinvoltage should be in volts.
    """
    #Calculating the number of samples given the samplig frecuency and playing time
    samples = int(sr * playingtime) 
    measuring_time = np.linspace(0,playingtime,samples)

    instrument.write('INIT:IMM')
    time.sleep(5)

    #setting the tasks
    measuring_task = nidaqmx.Task()
    trig_task =  nidaqmx.Task()
    #current_tast = nidaqmx.Task()

    #current_tast.ai_channels.add_ai_current_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Current'],max_val=DAQ_settings['Maximum Current'], units=CurrentUnits.AMPS)


    #Channels Configuration
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Voltage'],max_val= DAQ_settings['Maximum Voltage'])
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Marker']),min_val=DAQ_settings['Minimum Voltage Marker'],max_val= DAQ_settings['Maximum Voltage Marker'])
    trig_task.ao_channels.add_ao_voltage_chan('{a}/{b}'.format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Output']),'triggering',-4,4)

    #Sampling configuration measuring channel
    measuring_task.timing.cfg_samp_clk_timing(sr, samps_per_chan=samples)
    #trig_task.timing.cfg_samp_clk_timing(DAQ_settings['Sampling Frequency'], samps_per_chan=samples)
    #source = "measuring_task/SampleClock"

    trig_task.start()
    measuring_task.start()
    

    
    trig_task.write(1.5)
    #time.sleep(3)
    data = np.array(measuring_task.read(samples,timeout=50.0))


    
    #time.sleep(3)
    print('Triggering Pulse Stoped')
    trig_task.write(0)

    
    
    

    trig_task.stop()
    measuring_task.stop()

    measuring_task.close()
    trig_task.close()


    instrument.write('ABOR')

    return data, measuring_time




def DAQ_Measuring_Markersms(DAQ_settings,sr,playingtime,instrument):
    """This function starts sets up the DAQ box in order to collect data for a time duration given by "playing time"
      It then uses the DAQ box to trigger the instrument into playing a waveform.

      This DAQ maximum sampling rate of 400 KS/s for a single channel.  If you have more than 1 channel this max rate will decrease.
      For example for 5 channels you will have a max sampling rate of 50 kS/s.


      playingtime should be in seconds. it will be converted to mili seconds
      triggerinvoltage should be in volts.
    """
    #Calculating the number of samples given the samplig frecuency and playing time
    samples = int(sr * playingtime*1e-3) 
    measuring_time = np.linspace(0,playingtime,samples)

    instrument.write('INIT:IMM')
    time.sleep(5)

    #setting the tasks
    measuring_task = nidaqmx.Task()
    trig_task =  nidaqmx.Task()
    #current_tast = nidaqmx.Task()

    #current_tast.ai_channels.add_ai_current_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Current'],max_val=DAQ_settings['Maximum Current'], units=CurrentUnits.AMPS)


    #Channels Configuration
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Waveform']),min_val=DAQ_settings['Minimum Voltage'],max_val= DAQ_settings['Maximum Voltage'])
    measuring_task.ai_channels.add_ai_voltage_chan("{a}/{b}".format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Input Marker']),min_val=DAQ_settings['Minimum Voltage Marker'],max_val= DAQ_settings['Maximum Voltage Marker'])
    trig_task.ao_channels.add_ao_voltage_chan('{a}/{b}'.format(a = DAQ_settings['DAQ Name'], b = DAQ_settings['Analog Channel Output']),'triggering',-4,4)

    #Sampling configuration measuring channel
    measuring_task.timing.cfg_samp_clk_timing(sr, samps_per_chan=samples)
    #trig_task.timing.cfg_samp_clk_timing(DAQ_settings['Sampling Frequency'], samps_per_chan=samples)
    #source = "measuring_task/SampleClock"

    trig_task.start()
    measuring_task.start()
    

    
    trig_task.write(1.5)
    #time.sleep(3)
    data = np.array(measuring_task.read(samples,timeout=50.0))


    
    #time.sleep(3)
    print('Triggering Pulse Stoped')
    trig_task.write(0)

    
    
    

    trig_task.stop()
    measuring_task.stop()

    measuring_task.close()
    trig_task.close()


    instrument.write('ABOR')

    return data, measuring_time


def Sweeping_Single_List_File(PulseList,P,t,N,start,stop,AWG_Settings_Dict,cycle):

    """ Given a pulse scheme list, this functions iterates the pulse scheme from start to stop.

        This function firts creates the corresponding pulse sequence csv data given the PulseList using the Sweep_iteration_csv function
        
    """
    
    if cycle == 'A':
        #Markers for cycle A
        Loc1,DF1,timm = Sweep_Iteration_CSV_List(PulseList,P,t,N,start,stop,AWG_Settings_Dict,1)

    if cycle == 'B':
        #Markers for cycle B
        Loc1,DF1,timm = Sweep_Iteration_CSV_List(PulseList,P,t,N,start,stop,AWG_Settings_Dict,0)

    return Loc1, DF1, timm

def Sweeping_Single_List_File_teil(PulseList,P,t,N,start,stop,AWG_Settings_Dict,cycle):

    """ Given a pulse scheme list, this functions iterates the pulse scheme from start to stop.

        This function firts creates the corresponding pulse sequence csv data given the PulseList using the Sweep_iteration_csv function
        
    """
    
    if cycle == 'A':
        #Markers for cycle A
        Loc1,DF1,timm = Sweep_Iteration_CSV_List_teil(PulseList,P,t,N,start,stop,AWG_Settings_Dict,1)

    if cycle == 'B':
        #Markers for cycle B
        Loc1,DF1,timm = Sweep_Iteration_CSV_List_teil(PulseList,P,t,N,start,stop,AWG_Settings_Dict,0)

    return Loc1, DF1, timm



def Measurement_Autocorrelation_voltage(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB,location):
    """This function loads a sweeping sequence into the AWG, plays it and triggers it with the DAQ and afterwards records the values with the DAQ.


        The sweeping is performed with the Sequence_Loader_File_DAQ_no function, and the measurement data is storaged in the folder given by location.
        It stores the invidivual values for each sweep, as well as the averaged version after removing the Lock-In_Offset, which is the initial time in
        which the Lock In perfomrs weird measurements (negativa and oscilating values). The offset is given at 2.5 seconds.
    """

    Data = Sequence_Loader_File_DAQ_np(instrument,DAQ_settings,sampling_rate,playingtime,fileA,fileB)

    for i in range(0,len(Data)):
        np.savetxt(r'{loc}\diode_signal_step{stp}_{dur}daqtime_5ms.csv'.format(loc = location ,stp = i,dur = playingtime), Data[i][0], delimiter=',') 

    LockIn_Offset = np.zeros((len(Data)),  dtype=object)
    for i in range(0,len(Data)):
        LockIn_Offset[i] = Data[i][0][2500:] 

    averaged_data = np.array([np.average(i) for i in LockIn_Offset])
    np.savetxt(r'{loc}\averaged signal_31steps_{dur}sdaqtime.csv'.format(loc =location,dur = playingtime),averaged_data,delimiter=',')

    return averaged_data