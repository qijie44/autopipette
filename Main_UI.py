import tkinter as tk
from load_config import load_config

unselected_color = "white"
selected_color = "grey"
GIANT_FONT = ("Helvetica", 20, "bold")

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Automated Pipette")

        # load the configs on startup
        Main.eppendorf_data = load_config("Eppendorfs.csv")
        Main.solutions_data = load_config("Solutions.csv")

        # Taking the screen dimensions and setting the window to the dimensions
        Main.screen_width = self.winfo_screenwidth()
        Main.screen_height = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (Main.screen_width, Main.screen_height - 70, -10, 0))

        # Creating a main container that will contain all the different pages
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
        label = tk.Label(self, text="Automated Pipetting Controller", anchor="center", font=GIANT_FONT)
        label.grid(columnspan=2)
        # just a boolean to keep check of the info_frame
        self.info_frame = False
        self.eppendorf_canvas = None
        self.eppendorf_label = None

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

        # Populating the information frame
        self.eppendorf_label = tk.Label(self.information_frame, text="None Selected", font=GIANT_FONT)
        self.eppendorf_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        row = 1
        for k, v in Main.solutions_data.items():
            solution_label = tk.Label(self.information_frame, text=k)
            solution_label.grid(row=row, column=0)
            # creating the entry boxes and tying them to the solutions data dictionary (this is 5 on the list)
            Main.solutions_data[k].append(tk.Entry(self.information_frame))
            Main.solutions_data[k][5].grid(row=row, column=1)
            row += 1
        save_solution = tk.Button(self.information_frame, text="Save solutions", command=self.save_solutions)
        save_solution.grid(row=row, column=3)


        # TODO: Update the function below after writing the change_config function
        # Populating the options frame
        self.load_eppendorf_config_button = tk.Button(self.options_frame, text="Load eppendorfs",
                                                      command=lambda: self.change_configs("eppendorfs"))
        self.load_solutions_config_button = tk.Button(self.options_frame, text="Load solutions",
                                                      command=lambda: self.change_configs("solutions"))
        self.information_toggle_button = tk.Button(self.options_frame, text="Information",
                                                   command=self.toggle_info_frame, width=10)
        self.save_to_file_button = tk.Button(self.options_frame, text="Save to File",
                                                   command=self.save_to_file, width=10)
        self.load_eppendorf_config_button.grid(row=0, column=0)
        self.load_solutions_config_button.grid(row=0, column=1)
        self.information_toggle_button.grid(row=0, column=2)
        self.save_to_file_button.grid(row=0, column=3)

        self.eppendorf_frame.tkraise()
        self.solutions_frame.tkraise()

    def button_frame(self, frame_type):
        frame = tk.Frame(self, width=int(Main.screen_width / 2), height=int(Main.screen_height * 2 / 3), bg="grey",
                         highlightbackground="black", highlightthickness=1)
        button_canvas = ResizingCanvas(frame)

        if frame_type == "eppendorf":
            self.eppendorf_circles(button_canvas)
            self.eppendorf_canvas = button_canvas
        elif frame_type == "solution":
            self.solutions_circle(button_canvas)
            add_solution_button = tk.Button(frame, text="Add Solutions", command=self.add_solutions)
            button_canvas.create_window(button_canvas.width-(button_canvas.width/15), button_canvas.height-5, window=add_solution_button)
        else:
            raise Exception("Unknown Frame!")
        button_canvas.pack()

        return frame

    # the following are button codes and their dependencies
    def solutions_circle(self, canvas, color="grey"):
        radius = 44
        max_x, max_y = self.get_max(Main.solutions_data)
        for k,v in Main.solutions_data.items():
            # TODO: Look into direct mapping instead of grid mode
            # generate the position of the circles the +3 is to remove the clipping
            x_position = ((canvas.width-radius/2)/(max_x+1))*v[2]+canvas.width/100
            # minusing 10 to add a button at the bottom, along with allowing space for the circles
            y_position = ((canvas.height-10-radius/2)/(max_y+1))*v[3]+canvas.width/100
            canvas.create_oval(x_position, y_position, x_position+radius, y_position+radius, fill=color)
            # labelling the circles
            label = tk.Label(canvas, text=k, bg=color)
            canvas.create_window(x_position+(radius/2), y_position+15, window=label)
            # creating the entry boxes and tying them to the solutions data dictionary (this is 4 on the list)
            Main.solutions_data[k].append(tk.Entry(canvas, width="10"))
            canvas.create_window(x_position+(radius/2), y_position+(radius/2), window=Main.solutions_data[k][4])

    def get_max(self, dictionary):
        max_x = 0
        max_y = 0
        for k, v in dictionary.items():
            if v[2] > max_x:
                max_x = v[2]
            if v[3] > max_y:
                max_y = v[3]

        return max_x, max_y

    def add_solutions(self):
        #TODO add add_solutions functionality
        print("hi")
        pass

    def save_solutions(self):
        #TODO add save_solutions functionality
        pass

    def check_entry(self, entry):
        try:
            float(entry)
            return True
        except:
            return False

    def eppendorf_circles(self, canvas):
        radius = 10
        max_x, max_y = self.get_max(Main.eppendorf_data)
        for k,v in Main.eppendorf_data.items():
            # generate the position of the circles
            #TODO: Look into direct mapping instead of grid mode
            x_position = ((canvas.width-radius)/(max_x+1))*v[2]
            y_position = ((canvas.height-radius)/(max_y+1))*v[3]
            # instantiate the buttons as false and write to eppendorf data (this is 4 on the list)
            Main.eppendorf_data[k].append(False)
            # write the button object to the eppendorf data (this is 5 on the list)
            Main.eppendorf_data[k].append(canvas.create_oval(x_position, y_position, x_position+radius, y_position+radius, fill=unselected_color))
            canvas.tag_bind(Main.eppendorf_data[k][5], "<Button-1>", lambda event, k=k, canvas=canvas: self.eppendorf_toggle(canvas, k))
            solutions_dictionary = {}
            for solutions, value in Main.solutions_data.items():
                solutions_dictionary[solutions] = 0
            Main.eppendorf_data[k].append(solutions_dictionary)

    # toggles the value of the eppendorf button and runs the set color function
    def eppendorf_toggle(self, canvas, k):
        if self.info_frame:
            self.clear_eppendorf_toggle()
            self.eppendorf_label.config(text=k)
            Main.eppendorf_data[k][4] = True
            for solutions, volume in Main.eppendorf_data[k][6].items():
                Main.solutions_data[solutions][5].delete(0, "end")
                Main.solutions_data[solutions][5].insert(0, str(volume))
        else:
            if Main.eppendorf_data[k][4]:
                Main.eppendorf_data[k][4] = False
            else:
                Main.eppendorf_data[k][4] = True
        self.set_color()

    def clear_eppendorf_toggle(self):
        for k, v in Main.eppendorf_data.items():
            Main.eppendorf_data[k][4] = False

    def set_color(self):
        for k,v in Main.eppendorf_data.items():
            if Main.eppendorf_data[k][4]:
                self.eppendorf_canvas.itemconfig(Main.eppendorf_data[k][5], fill=selected_color)
            else:
                self.eppendorf_canvas.itemconfig(Main.eppendorf_data[k][5], fill=unselected_color)

    # this is just code to change the frames and toggle the button text
    def toggle_info_frame(self):
        if not self.info_frame:
            self.info_frame = True
            self.clear_eppendorf_toggle()
            self.information_toggle_button.config(text="Solutions")
            for k, v in Main.solutions_data.items():
                Main.solutions_data[k][5].delete(0, 'end')
            self.set_color()
            self.information_frame.tkraise()
        else:
            self.info_frame = False
            self.clear_eppendorf_toggle()
            self.information_toggle_button.config(text="Information")
            for k, v in Main.solutions_data.items():
                Main.solutions_data[k][4].delete(0, 'end')
            self.set_color()
            self.solutions_frame.tkraise()

    def change_configs(self, temp):
        # TODO create a window to select the config file to select
        pass

    def save_to_file(self):
        # TODO write the save to file function or pass this to a wrapper
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