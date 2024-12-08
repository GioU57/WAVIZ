import tkinter as tk
from matplotlib import figure
from numpy import *
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import util
from filePlotter import *

from util import *

config = {}

class AudioGUI: #Execute logic if run directly
    def __init__(self): #Initialize the frme of the GUIs and required properties

        self._root = tk.Tk() # instantiate instance of Tk class

        #Boot the _root and establish the title and icon properties.
        self._root.title('Audio File Processor')
        self._root.iconbitmap("WAVIS.ico")

        #Wave_plot is the graph figure we will be placing the figures into
        self.wave_plot = None
        self.file_path = None

        #Analysis variables
        self.file_name = tk.StringVar()
        self.file_frequency = tk.StringVar()

        #Model class based off filePlotter.py Model Class -> established in file_select()
        self.model = None

        #Figures stores the fig data types passed from the file plotter into a list, which is cycled through to change
        #the current RT60 plot being viewed.
        self.figures = None

    #Mainloop init
    def start_gui(self):
        self._root.mainloop()

    #Called from main.py and runs the start up for the GUI frame which contains all the frames imaging
    def create_gui(self):
        
        #Create the window
        self._root.deiconify()
        self._root.resizable(False, False)
        self._root.geometry("800x600")

        #Make the file_path a string var that stores the filepath as a string.
        self.file_path=tk.StringVar()

        #Button to prompt file_select and open the file navigation window
        self.LoadBtn = tk.Button(self._root, text="Load Audio File (WAV/MP3)", command=self.file_select)
        
        #Establishes the title top frame which organizes the buttons in the GUI
        self._top_frame = tk.Frame(self._root)
        self._top_frame.pack(side=tk.TOP, pady=20)
        self.LoadBtn.pack(padx=10)

        #Button frame to keep buttons together in the root frame
        self.button_frame = tk.Frame(self._root)
        self.button_frame.pack(side=tk.TOP, anchor = "n")

        #Create the buttons to call the RT60 draw functions for high, medium, and low and load them into the button grid
        high_freq_radio= tk.Button(self.button_frame, text='High Frequency', command = self.plot_high)
        high_freq_radio.grid(row=0, column=1,padx=5, pady=2, sticky="W")

        med_freq_radio = tk.Button(self.button_frame, text='Mid Frequency', command = self.plot_mid)
        med_freq_radio.grid(row=0, column=2, padx=5, pady=2, sticky="W")

        low_freq_radio = tk.Button(self.button_frame, text='Low Frequency', command = self.plot_low)
        low_freq_radio.grid(row=0, column=3, padx=5, pady=2, sticky="W")

        plot_all_rt60_button = tk.Button(self.button_frame, text='Plot  All RT60', command= self.plot_all)
        plot_all_rt60_button.grid(row=0, column=4, padx=5, pady=2, sticky="W")

        #Button to call the Plot_wave function draws the waveform figure
        waveform_button = tk.Button(self.button_frame, text='Waveform', command = self.Plot_wave)
        waveform_button.grid(row=0, column=5, padx=5, pady=2, sticky="W")

        #Button to call the Plot_wave function draws the spectrogram figure
        spectro_button = tk.Button(self.button_frame, text='Spectrogram', command = self.Plot_spectrogram)
        spectro_button.grid(row=0, column=6, padx=5, pady=2, sticky="W")

        
        #Set up the frame for the details about the graph supporting text. 
        #Accessed from the Plot_Data function.
        self.status_frame = tk.Frame(self._root)
        self.status_frame.pack(side=tk.BOTTOM, pady=10)
        self.file_label = tk.Label(self.status_frame, text= "")
        self.file_label.pack(side=tk.BOTTOM)

    #Function to draw the waveform figure, called from the load file button and the waveform button
    def Plot_wave(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()

            #Plotting the wave function should also establish the values in the labels at the bottom of the figure,
            #which displays values such as file name, time, resonant frequency, etc.

            self.file_name.set(f'{self.file_path.split('/')[-1]} : {round(self.model.duration,3)} s \n{self.model.resonant_freq()} hertz\n{util.rt60(self.file_path)}')
            self.file_label.config(text=self.file_name.get())

            #Draw teh waveform using the matplot -> tkinter canvas module and calling the plot_waveform function in the
            #model. Model should always return a figure from matplotlib.
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_waveform(),master = self._top_frame)
            self.wave_plot.draw()

            #Pack the figure in order to appear in the graph frame.
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    #This repeats what the plot_wave function does but for the spectrogram
    def Plot_spectrogram(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_spectrogram(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    # The following functions (plot_low, plot_mid, plot_high, plot_all) call their respective functions in the model
    #and draw the stored figure from self.figures[]. These are created from the model when called in the plot_RT60
    #function call in the file_select function.

    def plot_low(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.figures[0],master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_mid(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.figures[1],master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_high(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.figures[2],master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_all(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.figures[3],master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    #Called from the load_file button: prompts the file nav window and then plots the waveform from the file.
    def file_select(self):
        self.file_path = askopenfilename(filetypes=[("Audio Files",".wav .mp3")])
        self.model = Model()

        if self.file_path != "":
            self.model.preprocess(self.file_path)
            self.Plot_wave()
            self.figures = self.model.plot_rt60()
        


