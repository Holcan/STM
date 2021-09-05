import numpy as np
import pandas as pd
from Sweeping import *

#The functions in this module are used to save the pulse numpy arrays creeated by the Sweeping module functions as csv files, mainly using the pandas module and the generated DataFrames


def CSV_PD(pulse_array0,AWG_Settings_Dict,marker,step):
    
    """This funcion converts pulse segments numpy arrays into csv files and appends the markers. It outputs the file strng name and the DataFrame

        This function first normalizes pulse_array by the value of the voltage given in the settings 'Voltage Amplitude' AWG_Settings_Dict dictionary key.
        'marker' should be either 1 or 0, it assigns the given marker to the csv file. If marker is 1, file name will be labeled as "SegmentA..."
        if marker is 0, file name will be labeled as "SegmenttB..."
        'step' corresponds to the sweeping step of the Sweeping function.
        The csv file will have be named: Segment(A or B)_(number of data points)_(sweeping step) and its location will be the folder direction
        given by the dictionary key 'Data Directory' in the AWG_Settings_Dict dictionary.
    """
    #normalizing the array values
    pulse_array = pulse_array0/AWG_Settings_Dict['Voltage Amplitude']

    Seg = pd.DataFrame( pulse_array,columns=['Y1'] )

    #marker condition
    if marker == 0:
        Markers = pd.DataFrame(np.zeros((len(pulse_array),2),dtype=np.int8),columns=['SyncMarker1','SampleMarker1'])
        segment = 'B'

    if marker == 1:
        Markers = pd.DataFrame(np.ones((len(pulse_array),2),dtype=np.int8),columns=['SyncMarker1','SampleMarker1'])
        segment ='A'

    #Appending the markers    
    SegMark = pd.concat([Seg,Markers],axis = 1)

    #string for the new csv file location
    new_csv = r'{File_Location}\Segment{seg}_{n}_{nm}.csv'.format(File_Location = AWG_Settings_Dict['Data Directory'],seg=segment,n=len(pulse_array),nm=step)

    #exporting the data frame to csv
    SegMark.to_csv(new_csv, index= False)

    return new_csv, SegMark


def Sweep_Iteration_CSV_Arrays(pultau,AWG_Settings_Dict,marker,start):


    """ This function produces the corresponging normalized CSV files given by the entries of the pultau array(of arrays).

        This function is a generalize version of the CSV_PD function, and it works for the Pulse arrayes 
        given by the Sweep_Iteration function.
        pultau is an array of arrays.
        It uses the CSV_PD function to produce the CSV files asociated to each sweeping iteration.
        It outputs 2 dictionaries: the StrngName and the DataFrames dictionary.
        The StrngName dictionary has the csv files directory\name 's stored in the directory given by the corresponding AWG_Settings_Dict key.
        The DataFrames dictionary  has as elements the Data Frames asociated to the CSV files.
        Start refers to the starting sweeping step  of the Sweep_Iteration function
    """

    DataFrames={}
    StrngName={}
    for i in range(len(pultau)):
        StrngName['Pulse File Location, at step {step}'.format(step=i+start)],DataFrames['Segment{seg}_{val}_{n}'.format( seg = "A" if marker == 1 else "B" ,val =len(pultau[i]),n=i+start)] = CSV_PD(pultau[i],AWG_Settings_Dict,marker,i+start)

    return  StrngName,DataFrames

def Sweep_Iteration_CSV_List(PulList,P,t,N,start,stop,AWG_Settings_Dict,marker):
    
    """This function combinates the Sweep_Iteration function with the Sweep_Iteration_CSV_Arrays function.

        Using the Sweep_Iteration function it creates numpy arrays corresponding to the pulse squemes at different sweep steps accordingly to the pulse Sweep keys in the 
        dictionaries of the PulList list. 
        Then it uses the Sweep_Iteration_CSV_Arrays function to import this numpy arrays to csv data files, with the desired markers given by the marker parameter, similar as in the 
        CSV_PD functiuon.
        It returns the same StrngName and DataFrames dictionary  as the Sweep_Iteration_CSV_Arrays function.
    """

    pultau,time = Sweep_Iteration(PulList,P,t,N,start,stop)
    StrngName, DataFrames = Sweep_Iteration_CSV_Arrays(pultau,AWG_Settings_Dict,marker,start)

    return StrngName, DataFrames, time

def Sweep_Iteration_CSV_List_teil(PulList,P,t,N,start,stop,AWG_Settings_Dict,marker):
    
    """This function combinates the Sweep_Iteration function with the Sweep_Iteration_CSV_Arrays function.

        Using the Sweep_Iteration function it creates numpy arrays corresponding to the pulse squemes at different sweep steps accordingly to the pulse Sweep keys in the 
        dictionaries of the PulList list. 
        Then it uses the Sweep_Iteration_CSV_Arrays function to import this numpy arrays to csv data files, with the desired markers given by the marker parameter, similar as in the 
        CSV_PD functiuon.
        It returns the same StrngName and DataFrames dictionary  as the Sweep_Iteration_CSV_Arrays function.
    """

    pultau,time = Sweep_Iteration_teil(PulList,P,t,N,start,stop)
    StrngName, DataFrames = Sweep_Iteration_CSV_Arrays(pultau,AWG_Settings_Dict,marker,start)

    return StrngName, DataFrames, time
