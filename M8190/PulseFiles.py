import numpy as np
import pandas as pd
from Sweeping import *



def CSV_PD(pulse_array0,AWG,marker,step):
    
    """This funcion converts pulse segments numpy arrays into csv files and appends the markers. It outputs the file strng name and the DataFrame

        This function first normalizes pulse_array by the value of the voltage given in the settings 'Voltage Amplitude' AWG dictionary key.
        'marker' should be either 1 or 0, it assigns the given marker to the csv file. If marker is 1, file name will be labeled as "SegmentA..."
        if marker is 0, file name will be labeled as "SegmenttB..."
        'step' corresponds to the sweeping step of the Sweeping function.
        The csv file will have be named: Segment(A or B)_(number of data points)_(sweeping step) and its location will be the folder direction
        given by the dictionary key 'Data Directory' in the AWG dictionary.
    """
    #normalizing the array values
    pulse_array = pulse_array0/AWG['Voltage Amplitude']

    Seg = pd.DataFrame( pulse_array,columns=['Y1'] )

    #marker condition
    if marker == 0:
        Markers = pd.DataFrame(np.zeros((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])
        segment = 'B'

    if marker == 1:
        Markers = pd.DataFrame(np.ones((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])
        segment ='A'

    #Appending the markers    
    SegMark = pd.concat([Seg,Markers],axis = 1)

    #string for the new csv file location
    new_csv = r'{File_Location}\Segment{seg}_{n}_{nm}.csv'.format(File_Location = AWG['Data Directory'],seg=segment,n=len(pulse_array),nm=step)

    #exporting the data frame to csv
    SegMark.to_csv(new_csv, index= False)

    return new_csv, SegMark


def Sweep_Iteration_CSV0(pultau,AWG,segment,start):

#I should rename this function.

    """ This function produces the corresponging normalized CSV files given by the entries of the pultau array.

        This function is a generalize version of the CSV_PD function, and it works for the Pulse arrayes 
        given by the Sweep_Iteration function.
        It uses the CSV_PD function to produce the CSV files asociated to each sweeping iteration.
        It outputs 2 dictionaries: the StrngName and the DataFrames dictionary.
        The StrngName dictionary has the csv files directory\name 's stored in the directory given by the corresponding AWG key.
        The DataFrames dictionary  has as elements the Data Frames asociated to the CSV files.  
    """

    DataFrames={}
    StrngName={}
    for i in range(len(pultau)):
        StrngName['File Location at step {step}'.format(step=i+start)],DataFrames['Data Frame Segment{seg}, data={val}, step{n}'.format( seg = segment ,val =len(pultau),n=i+start)] = CSV_PD(pultau[i],AWG,segment,i+start)

    return  StrngName,DataFrames

def Swep_Iteration_csv(PulList,P,t,N,start,stop,AWG,segment):
    
    """This function combinates the Sweep_Iteration function with the Sweep_Iteration_CSV0 function.

        Using the Sweep_Iteration function it creates numpy arrays corresponding to the pulse squemes at different sweep steps accordingly to the pulse Sweep keys in the 
        dictionaries of the PulList list. 
        Then it uses the Sweep_Iteration_CSV0 function to import this numpy arrays to csv data files, with the desired markers given by the segment parameter, similar as in the 
        CSV_PD functiuon.
        It returns the same StrngName and DataFrames dictionary  as the Sweep_Iteration_CSV0 function.
    """

    pultau,time = Sweep_Iteration(PulList,P,t,N,start,stop)
    StrngName, DataFrames = Sweep_Iteration_CSV0(pultau,AWG,segment,start)

    return StrngName, DataFrames, time


