# import GUI libraries
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import math
from fl_city_analyzer import raincatcher

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

class HVAC_sizer_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        """
        GUI Setup
        """

        # set up root window
        self.title('HVAC sizer')
        self.geometry('500x350')
        self.resizable(True, True)

        # create a tabview for different sizers
        self.my_tab = ctk.CTkTabview(self, width = 500, height = 350,
                                     anchor = 'nw')
        self.my_tab.pack(padx = 10, pady = 10)

        # create tabs
        self.tab_1 = self.my_tab.add('Ductsizer')
        self.tab_2 = self.my_tab.add('Pipesizer')
        self.tab_3 = self.my_tab.add('Roof Drainsizer')
            
        """
        create function for duct sizing based on inputs
        """
        def duct_sizing(*args):
            try:
                # get the airflow, friction, and velocity values
                airflow = round(float(self.airflow_combo.get()), 2)
                friction = round(float(self.friction_combo.get()), 2)
                velocity = round(float(self.velocity_combo.get()), 2)

                # set up list for factors of rectangular area
                factor_list = []

                # set up calculation testcases for loop and stop program from crashing
                min_velocity = 1.0
                if velocity < min_velocity:
                    velocity = min_velocity
                if velocity > 0:
                    area = int((airflow/velocity)/(friction**2))
                if area % 2 != 0:
                    area +=1
                
                elif area > 3000:
                    area = 3000
                for height in range(4, area+1):
                    for width in range(4, area+1):
                        if (height*width == area) and height <= width:
                            factor_list.append((width, height))
                
                # clear old spinboxes
                for widget in self.ductsizer_frame.grid_slaves():
                    if int(widget.grid_info()['row']) >= 4:
                        widget.grid_forget()
                
                # dynamically generate spinboxes for each width-height pair
                for i, (width, height) in enumerate(factor_list):
                    # set height and width inputs 
                    if width % 2 != 0:
                        width += 1
                    if height % 2 != 0:
                        height += 1
                    
                    self.rec_w = tk.IntVar(value = width)
                    self.rec_h = tk.IntVar(value = height)

                    # width spinbox
                    tk.Spinbox(self.ductsizer_frame,
                                font = ('Arial', 12), width = 4,
                                from_ = 0, to = 200, increment=2,
                                textvariable = self.rec_w,
                                validate='key', validatecommand=self.vcmd).grid(row = i+3, column = 4, pady = 5, sticky = 'w')
                
                    # separator
                    self.x_figure_text = '×'
                    self.x_label = ctk.CTkLabel(self.ductsizer_frame, text = self.x_figure_text,
                                            font = ('Arial', 18))
                    self.x_label.grid(row = i+3, column = 5, pady = 5, sticky = 'ew')      

                    # height spinbox
                    tk.Spinbox(self.ductsizer_frame,
                                font = ('Arial', 12), width = 4,
                                from_ = 0, to = 100, increment=2,
                                textvariable = self.rec_h,
                                validate='key', validatecommand=(self.vcmd, '%S')).grid(row = i+3, column = 6, pady = 5, sticky = 'e')
                
                # Calculate the round duct diameter
                round_duct_diameter = round((math.sqrt((4*airflow) / (math.pi*velocity)))/friction, 0)
                round_duct_diameter = int(round_duct_diameter)
                if round_duct_diameter % 2 != 0:
                    round_duct_diameter += 1

                # Dynamically update the spinbox value
                self.roudo.set(round_duct_diameter)

            except Exception as e:
                print(e) 

        # create function for pipe sizing
        def pipesizer(*args):
            pass
        
        """
        create function for roof drain sizing 
        """

        def rdrainsizer(*args): 
            # get inputs
            roof_area = float(self.roof_area_spinbox.get())
            parapet_area = float(self.parapet_area_spinbox.get())
            total_area = roof_area + parapet_area

            # select gpmpsf based on city
            rain_data = raincatcher()
            current_city = self.city_combo.get()
            for (city, rainfall) in (rain_data):
                if city == current_city:
                    gpmpsf = rainfall            

            # find GPM
            gpm = total_area*gpmpsf
            print(f'GPM: {gpm}')

            # find drain size based on GPM (pipe diameter, GPM)
            leader_GPMs = [(2, 30), (2.5, 54), (3, 92), (4, 192), (5, 360), (6, 563), (8, 1208)]

            for i, (pipe_diameter, GPM) in enumerate(leader_GPMs):
                if gpm < GPM:
                    # dynamically update the roof drain pipe diameter
                    print(f'Pipe Diameter: {pipe_diameter}')
                    self.pipe_diameter.set(pipe_diameter)
                    break

        """
        set up input field validator for only integers
        """
        self.vcmd = (self.register(self.validate_input), '%P')      

        """
        Set up the ductsizer
        """
        # set up frame to hold duct widgets
        self.ductsizer_frame = ctk.CTkFrame(self.tab_1, corner_radius=10, width = 500, height = 350)
        self.ductsizer_frame.grid(row = 0, column = 0, padx = 5)

        # set up airflow fields
        self.airflow_label = ctk.CTkLabel(self.ductsizer_frame,
                                          text = 'Airflow (CFM)')
        self.airflow_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'n')

        self.default_airflow = tk.IntVar(master = self.ductsizer_frame, value = 700)

        self.airflow_combo = tk.Spinbox(self.ductsizer_frame, width = 8, font = ('Arial', 14),
                                        textvariable=self.default_airflow, validate='key', validatecommand= self.vcmd)
    
        self.airflow_combo.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'e')

        # set up static friction fields
        self.friction_label = ctk.CTkLabel(self.ductsizer_frame, 
                                           text = 'Static Friction')
        self.friction_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'n')

        self.default_friction = tk.DoubleVar(master = self.ductsizer_frame, value = 0.08)
        self.friction_combo = tk.Spinbox(self.ductsizer_frame, font = ('Arial', 14),
                                           width = 8, textvariable=self.default_friction,
                                           validate='key', validatecommand= self.vcmd)
        self.friction_combo.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'n')

        self.friction_checkbox = ctk.CTkCheckBox(self.ductsizer_frame, text = '')
        self.friction_checkbox.grid(row = 2, column  = 2, padx = 5, pady = 5, sticky = 'n')

        # set up velocity fields
        self.velocity_label = ctk.CTkLabel(self.ductsizer_frame,
                                           text = 'Velocity (FPM)',
                                           font = ('Arial', 12))
        self.velocity_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'n')

        self.default_velocity = tk.IntVar(master = self.ductsizer_frame, value = 800)
        self.velocity_combo = tk.Spinbox(self.ductsizer_frame, width = 8, font = ('Arial', 14),
                                        textvariable = self.default_velocity,
                                        validate='key', validatecommand = self.vcmd)

        self.velocity_combo.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'n')

        self.velocity_checkbox = ctk.CTkCheckBox(self.ductsizer_frame, text = '')
        self.velocity_checkbox.grid(row = 3, column  = 2, padx = 5, pady = 5, sticky = 'n')

        # set up round duct fields
        self.round_duct_header = ctk.CTkLabel(self.ductsizer_frame,
                                              text = 'Round (in)', font = ('Arial',16))
        self.round_duct_header.grid(row =  0, column = 4, pady = 5, sticky = 'w')

        # initialize output variables
        self.roudo = tk.IntVar()
        self.rec_w = tk.IntVar()
        self.rec_h = tk.IntVar() 

        self.round_duct_output = tk.Spinbox(self.ductsizer_frame,
                                                      font = ('Arial', 12), width = 4,
                                                      from_ = 2, to = 100, increment=2,
                                                      textvariable = self.roudo, 
                                                      validate='key', validatecommand=self.vcmd)
        self.round_duct_output.grid(row = 1, column = 4, pady = 5, sticky = 'nw')

        # set rectangular duct header
        self.rectangular_duct_header = ctk.CTkLabel(self.ductsizer_frame,
                                              text = 'Rectangular (in)', font = ('Arial', 16))
        self.rectangular_duct_header.grid(row =  2, column = 4, pady = 5, sticky = 'w')

        # bind the airflow, friction, and velocity to update the rectangular and round duct size
        self.airflow_combo.bind('<KeyRelease>', lambda event: duct_sizing())
        self.friction_combo.bind('<KeyRelease>', lambda event: duct_sizing())
        self.velocity_combo.bind('<KeyRelease>', lambda event: duct_sizing())

        """
        Set up the pipesizer
        """ 


        """
        Set up roof drainsizer
        """
        # set up the roof drain sizing frame
        self.rdrainsizer_frame = ctk.CTkFrame(self.tab_3, corner_radius=10, width = 500, height = 350)
        self.rdrainsizer_frame.grid(row = 0, column = 0, padx = 5)

        #instantiate variables
        self.roof_area = tk.DoubleVar()
        self.parapet_area = tk.DoubleVar()
        self.pipe_diameter = tk.DoubleVar()

        # set up roof area fields
        self.roof_area_label = ctk.CTkLabel(self.rdrainsizer_frame, 
                                            text = 'Roof Area (ft^2)', font = ('Arial', 12))
        self.roof_area_label.grid(row = 0, column = 0)

        self.roof_area_spinbox = tk.Spinbox(self.rdrainsizer_frame,
                                            from_ = 0, to = 10000,
                                            width = 6,
                                            font = ('Arial', 12),
                                            textvariable= self.roof_area,                                            
                                            validate = 'key', validatecommand=self.vcmd)
        self.roof_area_spinbox.grid(row = 0, column = 1, pady = 5, sticky = 'w')

        # set up parapet area fields
        self.parapet_area_label = ctk.CTkLabel(self.rdrainsizer_frame, 
                                               text = 'Parapet Area (ft^2)', font = ('Arial', 12))
        self.parapet_area_label.grid(row = 1, column = 0)

        self.parapet_area_spinbox = tk.Spinbox(self.rdrainsizer_frame,
                                               from_ = 0, to = 10000,
                                               width = 6,
                                               font = ('Arial', 12),
                                               textvariable= self.parapet_area,
                                               validate = 'key', validatecommand=self.vcmd)
        self.parapet_area_spinbox.grid(row = 1, column = 1, pady = 5, sticky = 'w')

        # set up climate zone fields
        self.climate_zone_header = ctk.CTkLabel(self.rdrainsizer_frame,
                                                text = 'Climate Zone', font = ('Arial', 12))
        self.climate_zone_header.grid(row = 2, column = 0, pady = 5, sticky = 'w')

        self.climate_zones = ['select a climate zone', 
                        '0A', '0B', '1A', '1B',
                         '2A', '2B', '3A', '3B',
                         '3C', '4A', '4B', '4C',
                         '5A', '5B', '5C', '6A',
                         '6B', '7', '8']
        self.climate_zone_combo = ctk.CTkComboBox(self.rdrainsizer_frame, 
                                                  width = 160, height = 20,
                                                  values = self.climate_zones, command = self.state_selector)
        self.climate_zone_combo.grid(row = 2, column = 1, pady = 5, sticky = 'w')

        # set up state fields
        self.state_header = ctk.CTkLabel(self.rdrainsizer_frame,
                                                text = 'State', font = ('Arial', 12))
        self.state_header.grid(row = 3, column = 0, pady = 5, sticky = 'w')

        self.states = ['select a state: ']

        self.state_combo = ctk.CTkComboBox(self.rdrainsizer_frame, 
                                                  width = 120, height = 20,
                                                  values = self.states, command = self.city_selector,
                                                  state = NORMAL)
        self.state_combo.grid(row = 3, column = 1, pady = 5, sticky = 'w')

        # set up city fields
        self.city_header = ctk.CTkLabel(self.rdrainsizer_frame,
                                                text = 'City', font = ('Arial', 12))
        self.city_header.grid(row = 4, column = 0, pady = 5, sticky = 'w')

        self.cities = ['select a city: '] 
        self.city_combo = ctk.CTkComboBox(self.rdrainsizer_frame, 
                                                  width = 140, height = 20,
                                                  values = self.cities,
                                                  state = NORMAL)
        self.city_combo.grid(row = 4, column = 1, pady = 5, sticky = 'w')

        # set up roof drain size fields
        self.roof_drain_size_header = ctk.CTkLabel(self.rdrainsizer_frame,
                                                   text = 'Roof Drain Size', font = ('Arial', 12))
        self.roof_drain_size_header.grid(row = 0, column = 4, pady = 5, sticky = 'n')
        
        self.roof_drain_spinbox = tk.Spinbox(self.rdrainsizer_frame,
                                             width=10,
                                             font = ('Arial', 12),
                                             from_ = 2, to = 8,
                                             textvariable = self.pipe_diameter,
                                             validate= 'key', validatecommand=(self.vcmd, '%S'))
        self.roof_drain_spinbox.grid(row = 1, column = 4, pady = 5, sticky = 'n')

        # bind the roof area, parapet area, and roof drain pipe size to update the rectangular and round duct size
        self.roof_area_spinbox.bind('<KeyRelease>', lambda event: rdrainsizer())
        self.parapet_area_spinbox.bind('<KeyRelease>', lambda event: rdrainsizer())

    # prevent user from entering non-integers
    def validate_input(self, text):
        if text == "":
            return True
        if text.isdigit() or (text.count('.') == 1 and all(part.isdigit() for part in text.split('.'))):
            return True
        return False
        
    def state_selector(self, *args):
        # select state based on climate zone
        climate_zone = self.climate_zone_combo.get()
        if climate_zone == '2A':
            state_values = ['Florida', 'Colorado', 'Montana', 'Nevada', 'Wyonming']
        elif climate_zone == '3A':
            state_values = ['Oregon', 'Washington', 'Idaho', 'Utah',
                            'New Mexico', 'Arizona']
        elif climate_zone == '3B':
            state_values = ['Texas', 'California', 'New Mexico', 'Nevada',
                            'Arizona']
        if state_values not in self.states:
            self.states = ['Select a State: ']
            self.states += state_values
        self.state_combo.configure(values = self.states)

    def city_selector(self, *args):
        # update city selection based on state
        state = self.state_combo.get()
        if state == 'Florida':
            rain_data = raincatcher()
            self.cities = ['select a city: ']
            for city, gpmpsf in rain_data:
                if city not in self.cities:
                    # updated city spinbox with rain data
                    self.cities.append(city)
            self.city_combo.configure(values = self.cities)
       
app = HVAC_sizer_GUI()
app.mainloop()
