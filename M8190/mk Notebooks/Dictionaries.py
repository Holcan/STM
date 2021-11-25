#Here are the Dictionaries that correspond to the Pulses and the instrument settings
#Time is given in micro seconds, Amplitude is Voltage in milivolts.
#Daq Model is NI USB-6212(BNC)


AWG_Settings1 = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':300,
    'Clock Sample Frecuency':125000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Trigger In Threshold' : 1,
    'Output Rout': 'DAC',
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S1'
}

AWG_Settings2 = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Trigger In Threshold' : 1,
    'Output Rout': 'DAC',
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S2'
}

AWG_Settings3 = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Trigger In Threshold' : 1,
    'Output Rout': 'DAC', #DAC output rout only has the BNC outputs: Direct Out and (Averaged) Direct Out
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S3'
}

AWG_Settings4 = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Trigger In Threshold' : 1,
    'Output Rout': 'DAC',
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S4'
}

AWG_Settings4huh = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Output Rout': 'DAC',
    'Data Directory': r'D:\Documentos\STM\Python Pulses\S4'
}

AWG_Settings5 = {
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':6000000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Trigger In Threshold' : 1,
    'Output Rout': 'DAC', #DAC output rout only has the BNC outputs: Direct Out and (Averaged) Direct Out
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S5'
}

DAQ_Settings1 = {
    'DAQ Name' : 'DAQBNC1',
    'Analog Channel Input Marker' : 'ai2',
    'Analog Channel Input Waveform' : 'ai0 ',
    'Analog Channel Output' : 'ao1',
    'Minimum Voltage' : -10,
    'Maximum Voltage' : 10,
    'Minimum Voltage Marker' : -9,
    'Maximum Voltage Marker' : 9,
    'Maximum Current': 0.01,
    'Minimum Current' : -0.01,
    'Sampling Frequency' : 1000,
    'Data Directory': r'D:\Documentos\STM\Python Pulses\S1' #path of home computer file!
}

DAQ_Settings2 = {
    'DAQ Name' : 'DAQBNC1',
    'Analog Channel Input Marker' : 'ai2',
    'Analog Channel Input Waveform' : 'ai0 ',
    'Analog Channel Output' : 'ao1',
    'Minimum Voltage' : -4,
    'Maximum Voltage' : 4,
    'Minimum Voltage Marker' : -5,
    'Maximum Voltage Marker' : 5,
    'Maximum Current': 0.01,
    'Minimum Current' : -0.01,
    'Sampling Frequency' : 1000,
    'Data Directory': r'D:\Documentos\STM\Python Pulses\S1'
}



#Pulse Dictionaries:



Rabi = {
    'Name':'Rabi',
    'Amplitude':400,
    'Start time':200,
    'End time':2e-10,
    'Start Duration':100    ,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

Rabi2 = {
    'Name':'Rabi2',
    'Amplitude':-200,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':1,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}


Rabi3 = {
    'Name':'Rabi3',
    'Amplitude':200,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':7,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

PumpN =  {
    'Name':'PumpN',
    'Amplitude':120,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':30,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

ProbeNA = {
    'Name':'ProbeNA',
    'Amplitude':40,
    'Start time':50,
    'End time':90,
    'Start Duration':20,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}

ProbeNB = {
    'Name':'ProbeNB',
    'Amplitude':-40,
    'Start time':50,
    'End time':90,
    'Start Duration':20,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}


Rabis = {
    'Name':'Rabis',
    'Amplitude':40,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':2,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

ProbesA = {
    'Name':'ProbesA',
    'Amplitude':20,
    'Start time':2,
    'End time':12,
    'Start Duration':4,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}

ProbesB = {
    'Name':'ProbesB',
    'Amplitude':-20,
    'Start time':2,
    'End time':12,
    'Start Duration':4,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}

Probe1 = {
    'Name':'Probe1',
    'Amplitude':310,
    'Start time':0,
    'End time':400,
    'Start Duration':100,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}



Probe2 = {
    'Name':'Probe2',
    'Amplitude':-310,
    'Start time':2,
    'End time':12,
    'Start Duration':3,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoG = {
    'Name':'PulsoG',
    'Amplitude':100,
    'Start time':2,
    'End time':12,
    'Start Duration':2,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoH = {
    'Name':'PulsoH',
    'Amplitude':-100,
    'Start time':2,
    'End time':12,
    'Start Duration':2,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

#Pulse Sequences = Lists of Pulse Dictionaries, contained in dictionaries
Pulses_List =  {
    'Name' : 'Pulses_List',
    'Pulse Scheme': [Rabi,Probe1],
    'Number of repetitions': 1,
}

Pulses_List2 =  {
    'Name' : 'Pulses_List2',
    'Pulse Scheme': [Rabi,Probe2],
    'Number of repetitions': 1,
}

PList_secondsA =  {
    'Name' : 'PList_secondsA',
    'Pulse Scheme': [Rabis, ProbesA],
    'Number of repetitions': 1,
}

PList_secondsB =  {
    'Name' : 'PList_secondsB',
    'Pulse Scheme': [Rabis, ProbesB],
    'Number of repetitions': 1,
}

PScheme =  {
    'Name' : 'PScheme',
    'Pulse Scheme': [Rabi, PulsoG],
    'Number of repetitions': 1,
}

PScheme2 =  {
    'Name' : 'PScheme2',
    'Pulse Scheme': [Rabi, PulsoH],
    'Number of repetitions': 1,
}

Nano_ListA =  {
    'Name' : 'Nano_ListA',
    'Pulse Scheme': [PumpN, ProbeNA],
    'Number of repetitions': 1,
}

Nano_ListB =  {
    'Name' : 'Nano_ListB',
    'Pulse Scheme': [PumpN, ProbeNB],
    'Number of repetitions': 1,
}
