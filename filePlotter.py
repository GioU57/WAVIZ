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
    def __init__(self):
        self.file = None
        self.sample_rate, self.data, self.mono = None, None, None
        self.duration = None

    #Strip the data from the file passed from the GUI
    def preprocess(self, filepath):
        if filepath != "":
            self.file = filepath
            self.sample_rate, self.data, self.mono = check_filetype(filepath)
            self.duration = self.data.shape[0] / self.sample_rate

        else:
            print("Code broke ur cirnge")
        return self.duration


    def plot_waveform(self):
        time = np.linspace(0., self.duration, self.data.shape[0])
        fig = plt.Figure(figsize=(8, 4),dpi=100)
        ax = fig.add_subplot(111)
        if len(self.data.shape) > 1:
            ax.plot(time, self.data[:, 0], label="Left Channel", color="red")
            ax.plot(time, self.data[:, 1], label="Right Channel", color="blue")
            ax.set_title("Waveform")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            #ax.legend()
            ax.grid(True)
        else:
            ax.plot(time, self.mono)
            ax.set_title("Waveform")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            #ax.legend()
            ax.grid(True)
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
        filtered_data = np.abs(self.bandpass_filter(self.mono, 1, 250, self.sample_rate))
        return self.plot_rt60("Low RT60", highlight_point='low', data=filtered_data)

    def plot_mid_rt60(self):  # RT60 mid plot function
        if self.mono is None:
            return None
        # Apply bandpass filter for mid frequencies (250 Hz to 7 kHz)
        filtered_data = np.abs(self.bandpass_filter(self.mono, 250, 7000, self.sample_rate))
        return self.plot_rt60("Mid RT60", highlight_point='mid', data=filtered_data)

    def plot_high_rt60(self):  # RT60 high plot function
        if self.mono is None:
            return None
        # Apply bandpass filter for high frequencies (7 kHz to 15 kHz)
        filtered_data = np.abs(self.bandpass_filter(self.mono, 7000, 15000, self.sample_rate))
        return self.plot_rt60("High RT60", highlight_point='high', data=filtered_data)

    def bandpass_filter(self, data, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, data)

    def plot_rt60(self, title, highlight_point=None, data=None):  # RT60 plot function
        try:
            if data is None:  # Default to self.mono if no data is provided
                data = self.mono
            x = np.linspace(0, len(data) / self.sample_rate, len(data))
            y = data
            fig = plt.Figure(figsize=(8, 4))
            ax = fig.add_subplot(111)
            if highlight_point == "low":
                ax.plot(x, y, label="RT60 Line Graph", color="cornflowerblue")
                ax.scatter([x[np.argmax(y)]], [np.max(y)], 30, color="blue", label="Low Point")
            elif highlight_point == "mid":
                ax.plot(x, y, label="RT60 Line Graph", color="limegreen")
                ax.scatter([x[np.argmax(y)]], [np.max(y)], 30, color="green", label="Mid Point")
            elif highlight_point == "high":
                ax.plot(x, y, label="RT60 Line Graph", color="tomato")
                ax.scatter([x[np.argmax(y)]], [np.max(y)], 30, color="red", label="High Point")
            ax.set_title(title)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            ax.grid(True)

            return fig


        except Exception as e:
            print(f"Error plotting RT60: {e}")
            return None

    def resonant_freq(self):
        frequencies, power = welch(self.data, self.sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return round(dominant_frequency)