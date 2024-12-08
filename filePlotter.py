from scipy.io import wavfile
from scipy.signal import spectrogram
import wave 
import matplotlib.pyplot as plt
import numpy as np
from pydub import *
from pydub import AudioSegment
from scipy.signal import butter, filtfilt, welch
from pathlib import Path
from util import *


class Model:
    #Initialize the properties of the audio file stored as class properties.
    def __init__(self):
        self.file = None #File pathway
        self.sample_rate, self.data, self.mono = None, None, None #Sound data required to compute our wavefiles
        self.duration = None #Length of sound file


    #Strip the data from the file passed from the GUI and store them as class properties.
    def preprocess(self, filepath):
        #If the file is present and not null, store the values. Otherwise, return none.
        if filepath != "":
            self.file = filepath
            self.sample_rate, self.data, self.mono = check_filetype(filepath)
            self.duration = self.data.shape[0] / self.sample_rate

        else:
            print("File not loaded")
            return None

        #Return the time of the audio file when successfully imported.
        return self.duration

    # This function retrieves the data from the model class and uses matplotlib to display a graph of the waveform
    def plot_waveform(self):
        #The following 3 lines create the x axis as time, and establishes the figure which will be passed to GUI
        time = np.linspace(0., self.duration, self.data.shape[0])
        fig = plt.Figure(figsize=(8, 4),dpi=100)
        ax = fig.add_subplot(111)

        #Set labels for the graph
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True)

        #Test if the data is mono or stereo. If stereo, display both left and right channel, otherwise display mono.
        if len(self.data.shape) > 1:
            ax.plot(time, self.data[:, 0], label="Left Channel", color="red")
            ax.plot(time, self.data[:, 1], label="Right Channel", color="blue")

        else:
            ax.plot(time, self.mono)

        #Return the composed figure to the GUI
        return fig

        
    def plot_spectrogram(self):
        f, t, Sxx = spectrogram(self.mono, fs=self.sample_rate, nperseg=1024)
        fig = plt.Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx), shading="gouraud", cmap="viridis")
        fig.colorbar(pcm, ax=ax, label="Intensity (dB)")
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        return fig

    def plot_low_rt60(self):  # RT60 low plot function
        if self.mono is None:
            return None
        # Apply bandpass filter for low frequencies (up to 250 Hz)
        return 20*(np.log10(np.abs(self.bandpass_filter(60, 250, self.sample_rate))))


    def plot_mid_rt60(self):  # RT60 mid plot function
        if self.mono is None:
            return None

        # Apply bandpass filter for mid frequencies (250 Hz to 7 kHz)
        return 20*(np.log10(np.abs(self.bandpass_filter(250, 10000, self.sample_rate))))


    def plot_high_rt60(self):  # RT60 high plot function
        if self.mono is None:
            return None

        # Apply bandpass filter for high frequencies (7 kHz to 15 kHz)
        return 20*(np.log10(np.abs(self.bandpass_filter(10000, 20000, self.sample_rate))))

    #band_pass filter for the model class
    def bandpass_filter(self, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, self.mono)

    def plot_rt60(self):  # RT60 plot function
            #Low RT60
            x = np.linspace(0, len(self.data) / self.sample_rate, len(self.data))

            fig_low = plt.Figure(figsize=(8, 4))
            low_axis = fig_low.add_subplot(111)
            low_y = self.plot_low_rt60()
            low_axis.plot(x, low_y,label="RT60 Line Graph", color="cornflowerblue")
            low_axis.scatter([x[np.argmax(low_y)]], [np.max(low_y)], 30, color="blue", label="Low Point")

            #Labels for the low rt60 plot
            low_axis.set_title("Mid RT60")
            low_axis.set_xlabel("Time (s)")
            low_axis.set_ylabel("Amplitude (dB)")
            low_axis.legend()


            #Med rt60 plot creation
            fig_mid = plt.Figure(figsize=(8, 4))
            mid_axis = fig_mid.add_subplot(111)
            mid_y = self.plot_mid_rt60()
            mid_axis.plot(x, mid_y, label="RT60 Line Graph", color="limegreen")
            mid_axis.scatter([x[np.argmax(mid_y)]], [np.max(mid_y)], 30, color="green", label="Low Point")

            #Mid rt60 labels
            mid_axis.set_title("Mid RT60")
            mid_axis.set_xlabel("Time (s)")
            mid_axis.set_ylabel("Amplitude (dB)")
            mid_axis.legend()

            #Establish the figure for the high RT60 model
            fig_high = plt.Figure(figsize=(8, 4))
            high_axis = fig_high.add_subplot(111)
            high_y = self.plot_high_rt60()
            high_axis.plot(x, high_y, label="RT60 Line Graph", color="tomato")
            high_axis.scatter([x[np.argmax(high_y)]], [np.max(high_y)], 30, color="red", label="Low Point")

            #Set the titles for high figure
            high_axis.set_title("High RT60")
            high_axis.set_xlabel("Time (s)")
            high_axis.set_ylabel("Amplitude (dB)")
            high_axis.legend()

            #Take the plots generated in this function and then combine them into one file.
            fig_all = plt.Figure(figsize=(8, 4))
            all_axis = fig_all.add_subplot(111)
            all_axis.plot(x, low_y, label="RT60 Line Graph", color="cornflowerblue")
            all_axis.scatter([x[np.argmax(low_y)]], [np.max(low_y)], 30, color="blue", label="Low Point")
            all_axis.plot(x, mid_y, label="RT60 Line Graph", color="limegreen")
            all_axis.scatter([x[np.argmax(mid_y)]], [np.max(mid_y)], 30, color="green", label="Low Point")
            all_axis.plot(x, high_y, label="RT60 Line Graph", color="tomato")
            all_axis.scatter([x[np.argmax(high_y)]], [np.max(high_y)], 30, color="red", label="Low Point")

            #Set titles for the combined RT60 plot
            all_axis.set_title("Combined RT60")
            all_axis.set_xlabel("Time (s)")
            all_axis.set_ylabel("Amplitude (dB)")
            all_axis.legend()

            return (fig_low,fig_mid,fig_high,fig_all)

    #Funtion called in the plot_wave function in the GUI to gather resonant frequency
    def resonant_freq(self):
        frequencies, power = welch(self.mono, self.sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return round(dominant_frequency)