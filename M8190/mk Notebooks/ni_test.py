import nidaqmx
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt
import numpy as np

with nidaqmx.Task() as task:
    freq = 1e3
    duration = 5
    samples = duration * freq
    task.ai_channels.add_ai_voltage_chan('{a}/{b}'.format(a = 'DAQBNC1', b = 'ai1'))
    task.timing.cfg_samp_clk_timing(freq, samps_per_chan=int(samples))
    data = np.array(task.read(int(samples)))


plt.figure()
plt.plot(data)
plt.show()