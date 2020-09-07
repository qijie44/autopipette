#TODO currently experiencing issues with canvas/frames, if reusing this code, forgo the resizing canvas and change everything to frames

import tkinter as tk


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Automated Pipette")

        # Taking the screen dimensions and setting the window to the dimensions
        Main.screen_width = self.winfo_screenwidth()
        print(Main.screen_width)
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
        label = tk.Label(self, text="Automated Pipetting Controller", anchor="center", borderwidth=5, relief="groove")
        label.grid(columnspan=2)
        self.info_frame = False

        self.eppendorf_frame = self.button_frame("eppendorf")
        self.solutions_frame = self.button_frame("solution")
        self.information_frame = tk.Frame(self, bg="green", width=50, height=10)

        self.eppendorf_frame.grid(row=1, column=0, padx=10, pady=5)
        self.solutions_frame.grid(row=1, column=1, padx=10, pady=5)
        self.information_frame.grid(row=1, column=1, padx=10, pady=5)
        button = tk.Button(self.information_frame, text = "information")
        button.grid()

        self.information_toggle_button = tk.Button(self, text="Information", command=self.toggle_info_frame)
        self.information_toggle_button.grid(row=2)

        self.eppendorf_frame.tkraise()
        self.solutions_frame.tkraise()


    def button_frame(self, side):
        # Todo : write this dynamic button generation function
        frame = tk.Frame(self, bg="blue", width=Main.screen_width/2, height=100)

        # The following is just test code
        button = tk.Button(frame, text = "test")
        button.grid()

        return frame

    def toggle_info_frame(self):
        if self.info_frame:
            self.info_frame = False
            self.information_toggle_button.config(text="Solutions")
            self.information_frame.tkraise()
        else:
            self.info_frame = True
            self.information_toggle_button.config(text="Information")
            self.solutions_frame.tkraise()


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