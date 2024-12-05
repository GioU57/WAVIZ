from scipy.io import wavfile
import scipy.io
import wave 
import matplotlib.pyplot as plt
import numpy as np
def plot_waveform(file_path):
    try:
        audio_array, framerate = preprocess_audio(file_path)
        if audio_array is None:
              if audio_array is None:
            return None
        f, t, Sxx = spectrogram(audio_array, fs=framerate, nperseg=1024)
        fig = plt.Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx), shading="gouraud", cmap="viridis")
        fig.colorbar(pcm, ax=ax, label="Intensity (dB)")
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        return fig
    except Exception as e:
        print(f"Error plotting spectrogram: {e}")
        return None     return None
        time = np.linspace(0, len(audio_array) / framerate, len(audio_array))
        fig = plt.Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        ax.plot(time, audio_array, label="Waveform", color="blue")
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.legend()
        ax.grid(True)
        return fig
    except Exception as e:
        print(f"Error plotting waveform: {e}")
        return None

def plot_rt60(audio_array, framerate, title, highlight_point=None):#rt60 plot function
    try:
         x = np.linspace(0, len(audio_array) / framerate, len(audio_array))
        y = audio_array
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

def plot_low_rt60(file_path): #rt60 low plot function
    audio_array, framerate = preprocess_audio(file_path)
    if audio_array is None:
        return None
    return plot_rt60(audio_array, framerate, "Low RT60", highlight_point="low")

def plot_mid_rt60(file_path): #rt60 mid plot function
    audio_array, framerate = preprocess_audio(file_path)
    if audio_array is None:
        return None
    return plot_rt60(audio_array, framerate, "Mid RT60", highlight_point="mid")

def plot_high_rt60(file_path): #rt60 high plot function
    audio_array, framerate = preprocess_audio(file_path)
    if audio_array is None:
        return None
    return plot_rt60(audio_array, framerate, "High RT60", highlight_point="high")

def plot_spectrogram(file_path):
    try:
        audio_array, framerate = preprocess_audio(file_path)