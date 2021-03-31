import numpy as np
import pandas as pd
from Sweeping import *



def CSV_PD(pulse_array0,AWG,segment,step):
    
    """This funcion converts pulse segments numpy arrays into csv files and appends the corresponding markers using pandas. It outputs the correspondant DataFrame

        It also normalizes pulse_array by the value of the voltage given in the settings dictionary AWG

        Segment A correspond to the positive probe pulse and is sync with the marker channels via "1" markers.
        
        Segment B correspond to the negative probe pulse and is sync with the marker channels via the "0" markers.

        the csv file will have be named: Segment(A or B)_(number of data points)_(sweeping step)
    """
    pulse_array = pulse_array0/AWG['Voltage Amplitude']

    Seg = pd.DataFrame( pulse_array,columns=['Y1'] )

    #marker condition
    if segment == "B":
        Markers = pd.DataFrame(np.zeros((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])

    if segment == "A":
        Markers = pd.DataFrame(np.ones((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])

    SegMark = pd.concat([Seg,Markers],axis = 1)

    SegMark.to_csv(r'{File_Location}\Segment{seg}_{n}_{nm}.csv'.format(File_Location = AWG['Data Directory'],seg=segment,n=len(pulse_array),nm=step),index=False)

    return SegMark


def TDF_CVS(pultau,AWG,segment):

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

