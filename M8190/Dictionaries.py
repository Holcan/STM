#Here are the Dictionaries that correspond to the Pulses and the instrument settings
#Time is given in micro seconds, Amplitude is Voltage in milivolts.


AWG_Settings1={
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':300,
    'Clock Sample Frecuency':125000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Output Rout': 'DC',
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S1'

}

AWG_Settings2={
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Output Rout': 'DC',
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S2'

}

AWG_Settings3={
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':700,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Output Rout': 'DAC', #DAC output rout only has the BNC outputs: Direct Out and (Averaged) Direct Out
    'Data Directory': r'D:\Alejandro\Pulses\Dict\S3'

}

AWG_Settings4={
    'Visa Resource Name': 'TCPIP0::ibn3-036.ibn-net.kfa-juelich.de::hislip0::INSTR',
    'Voltage Amplitude':300,
    'Clock Sample Frecuency':500000000,
    'Output_Channel': 1,
    'Mode': 'STS',
    'Output Rout': 'DC',
    'Data Directory': r'D:\Documentos\STM\Python Pulses\S4'

}


Rabi={
    'Name':'Rabi',
    'Amplitude':400,
    'Start time':0,
    'End time':2e-10,
    'Start Duration':1,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

Rabi2={
    'Name':'Rabi2',
    'Amplitude':-200,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':1,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}


Rabi3={
    'Name':'Rabi3',
    'Amplitude':200,
    'Start time':1e-10,
    'End time':2e-10,
    'Start Duration':7,
    'End Duration':6,
    'Sweep time':0,
    'Sweep Duration':0
}

Probe1={
    'Name':'Probe1',
    'Amplitude':310,
    'Start time':2,
    'End time':12,
    'Start Duration':3,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}



Probe2={
    'Name':'Probe2',
    'Amplitude':-310,
    'Start time':2,
    'End time':12,
    'Start Duration':3,
    'End Duration':6,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoG={
    'Name':'PulsoG',
    'Amplitude':100,
    'Start time':2,
    'End time':12,
    'Start Duration':2,
    'End Duration':9,
    'Sweep time':1,
    'Sweep Duration':0
}

PulsoH={
    'Name':'PulsoH',
    'Amplitude':-100,
    'Start time':2,
    'End time':12,
    'Start Duration':2,
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