# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import os

# Band-pass filter function
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Load the audio file
sample_rate, data = wavfile.read("16bit1chan.wav")

# Import audio
def import_audio():
    print()

# Check if file exists
def file_exists(file):
    if os.path.exists(file):
        check_filetype(file)
    else:
        print("File does not exist")

# Check filetype
def check_filetype(file):
    filetype = file.split('.')
    extension = filetype[-1]
    if extension == "wav":
        analyze_audio(file)
    else:
        convert_file(file)

# Convert filetype
def convert_file(file):
    filetype = file.split('.')
    extension = filetype[-1]
    newfile = filetype[0] + ".wav"
    if extension == "mp3":
        sound = AudioSegment.from_mp3(file)
        sound.export(newfile, format = "wav")
        analyze_audio(newfile)
    else:
        if extension == "ogg":
            sound = AudioSegment.from_ogg(file)
            sound.export(newfile, format = "wav")
            analyze_audio(newfile)

def analyze_audio(file):
    sample_rate, data = wavfile.read(file)
    if len(data.shape) == 2:
        left_channel = data[:, 0]
        right_channel = data[:, 1]
        data = left_channel + right_channel
        reverb_time(data)
        resonant_freq(data)
        amplitude(data)
    else:
        data = data
        reverb_time(data)
        resonant_freq(data)
        amplitude(data)

def reverb_time(data):
    rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
    rt60 = 3 * rt20
    print(f'RT60 value is {round(rt60)}')
    
def resonant_freq(data):
    frequencies, power = welch(data, sample_rate, nperseg=4096)
    dominant_frequency = frequencies[np.argmax(power)]
    print(f'dominant frequency is {round(dominant_frequency)}Hz')

def amplitude(data):
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    return value_of_max

    

# Define the time vector
t = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)

# Calculate the Fourier Transform of the signal
fft_result = np.fft.fft(data)
spectrum = np.abs(fft_result)  # Get magnitude spectrum
freqs = np.fft.fftfreq(len(data), d=1/sample_rate)

# Use only positive frequencies
freqs = freqs[:len(freqs)//2]
spectrum = spectrum[:len(spectrum)//2]

# Find the target frequency closest to 1000 Hz
def find_target_frequency(freqs, target=1000):
    nearest_freq = freqs[np.abs(freqs - target).argmin()]
    return nearest_freq

# Find the target frequency
target_frequency = find_target_frequency(freqs)

# Apply a band-pass filter around the target frequency
filtered_data = bandpass_filter(data, target_frequency - 50, target_frequency + 50, sample_rate)

# Convert the filtered audio signal to decibel scale
data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero

# Plot the filtered signal in decibel scale
plt.figure(2)
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')

# Find the index of the maximum value
index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

# Slice the array from the maximum value
sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5

# Function to find the nearest value in the array
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# Find the nearest value for max-5dB and its index
value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

# Find the nearest value for max-25dB and its index
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

# Calculate RT60 time
rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
rt60 = 3 * rt20

# Display plot
plt.grid()
plt.show()

# Print RT60 value
print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')
