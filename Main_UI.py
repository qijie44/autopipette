#TODO currently experiencing issues with canvas/frames, if reusing this code, forgo the resizing canvas and change everything to frames

import tkinter as tk
from load_config import load_config


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Automated Pipette")

        #load the configs on startup
        Main.eppendorf_data = load_config("Eppendorfs.csv")
        Main.solutions_data = load_config("Solutions.csv")

        # Taking the screen dimensions and setting the window to the dimensions
        Main.screen_width = self.winfo_screenwidth()
        Main.screen_height = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (Main.screen_width, Main.screen_height - 70, -10, 0))
        # TODO: import the read_config file after merging this branch back

        # Creating a main container that will contain all the different pages
        # TODO: check if this ResizingCanvas even works (nope)
        main_container = ResizingCanvas(self, width=Main.screen_width, height=Main.screen_height - 70,
                                        highlightthickness=0)
        main_container.pack(side="top", fill="both", expand=True)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # create an empty dictionary for frame references
        self.frames = {}

        for page in (StartPage, TempPage):
            # initialise the frames
            frame = page(main_container, self)
            # write the frame to the dictionary
            self.frames[page] = frame
            # TODO: check if this line: creates a grid in the frame for putting things in OR put all of the pages in the same location
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()
        return True


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Automated Pipetting Controller", anchor="center")
        label.grid(columnspan=2)
        # just a boolean to keep check of the info_frame
        self.info_frame = True

        # Making that the rows and columns are a percentage of the screens
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=16)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)

        # Creating the frames for the windows
        self.eppendorf_frame = self.button_frame("eppendorf")
        self.solutions_frame = self.button_frame("solution")
        self.information_frame = tk.Frame(self, bg="grey")
        self.options_frame = tk.Frame(self)

        self.eppendorf_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.solutions_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.information_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.options_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ne")

        self.information_toggle_button = tk.Button(self.options_frame, text="Information", command=self.toggle_info_frame, width=10)

        #TODO add the load configs functionality
        self.load_eppendorf_config_button = tk.Button(self.options_frame, text="Load eppendorfs", commands=self.change_configs("eppendorfs"))
        self.load_solutions_config_button = tk.Button(self.options_frame, text="Load solutions", commands=self.change_configs("solutions"))
        self.load_eppendorf_config_button.grid(row=0, column=0)
        self.load_solutions_config_button.grid(row=0, column=1)
        self.information_toggle_button.grid(row=0, column=2)

        #info_label = Label

        self.eppendorf_frame.tkraise()
        self.solutions_frame.tkraise()


    def button_frame(self, type):
        # Todo : write this dynamic button generation function
        frame = tk.Frame(self, width=int(Main.screen_width/2), height=int(Main.screen_height*2/3), bg="grey")
        button_canvas = ResizingCanvas(frame)

        if type == "eppendorf":
            pass
        elif type == "solution":
            self.solutions_circle(button_canvas)
        else:
            raise FrameError("Unknown Frame!")

        return frame

    # the following are button codes and their dependencies
    def solutions_circle(self, canvas):
        radius = 30
        max_x, max_y = self.get_max(Main.solutions_data)
        for k,v in Main.solutions_data.items():
            x_position = (canvas.width/max_x+2)*v[2]
            y_position = (canvas.height/max_y+2)*v[3]
            canvas.create_oval(x_position, y_position, x_position+radius, y_position+radius, fill="grey")
            print(x_position)

    def get_max(self, dictionary):
        max_x = 0
        max_y = 0
        for k, v in dictionary.items():
            if v[2] > max_x:
                max_x = v[2]
            if v[3] > max_y:
                max_y = v[3]

        return max_x, max_y

    # this is just code to change the frames and toggle the button text
    def toggle_info_frame(self):
        if self.info_frame:
            self.info_frame = False
            self.information_toggle_button.config(text="Solutions")
            self.information_frame.tkraise()
        else:
            self.info_frame = True
            self.information_toggle_button.config(text="Information")
            self.solutions_frame.tkraise()

    def change_configs(self, temp):
        #TODO create a window to select the config file to select
        pass


class TempPage(tk.Frame):
    # This is currently unused, just so that the pages code don't throw a fit
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


master = Main()
master.mainloop()