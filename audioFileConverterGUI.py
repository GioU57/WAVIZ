import tkinter as tk
from matplotlib import figure
from numpy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


config = {}

class AudioGUI: # execute logic if run directly
    def __init__(self):
        self._root = tk.Tk() # instantiate instance of Tk class
        self._root.title('Audio File Processor')
        self._root.iconbitmap("WAVIS.ico")
        self.LoadBtn = tk.Button(self._root, text="Load Audio File (WAV/MP3)", command=self.print_ligma())

    def start_gui(self):
        self._root.mainloop()

    def create_gui(self):
        #Create the window and establish close condition.
        self._root.title("Hello")
        self._root.deiconify()
        self._root.geometry("500x350")
        #self._root.protocol("WM_DELETE_WINDOW", exit(0))

        self._top_frame = tk.Frame(self._root)
        self._top_frame.pack(side=tk.TOP, pady=20)
        self.LoadBtn.pack(padx=10)


        high_freq_radio= tk.Radiobutton(self._top_frame, text='High Frequency', variable=self.print_ligma(), value='high')
        high_freq_radio.grid(row=0, column=1,padx=5, pady=2, sticky="W")

        med_freq_radio = tk.Radiobutton(self._top_frame, text='Mid Frequency', variable=self.print_ligma(),value='med')
        med_freq_radio.grid(row=0, column=2, padx=5, pady=2, sticky="W")

        low_freq_radio = tk.Radiobutton(self._top_frame, text='Low Frequency', variable=self.print_ligma(),value='low')
        low_freq_radio.grid(row=0, column=3, padx=5, pady=2, sticky="W")

        high_freq_radio.configure(state='normal')

        self.graph_frame = tk.Frame(self._root)
        self.graph_frame.pack(side=tk.BOTTOM, pady=20)
        
        #Set up the frame for the details about the graph supporting text. 
        #Accessed from the Plot_Data function.
        self.status_frame = tk.Frame(self._root)
        self.status_frame.pack(side=tk.BOTTOM, pady=10)

        self.Plot_Data()

        

    
    def Plot_Data(self):
        self.graphs = [0]
        #self.canvas = FigureCanvasTkAgg(self.graphs[0], master=self._root)

        time_status = tk.Label(self._root, text="Time: " + "foo"+ " seconds")
        
        time_status.pack(side=tk.BOTTOM)
        temp_status = tk.Label(self._root, text="Other Thing: " + "foo"+ " units")
        temp_status.pack(side=tk.BOTTOM)
        
        temp2_status = tk.Label(self._root, text="Other Other Thing: " + "foo"+ " units")
        temp2_status.pack(side=tk.BOTTOM)

        




    def print_ligma(self):
        print("ligma")