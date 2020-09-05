import tkinter as tk


pages = {main_page}

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "automated pipette")

        # Taking the screen dimensions and setting the window to the dimensions
        main.screen_width = self.winfo_screenwidth()
        main.screen_height = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (main.screen_width, main.screen_height - 70, -10, 0))

        # Creating a main container that will contain all the different pages
        # TODO: check if this even works
        main_container = ResizingCanvas(self, width=main.screen_width, height=main.screen_height - 70,
                                        highlightthickness=0)
        main_container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create an empty dictionary for frame references
        self.frames = {}

        for page in pages:
            # initialise the frames
            frame = page(container, self)
            # write the frame to the dictionary
            self.frames[page] = frame
            # TODO: check if this line: creates a grid in the frame for putting things in OR put all of the pages in the same location
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()
        return True


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Automated Pipetting Controller")

    def button_frame(self):
        # Todo : write this dynamic button generation function
        pass


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


master = main()
master.mainloop()