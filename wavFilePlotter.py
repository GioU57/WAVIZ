from scipy.io import wavfile
import scipy.io
import wave 
import matplotlib.pyplot as plt
import numpy as np
#samplerate = 44100
#length = 0.4658049886621315
wav_fname = 'Audio Samples\\16bit2chan.wav'
#wav_fname = r'c:\Programming\Python\Group Project!\16bit2chan.wav'

samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f'this is data shape {data.shape}')
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()