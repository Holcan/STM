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

    #string for the new scv file location
    new_csv = r'{File_Location}\Segment{seg}_{n}_{nm}.csv'.format(File_Location = AWG['Data Directory'],seg=segment,n=len(pulse_array),nm=step)

    #exporting the data frame to csv
    SegMark.to_csv(new_csv, index= False)

    return new_csv, SegMark


def TDF_CVS(pultau,AWG,segment):

#CHECK THIS
    """ This function produces the corresponging normalized CSV files given by the entries of the pultau array.

        This function is a generalize version of the CSV_PD function, and it works for the Pulse arrayes 
        given by the Tau function.
        It uses the CSV_PD function to produce the CSV files asociated to each sweeping iteration.
        It also outputs the DataFrames dictionary, whose elements are the Data Frames asociated to the CSV files.
    """
    
    #pultau, tim= Tau(PulList,P,t,N,start,stop)

    DataFrames={}
    for i in range(len(pultau)):
        DataFrames['Data Frame Segment{seg}, data={val}, step{n}'.format( seg = segment ,val =len(pultau),n=i)] = CSV_PD(pultau[i],AWG,segment,i)

    return  DataFrames

