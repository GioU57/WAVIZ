# Import required libraries
import numpy as np
from pydub import *
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, welch
from pathlib import Path
import matplotlib.pyplot as plt

def digital_to_decibel(signal):
    if signal > 0:
        return 10 * np.log10(signal)
    else:
        return 0

# Check filetype
def check_filetype(file):
    extension = Path(file).suffix.lower()
    if extension == ".wav":
        sample_rate, data, mono = analyze_audio(file)
    else:
        sample_rate, data, mono = convert_file(file, extension)
    return sample_rate, data, mono

# Convert filetype
def convert_file(file, extension):
    if extension == ".mp3":
        AudioSegment.from_mp3(file).export("newfile.wav", format = "wav")
        sample_rate, data, mono = analyze_audio("newfile.wav")
        Path("newfile.wav").unlink()
    elif extension == "ogg":
        AudioSegment.from_ogg(file).export("newfile.wav", format = "wav")
        sample_rate, data, mono = analyze_audio("newfile.wav")
        Path("newfile.wav").unlink()

    return sample_rate, data, mono

def analyze_audio(file):
    sample_rate, data = wavfile.read(file)
    if len(data.shape) == 2:
        left_channel = data[:, 0]
        right_channel = data[:, 1]
        mono = (left_channel + right_channel)/2
    else:
        mono = data
    return sample_rate, data, mono

def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def reverb_time(model):
    # Reverb time
    value_of_max_less_5 = model.mono[np.argmax(model.mono)]-5
    value_of_max_less_5 = find_nearest_value(model.mono[value_of_max_less_5:], value_of_max_less_5)
    index_of_max_less_5 = np.where(model.mono == value_of_max_less_5)[0][0]

    value_of_max_less_25 = model.mono[np.argmax(model.mono)]-25
    value_of_max_less_25 = find_nearest_value(model.mono[value_of_max_less_25:], value_of_max_less_25)
    index_of_max_less_25 = np.where(model.mono == value_of_max_less_25)[0][0]
    
    rt20 = (index_of_max_less_25 - index_of_max_less_5)/len(model.mono) * model.duration
    rt60 = 3 * rt20
    print(f'RT60 value is {round(rt60)}')
    


def amplitude(data):
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    return value_of_max

def find_target_frequency(freqs, target=1000):
    nearest_freq = freqs[np.abs(freqs - target).argmin()]
    return nearest_freq

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def rt60(filepath):
    # Load the audio file
    sample_rate, data, mono = check_filetype(filepath)


    # Check if the audio has 2 channels
    if len(data.shape) == 2:
        # Split into left and right channels
        left_channel = data[:, 0]
        right_channel = data[:, 1]
        # Optionally, combine the channels (e.g., average)
        data = (left_channel + right_channel) / 2
    else:
        # Mono audio, no change needed
        data = data

    # Define the time vector
    t = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)

    # Calculate the Fourier Transform of the signal
    fft_result = np.fft.fft(data)
    spectrum = np.abs(fft_result)  # Get magnitude spectrum
    freqs = np.fft.fftfreq(len(data), d=1/sample_rate)

    # Use only positive frequencies
    freqs = freqs[:len(freqs)//2]
    spectrum = spectrum[:len(spectrum)//2]


    # Find the target frequency
    target_frequency = find_target_frequency(freqs)

    # Apply a band-pass filter around the target frequency
    filtered_data = bandpass_filter(data, target_frequency - 50, target_frequency + 50, sample_rate)

    # Convert the filtered audio signal to decibel scale
    data_in_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)  # Avoid log of zero


    # Find the index of the maximum value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]

    # Slice the array from the maximum value
    sliced_array = data_in_db[index_of_max:]
    value_of_max_less_5 = value_of_max - 5

    # Find the nearest value for max-5dB and its index
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)[0][0]

    # Find the nearest value for max-25dB and its index
    value_of_max_less_25 = value_of_max - 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)[0][0]

    # Calculate RT60 time
    rt20 = t[index_of_max_less_5] - t[index_of_max_less_25]
    rt60 = 3 * rt20

    # Print RT60 value
    return f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds'
