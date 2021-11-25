import numpy as np
import pandas as pd

#The functions in this module are used to generate numpy arrays that correspond to pulse segments,sequences and sweepings of such given the information in the 
#corresponding dictionary in the Dictionary module. 

def sweep0(Pulse,P,p,t,N):
    
    """Sweeping function for a single pulse with respect of time and duration.

    This function takes the Amplitude, Start and End time, Start and End and Duration of the Pulse dictionary.
    Given a total number of points P, it calcultes the time step dt and the duration step dτ depending on 
    the values of 'Sweep Duration' and 'Sweep time' keys. 
    It then calculates the pulse shape up to the given p point at a time t.
    
    If both of the sweeping keys are equal to zero, it just gives the puls shape at 'Starting time' with 'Starting Duration' at  time t.
    There is still a faster version of this.
    """
    time=np.linspace(0,t,N)
    #Pulse array
    pul=np.copy(time)

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
            


        new_start, new_duration = p * dt + Pulse['Start time'], p * dτ + Pulse['Start Duration']
        new_end = new_duration + new_start
    
        pul[pul <= new_start] = 0
        pul[pul >= new_end] = 0
        pul[pul !=0] = Pulse['Amplitude']         
          
        return pul
    
    else:
        print('p must be in the interval',[0,P])


def Sweep(PulList,P,p,t,N):
    
    """Function that perfoms or not a Sweep, depending on the Sweep dictionary keys, for the Pulse Scheme PulList.
    
    This function is a generalization of the sweep0(Pulse,P,p,t).
    It calls it and maps it over every Pulse in the list of pulses PulList.
    If two pulses overlap, their amplitude is added up.
    P gives the number of sample points for the overal pulse scheme, not to be confused with dt, the sweeping time step given by P
    The pulse sequence is generated in the order that the pulses have within the PulseList.
    """
    
    #time interval
    time = np.linspace(0,t,N)
    
    #Each pulse will be an array, and an entry of a bigger array (we have an array of arrays)
    pularray=np.array([sweep0(Pulse,P,p,t,N) for Pulse in PulList])
        
    #the final pulse scheme will be the overlap of each individual pulse, given by the sum of their arrays    
    pulscheme = np.sum(pularray,0)
    
        
    return pulscheme, time
        
def Sweep_teil(PulList,P,p,t,N):
    
    """Function that perfoms or not a Sweep, depending on the Sweep dictionary keys, for the Pulse Scheme PulList.
    
    This function is a generalization of the sweep0(Pulse,P,p,t).
    It calls it and maps it over every Pulse in the list of pulses PulList.
    If two pulses overlap, their amplitude is added up.
    P gives the number of sample points for the overal pulse scheme, not to be confused with dt, the sweeping time step given by P
    The pulse sequence is generated in the order that the pulses have within the PulseList.
    """
    
    #time interval
    time = np.linspace(0,t,N)
    
    #Each pulse will be an array, and an entry of a bigger array (we have an array of arrays)
    pularray=np.array([sweep0(Pulse,P,p,t,N) for Pulse in PulList['Pulse Scheme']])
        
    #the final pulse scheme will be the overlap of each individual pulse, given by the sum of their arrays    
    pulscheme0 = np.sum(pularray,0)
    
    #we divide the pulse scheme in order to play it several times
    teil = int(pulscheme0.size/PulList['Number of repetitions'])
    pulscheme = np.tile(pulscheme0[:teil],PulList['Number of repetitions'])
        
    return pulscheme, time


def Sweep_dir_noteil(PulList,P,p,t,N):
    
    """Function that perfoms or not a Sweep, depending on the Sweep dictionary keys, for the Pulse Scheme PulList.
    
    This function is a generalization of the sweep0(Pulse,P,p,t).
    It calls it and maps it over every Pulse in the list of pulses PulList.
    If two pulses overlap, their amplitude is added up.
    P gives the number of sample points for the overal pulse scheme, not to be confused with dt, the sweeping time step given by P
    The pulse sequence is generated in the order that the pulses have within the PulseList.
    """
    
    #time interval
    time = np.linspace(0,t,N)
    
    #Each pulse will be an array, and an entry of a bigger array (we have an array of arrays)
    pularray=np.array([sweep0(Pulse,P,p,t,N) for Pulse in PulList['Pulse Scheme']])
        
    #the final pulse scheme will be the overlap of each individual pulse, given by the sum of their arrays    
    pulscheme = np.sum(pularray,0)
    
    #we divide the pulse scheme in order to play it several times
    #teil = int(pulscheme0.size/PulList['Number of repetitions'])
    #pulscheme = np.tile(pulscheme0[:teil],PulList['Number of repetitions'])
        
    return pulscheme, time

def Sweep_Iteration(PulList,P,t,N,start,stop):

    """ This function iterates the Sweep function over the smaller interval [start,stop] for a given pulse list PulList

        This function creates an array, whose entries are the corresponding pulse sequences
        at different sweeping steps p, starting at the sweeping step p =start and ending at sweeping step p=stop.
        The sweeping advance step is 1. 
        The set [start,stop] must be contained in the bigger set [0,P].
        In order to access a specific sweeping step use the Sweeping function instead.
    """
    L = (stop-start)
    pultau = np.zeros((L+1,N))
    
    for p in range(0,L+1):
        pultau[(p)],time= Sweep(PulList,P,p+start,t,N) 

    #this dictionary is for obtaining the proper name 
    #Intervaldict={'start':start,'stop':stop,'interval':L}

    return pultau, time

def Sweep_Iteration_teil(PulList,P,t,N,start,stop):

    """ This function iterates the Sweep function over the smaller interval [start,stop] for a given pulse list PulList

        This function creates an array, whose entries are the corresponding pulse sequences
        at different sweeping steps p, starting at the sweeping step p =start and ending at sweeping step p=stop.
        The sweeping advance step is 1. 
        The set [start,stop] must be contained in the bigger set [0,P].
        In order to access a specific sweeping step use the Sweeping function instead.
    """
    L = (stop-start)
    pultau = np.zeros((L+1,N))
    
    for p in range(0,L+1):
        pultau[(p)],time= Sweep_teil(PulList,P,p+start,t,N) 

    #this dictionary is for obtaining the proper name 
    #Intervaldict={'start':start,'stop':stop,'interval':L}

    return pultau, time



def Param(t,Δt):

    """This function gives the sample size N and the sampling rate Sr to be used for proper 
        pulse time scale.
        
        This function takes the desired total pulse time length t and the desired time resolution Δt
        and outputs the corresponding sample size N to be used in the Sweeping function and it 
        also gives the sample rate Sr to be set in the AWG, in order to get the proper
        time scale within the Pulse from the AWG. Everything should be in the correct units
    """
    #for the sampling rate we have 
    sr=(Δt)**-1

    #for the sample size N
    N=t*sr 

    return N,sr
    

<<<<<<< Updated upstream
def Granularity(samples):
    """ This function takes the number of samples and converts it to the closest number that satisfies the granularity
        of 48  

        samples: int
=======
def div_test(sampling_frequency,time_int):
    """ 
    
    
    
    """
    samples = sampling_frequency * time_int

    statement = samples % 48 == 0

    return statement


def Gran_find(starting_freq,ending_freq,time_int):
    """ from the interval of frequency given, this function checks whether there us a multiple of 48 ot satisfy the granularity
    
    
    
    """
    samp_interval = np.arange(starting_freq,ending_freq)
    sol = np.zeros((len(samp_interval)))

    for i,j in zip(samp_interval,range(0,len(sol))):
        if div_test(i,time_int) == True:
            sol[j] = i
        else:
            sol[j] = 0
    return sol

def Granularity(samples):
    """ This function takes the number of samples and converts it to the closest number that satisfies the granularity
        of 48  
>>>>>>> Stashed changes
    """
    
    x = int((samples /48)+1)* 48
    
    return x

#tilecycle 
def Tc(modulation,loop):
    """
    This function takes modulation and number as an argument and returns the time length in seconds of the segment that will build up a cycle


    modulation: int, desired frequency in Herz to use as a reference signal for the Lock-In Amplifier
    loop: int, desired number of repetitions that will build up the whole cycle
    """

    tiled_cycle = (1/2) * (1/ (loop * modulation) )

    return tiled_cycle

def div(samples):
    """ 
    Checks whether a number of samples is ddivisible by the granularity of 48
    
    samples: int, number of samples to be checked
    """
    statement = samples % 48 == 0

    return statement

<<<<<<< Updated upstream

def Adj(resolution,modulation,repetitions):
    """
        Returns the correct AWG sampling frecuency and number of samples of the segment that satisfies the desired parameters and granularity. 

    this function takes the desired time resolution, modulation frequency and number of repetitions and will return the appropiate sampling frequency for the AWG and number
    of samples to build the whole segment cycle, following also the restriction given by the granularity of the AWG.

    
=======
def Adj(resolution,modulation,repetitions):
    """
    240 minimum length
>>>>>>> Stashed changes
    """

    time_length_segment = Tc(modulation,repetitions)

    samples0,sampling_frequency0 = Param(time_length_segment,resolution)

    if div(samples0) == True:
        return samples0,sampling_frequency0

    else:
        adjusted_samples = Granularity(samples0)
        adjusted_sr = int(adjusted_samples/time_length_segment)

        return adjusted_samples, adjusted_sr
        

<<<<<<< Updated upstream
    
=======

def Adj_minimum(modulation,repetitions):
    """ This function returns the proper sampling frequency and segment time length for waveforms with 240 samples, given the desired modulation frequency and number of repetitios
    

    modulation: int, desired modulation frequenxy in Herz to be used as a reference signal in the Lock-In Amplifier
    repetitions: int, desired number of repetitions (loop number). the total duration of one cycle will be split into this number
    """

    time_length_segment = Tc(modulation,repetitions)

    minimum_sample_length = 240 

    sampling_frequency0 = 1/6800000000


    return minimum_sample_length,sampling_frequency0, time_length_segment



def Adj9(resolution,modulation,repetitions):
    """This function returns the proper sampling frequency and segment time length for waveforms with 240 samples, given the desired modulation frequency and number of repetitios

        The minimal segment length is 240

    resolution: int, desired  time resolution for the pulse scheme 
    modulation: int, desired modulation frequenxy in Herz to be used as a reference signal in the Lock-In Amplifier
    repetitions: int, desired number of repetitions (loop number). the total duration of one cycle will be split into this number
    
    """

    time_length_segment = Tc(modulation,repetitions)

    samples0,sampling_frequency0 = Param(time_length_segment,resolution)

    if samples0 < 240 :
        samples0 = 240
        sampling_frequency0 = int(samples0/time_length_segment)
        return samples0,sampling_frequency0

    else :
        if div(samples0) == True:
            return samples0,sampling_frequency0
        else:
            adjusted_samples = Granularity(samples0)
            adjusted_sr = int(adjusted_samples/time_length_segment)

            return adjusted_samples, adjusted_sr, time_length_segment



    
def Adj_minimum2(modulation,repetitions):
    """ This function returns the proper sampling frequency and segment time length for waveforms with 240 samples, given the desired modulation frequency and number of repetitios
    

    modulation: int, desired modulation frequenxy in Herz to be used as a reference signal in the Lock-In Amplifier
    repetitions: int, desired number of repetitions (loop number). the total duration of one cycle will be split into this number
    """

    time_length_segment = Tc(modulation,repetitions)

    sample_length = 240 

    sampling_frequency0 = int(sample_length / time_length_segment)

    while  not sampling_frequency0 in range(125e6,8e9+1):
        sample_length =sample_length  + 48
        sampling_frequency0 = int(sample_length / time_length_segment)

    return sample_length, sampling_frequency0, time_length_segment
>>>>>>> Stashed changes
