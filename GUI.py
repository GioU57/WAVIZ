import tkinter as tk
from matplotlib import figure
from numpy import *
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from filePlotter import *

config = {}

class AudioGUI: # execute logic if run directly
    def __init__(self):
        self._root = tk.Tk() # instantiate instance of Tk class
        self._root.title('Audio File Processor')
        self._root.iconbitmap("WAVIS.ico")
        self.wave_plot = None
        self.file_path = None

        #Analysis variables
        self.file_name = tk.StringVar()
        self.file_frequency = tk.StringVar()

        self.model = None

    def start_gui(self):
        self._root.mainloop()

    def create_gui(self):
        
        #Create the window and establish close condition.
        self._root.deiconify()
        self._root.resizable(False, False)
        self._root.geometry("800x600")
        self.file_path=tk.StringVar()
        
        #self.name_entry = tk.Entry(self._root,textvariable = file_path, font=('calibre',10,'normal'))

        self.LoadBtn = tk.Button(self._root, text="Load Audio File (WAV/MP3)", command=self.print_ligma)
        
        #Establishes the title top frame which organizes the buttons in the GUI

        self._top_frame = tk.Frame(self._root)
        self._top_frame.pack(side=tk.TOP, pady=20)
        self.LoadBtn.pack(padx=10)

        self.button_frame = tk.Frame(self._root)
        self.button_frame.pack(side=tk.TOP, anchor = "n")



        #self.name_entry.pack(padx=10)

        high_freq_radio= tk.Button(self.button_frame, text='High Frequency', command = self.plot_high)
        high_freq_radio.grid(row=0, column=1,padx=5, pady=2, sticky="W")

        med_freq_radio = tk.Button(self.button_frame, text='Mid Frequency', command = self.plot_mid)
        med_freq_radio.grid(row=0, column=2, padx=5, pady=2, sticky="W")

        low_freq_radio = tk.Button(self.button_frame, text='Low Frequency', command = self.plot_low)
        low_freq_radio.grid(row=0, column=3, padx=5, pady=2, sticky="W")

        plot_all_rt60_button = tk.Button(self.button_frame, text='Plot  All RT60', command=self.plot_all)
        plot_all_rt60_button.grid(row=0, column=4, padx=5, pady=2, sticky="W")

        waveform_button = tk.Button(self.button_frame, text='Waveform', command = self.Plot_wave)
        waveform_button.grid(row=0, column=5, padx=5, pady=2, sticky="W")

        spectro_button = tk.Button(self.button_frame, text='Spectrogram', command = self.Plot_spectrogram)
        spectro_button.grid(row=0, column=6, padx=5, pady=2, sticky="W")

        
        #Set up the frame for the details about the graph supporting text. 
        #Accessed from the Plot_Data function.
        self.status_frame = tk.Frame(self._root)
        self.status_frame.pack(side=tk.BOTTOM, pady=10)

        self.file_label = tk.Label(self.status_frame, text= "")
        self.file_label.pack(side=tk.BOTTOM)

        

    def Plot_wave(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()

            #Plotting the wave function should also establish the values in the labels at the bottom of the figure,
            #which displays values such as file name, time, resonant frequency, etc.

            self.file_name.set(f'{self.file_path.split('/')[-1]} : {round(self.model.duration,3)} s \n{self.model.resonant_freq()} hertz')
            self.file_label.config(text=self.file_name.get())


            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_waveform(),master = self._top_frame)
            self.wave_plot.draw()

            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def Plot_spectrogram(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_spectrogram(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)



    def plot_low(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_low_rt60(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_mid(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_mid_rt60(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_high(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_high_rt60(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)

    def plot_all(self):
        if self.file_path is not None:
            if self.wave_plot is not None:
                self.wave_plot.get_tk_widget().pack_forget()
            self.wave_plot =  FigureCanvasTkAgg(self.model.plot_high_rt60(),master = self._top_frame)
            self.wave_plot.draw()
            self.wave_plot.get_tk_widget().pack(side=tk.BOTTOM, fill = tk.BOTH, expand=1)


    def Other_Plot_Data(self):
        time_status = tk.Label(self._root, text="Time: " + "foo"+ " seconds")
        
        time_status.pack(side=tk.BOTTOM)
        temp_status = tk.Label(self._root, text="Other Thing: " + "foo"+ " units")
        temp_status.pack(side=tk.BOTTOM)
        
        temp2_status = tk.Label(self._root, text="Other Other Thing: " + "foo"+ " units")
        temp2_status.pack(side=tk.BOTTOM)

        




    def print_ligma(self):
        self.file_path = askopenfilename(filetypes=[("Audio Files",".wav .mp3")])
        #wow this is li

        self.model = Model()

        self.model.preprocess(self.file_path)

        if self.file_path != "":
            self.Plot_wave()
        


