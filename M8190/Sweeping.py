import numpy as np
import pandas as pd

def sweep0(Pulse,P,p,t):
    
    """Sweeping function for a single pulse with respect of time and duration.

    This function takes the Amplitude, Start and End time, Start and End and Duration of the Pulse dictionary.
    Given a total number of points P, it calcultes the time step dt and the duration step dτ depending on 
    the values of 'Sweep Duration' and 'Sweep time' keys. 
    It then calculates the pulse shape up to the given p point at a time t.
    
    If both of the sweeping keys are equal to zero, it just gives the puls shape at 'Starting time' with 'Starting Duration' at     time t
    """
    
    if 0 <= p <= P:
        
        if Pulse['Sweep time'] == 0:
            dt = 0

        #Sweeping with respect to time
        if Pulse['Sweep time'] == 1:
            dt = (Pulse['End time'] - Pulse['Start time'])/P
            

        if Pulse['Sweep Duration'] == 0:
            dτ = 0

        #Sweeping with respect to Duration
        if Pulse['Sweep Duration'] == 1:
            dτ = (Pulse['End Duration'] - Pulse['Start Duration'])/P
            


        new_start = p * dt + Pulse['Start time']
        new_duration = p * dτ + Pulse['Start Duration']
        
        pol = Pulse['Amplitude'] * (new_start <= t <= new_duration + new_start)
        
          
        return pol
    
    else:
        print('p must be in the interval',[0,P])
        
def Sweep(PulList,P,p,t,N):
    
    """Function that perfoms or not a Sweep, depending on the Sweep dictionary keys, for the Pulse Scheme PulList.
    
    This function is a generalization of the sweep0(Pulse,P,p,t).
    It calls it and maps it over every Pulse in the list of pulses PulList.
    If two pulses overlap, their amplitude is added up.
    P gives the number of sample points for the overal pulse scheme, not to be confused with dt, the sweeping time step given by P
    """
    
    #time interval
    time = np.linspace(-1e-10,t,N)
    #Each pulse will be an array, and an entry of a bigger array (we have an array of arrays)
    pularray = np.zeros((len(PulList),len(time)))
    
    for i in range(0,len(PulList)):
        pularray[i] = np.array([sweep0(PulList[i],P,p,x) for x in time])
        
    #the final pulse scheme will be the overlap of each individual pulse, given by the sum of their arrays    
    pulscheme = np.zeros(len(pularray[0]))
    
    for i in range(0,len(pularray)):
        pulscheme += pularray[i]
        
    return pulscheme


def CSV_PD(pulse_array,segment,name):
    
    """This funcion converts pulse segments numpy arrays into csv files and appends the corresponding markers using pandas. It outputs the correspondant DataFrame


        Segment A correspond to the positive probe pulse and is sync with the marker channels via "1" markers.
        
        Segment B correspond to the negative probe pulse and is sync with the marker channels via the "0" markers.

        the csv file will have be named by 'name'
    """

    Seg = pd.DataFrame( pulse_array,columns=['Y1'] )

    #marker condition
    if segment == "B":
        Markers = pd.DataFrame(np.zeros((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])

    if segment == "A":
        Markers = pd.DataFrame(np.ones((len(pulse_array),2),dtype=int),columns=['SyncMarker1','SampleMarker1'])

    SegMark = pd.concat([Seg,Markers],axis = 1)

    SegMark.to_csv('{n}.csv'.format(n = name),index = False)

    return SegMark


def Tau(PulList,P,t,N):

    """ This function iterates the Sweep function over the range(0,P)

        This function creates an array, whose entries are the corresponding pulse sequences
        at different sweeping steps p. The sweeping advance step is 1.  So far the p time step is ambiguous since here is not really used.
        for accesing a specific sweep step use Sweeping instead.
    """

    time = np.linspace(-1e-10,t,N)
    pultau = np.zeros((P+1,len(time)))


    for i in range(P+1):
        pultau[i]= Sweep(PulList,P,i,t,N)

    return pultau, time



def Param(t,Δt):

    """This function gives the sample size N and the sampling rate Sr to be used for proper 
        pulse time scale.
        
        This function takes the desired total pulse time length and the desired time resolution
        and outputs the corresponding Sapmle size N to be used in the Sweeping function and it 
        also gives the Sample rate Sr to be set in the AWG, in order to get the proper
        time scale within the Pulse from the AWG. Everything should be in the correct units
    """
    #for the sampling rate we have 
    sr=(Δt)**-1

    #for the sample size N
    N=t*sr 

    return N,sr