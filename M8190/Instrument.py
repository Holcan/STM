import numpy as np
import pandas as pd
from Sweeping import *
from Dictionaries import * 
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
    inst = rm.open_resource('{visa}'.format( visa = AWG['Visa_Resource_Name']))
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
    instrument.write('OUTP1:ROUT DC') #setting the output to DC 
    instrument.write('OUTP1 ON') #activating the output "Amp Out"
    instrument.write('DC1:VOLT:AMPL {volt}'.format(volt = AWG['Voltage Amplitude']/1000)) #Setting voltage amplitude
    instrument.write('FREQ:RAST {sr}'.format(sr = AWG['Clock Sample Frecuency']))  #Setting the sample rate
    #print(instrument.query('FREQ:RAST?'))
    print('Instruments Sampling Frecuency set to {a}Hz'.format(a = instrument.query('FREQ:RAST?')))
    print('Instruments DC1 Output Voltage set to {V}deciVolts'.format(V = instrument.query('DC1:VOLT:AMPL?')))

def FileL(instrument,File,id):

    """
    This functions loads the csv file "File" into the AWG as a Segment whose Id is id.

    """
    inst.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=r'{Fil}'.format(Fil=File)))
    inst.query('*OPC?')



def AtS(instrument,id,pulse_array0,AWG,marker,step):
    
    """ This 'Array to segment' takes np pulse arrays and exports them as csv files, then it loads this files to the instrument.
    
        'instrument' correspond to the visa resource instrument object associated with our Instrument.
        'id' corresponds to an positive integer, which will be the Segemet id within the Instrument.
        'pulse_array0' should be the np array with the data of our pulse scheme.
        'AWG' should be a dictionary, whose 'Voltage Amplitude' key is used to normalize the csv data (since the instrument only takes values from -1 to 1).
        'marker' should be either 1 or 0, it assigns the given marker to the csv file.
        'step' corresponds to the sweeping step of the Sweeping function.
    """
    #normalizing the data
    pulse_array = pulse_array0/AWG['Voltage Amplitude']
    Seg = pd.DataFrame( pulse_array,columns=['Y1'] )

    #marker assignement
    if marker == 0:
        Markers = pd.DataFrame(np.zeros((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])
        segment = 'B' 

    if marker == 1:
        Markers = pd.DataFrame(np.ones((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])
        segment = 'A'

    #Appending the markers
    SegMark = pd.concat([Seg,Markers],axis = 1)

    #string for the new csv file location
    new_csv = r'{File_Location}\Segment{seg}_{n}_{nm}.csv'.format(File_Location = AWG['Data Directory'],seg=segment,n=len(pulse_array),nm=step)

    #exporting the data frame
    SegMark.to_csv(new_csv,index=False)

    #sending the csv file to the instrument
    instrument.write('TRAC1:IQIM {segmentid}, "{a}", CSV, BOTH, ON, ALEN'.format(segmentid= id,a=new_csv))
    instrument.query('*OPC?')

    return SegMark


def Seq(instrument,pulse_array0,pulse_array1,AWG,step):

    """ Sequences only for segment slots 1,2


    """
    #Creating cvs files and loading them to the AWG
    segmentA= AtS(instrument,1,pulse_array0,AWG,1,step)
    segmentB= AtS(instrument,2,pulse_array1,AWG,0,step)

    #Defining new sequence
    instrument.query('SEQ1:DEF:NEW? 2')


    HERE
    #loading sequences to the Instrment has the following syntaxis:
    #instrument.write('[:SOURce]:SEQuence[1|2]:DATA <sequence_id>, <step> ,[<value>,<value>,…|<data block>] <segment_id>, <loop_count>,<advance_mode>,<marker_enable>, <start_addr>,<end_addr>

    #instrument.write('SEQ1:DATA 0,0,1,1,0,1,0,#hFFFFFFFF'.format())

    #Loading Segment 1 to step 0 of Sequence 0
    #instrument.write('SEQ1:DATA 0,0,1,1,0,1,0,#hFFFFFFFF')

    #Loading Segment 2 to step 1 of Sequence 0
    #instrument.write('SEQ1:DATA 0,1,2,1,0,1,0,#hFFFFFFFF')

  