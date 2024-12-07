from scipy.io import wavfile
from scipy.signal import spectrogram
import wave 
import matplotlib.pyplot as plt
import numpy as np
from util import *

class Model:
    def __init__(self):
        self.file = None
        self.sample_rate, self.data, self.mono = None, None, None
        self.duration = None

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
            ax.legend()
            ax.grid(True)
        else:
            ax.plot(time, self.mono)
            ax.set_title("Waveform")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            ax.grid(True)
        return fig

        
    def plot_spectrogram(self):
        f, t, Sxx = spectrogram(self.data, fs=self.sample_rate, nperseg=1024)
        fig = plt.Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx), shading="gouraud", cmap="viridis")
        fig.colorbar(pcm, ax=ax, label="Intensity (dB)")
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        return fig
    
"""""
    def plot_rt60(self, title, highlight_point=None):#rt60 plot function
        try:
            x = np.linspace(0, len(self.mono) / self.sample_rate, len(self.mono))
            y = self.mono
            fig = plt.Figure(figsize=(8, 4))
            ax = fig.add_subplot(111)
            ax.plot(x, y, label="RT60 Line Graph", color="black")
            if highlight_point == "low":
                ax.scatter([x[np.argmin(y)]], [np.min(y)], color="blue", label="Low Point")
            elif highlight_point == "mid":
                mid_idx = len(x) // 2
                ax.scatter([x[mid_idx]], [y[mid_idx]], color="green", label="Mid Point")
            elif highlight_point == "high":
                ax.scatter([x[np.argmax(y)]], [np.max(y)], color="red", label="High Point")
            ax.set_title(title)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            ax.grid(True)
            return fig

        except Exception as e:
            print(f"Error plotting RT60: {e}")
            return None
        
    def plot_low_rt60(self): #rt60 low plot function
        self.mono, self.sample_rate = preprocess_audio(file_path)
        if self.mono is None:
            return None
        return plot_rt60(self.mono, self.sample_rate, "Low RT60", highlight_point="low")

    def plot_mid_rt60(self): #rt60 mid plot function
        self.mono, self.sample_rate = preprocess_audio(file_path)
        if self.mono is None:
            return None
        return plot_rt60(self.mono, self.sample_rate, "Mid RT60", highlight_point="mid")

    def plot_high_rt60(self): #rt60 high plot function
        self.mono, self.sample_rate = preprocess_audio(file_path)
        if self.mono is None:
            return None
        return plot_rt60(self.mono, self.sample_rate, "High RT60", highlight_point="high")
"""
    

