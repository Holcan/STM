'Here are the Dictionaries that correspond to the Pulses and the AWG settings'
'Time is given in micro seconds, Amplitude is Voltage in milivolts.'


AWG_S1={
    'Visa_Resource_Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':300,
    'Clock Sample Frecuency':125000000,
    'Output_Channel': 1,
    'Output_rout': 'DC'

}

AWG_S2={
    'Visa_Resource_Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Amplitude':300,
    'Clock Sample Frecuency':7200000000,
    'Output_Channel': 1,
    'Output_rout': 'DC'

}

Rabi={
    'Name':'Rabi',
    'Amplitude':200,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':1,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

Probe1={
    'Name':'Probe1',
    'Amplitude':50,
    'Start time':1,
    'End time':11,
    'Start Duration':1,
    'End Duration':9 ,
    'Sweep time':1,
    'Sweep Duration':0
}

Rabi2={
    'Name':'Rabi2',
    'Amplitude':-100,
    'Start time':1,
    'End time':2e-10,
    'Start Duration':2,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

Probe2={
    'Name':'Probe2',
    'Amplitude':-50,
    'Start time':1,
    'End time':4,
    'Start Duration':1,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoG={
    'Name':'PulsoG',
    'Amplitude':-50,
    'Start time':2,
    'End time':20,
    'Start Duration':1,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoH={
    'Name':'PulsoH',
    'Amplitude':-50,
    'Start time':3,
    'End time':20,
    'Start Duration':1,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

#Pulse Sequences = Lists of Dictionaries

Pulses_List = [
    Rabi,Probe1
    ]  ;



Pulses_List2 = [
    Rabi,Probe2
    ];

PScheme=[
    Rabi, PulsoG
    ];

PScheme2=[
    Rabi2, PulsoH
    ]