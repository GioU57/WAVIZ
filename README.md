# Scientific Python Interactive Data Acoustic Modeling (SPIDAM) 🎛️🔊🎵

## Summary🎶🎛️🔍
**WAV*I*Z** is a waveform visualization tool that extracts useful data from audio files. It will start as a highly specialized tool designed with scalability in mind. The specifics of the project will be discussed further in later sections.
is a Python-based project that focuses on analyzing and improving the acoustics of enclosed spaces by measuring reverberation time (RT60). This project employs Python libraries and a graphical user interface to import, clean, visualize, and model acoustic data, ultimately enhancing voice intelligibility.

---

## Compile and Run Instructions

### Setup🔊🔊🔊:
1. Clone the repository:
   ```bash
   git clone https://github.com/GioU57/WAVIZ
   cd WAVIZ
   ```

2. Download Requirements🎛️🎛️🎛️:

- Python 3.8+
- Required Libraries:
  - `contourpy`
  - `cycler`
  - `fonttools`
  - `kiwisolver`
  - `matplotlib`
  - `numpy`
  - `packaging`
  - `pillow`
  - `pydub`
  - `pyparsing`
  - `python-dateutil`
  - `scipy`
  - `six`
  - `ffmpeg-python`
- FFmpeg
    https://ffmpeg.org/download.html
Install all Python dependencies using:
```
pip install countourpy cycler fonttools kiwisolver matplotlib numpy packaging pillow pydub pyparsing python-dateutil scipy six ffmpeg-python
```
---

### Running the Application▶️🎛️🔊
```bash
python main.py
```

#### Input Parameters:
- Audio file input: WAV or MP3 formats
- Desired output plots for waveform and RT60 analysis
- GUI-driven data cleaning, analysis, and reporting

#### Example Workflow:
1. Load a sample file via the GUI.
2. Analyze RT60 values and identify problematic frequency ranges.
3. Export results, including visualizations and statistics, to a report.
---
Features 🏆🎛️🔊
Interactive GUI: Easy-to-use interface for loading and analyzing audio files.
RT60 Calculation: Accurately measures reverberation times for enclosed spaces.
Waveform Visualization: Generate clean, interactive plots of audio waveforms.
Scalable Design: Built for future acoustic modeling enhancements.
🎶🎛️ Dive into WAVIZ and make your sound waves sing! 🔊✨
