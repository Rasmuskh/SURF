import serial                            



class Pump:
    #command helper function
    def command(self, cmd):
        self.ser.write(self.port+cmd+"R\r")
        self.ser.readlines()
    #query helper function
    def query(self, q):
        self.ser.write(self.port+q+"R\r")
        response = self.ser.readlines()
        return response[0][4:-3]

    #===========================#
    #Pump Configuration Commands#
    #===========================#
    #Toggle microstep mode off/on
    def microstepmode(self, n):
        cmd = "N%s" %n
        self.command(cmd)
    def backlash_increments(self, n):
        cmd = "K%s" %n
        self.command(cmd)


    #=======================#
    #Initialization Commands#
    #=======================#
    #Constructor
    def __init__(self,port = "/1", polarity=0):
        self.port = port
        print(port)
        self.ser = serial.Serial(port = '/dev/ttyUSB0',
                    baudrate = 9600,      
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,                         
                    timeout = 2)               
        if polarity == 0:
            print("clockwise")
            self.init_plunger_and_valve_clockwise()
        if polarity == 1:
            print("counter clockwise")
            self.init_plunger_and_valve_counter_clockwise()

    
    def init_plunger_and_valve_clockwise(self, n1=1, n2=1, n3=1):
        cmd = "Z,%s,%s,%s" %(n1, n2, n3)
        self.command(cmd)
    def init_plunger_and_valve_counter_clockwise(self, n1=1, n2=1, n3=1):
        cmd = "Y,%s,%s,%s" %(n1, n2, n3)
        self.command(cmd)
    def plunger_drive(self,n=1):
        cmd = "W%s" %n
        self.command(cmd)
    def valve_drive(self,n1=1,n2=1):
        cmd = "w%s,%s" %(n1, n2)
        self.command(cmd)
    def simulated_plunger_initialization(self):
        self.command("z")
        
    #==============#
    #Value Commands#
    #==============#
    #Valve toggling commands for non-distribution valves (syringe, input and output port).
    def move_valve_to_input_port(self):
        self.command("I")
    def move_valve_to_output_port(self):
        self.command("O")
    def move_valve_to_bypass_position(self):
        self.command("B")

    #=========================#
    #Plunger Movement Commands#
    #=========================#
    def move_plunger_absolute_position(self,n):
        cmd = "A%s" %n
        self.command(cmd)
    def move_plunger_relative_position(self,n):
        if n<0:
            n = abs(n)
            cmd = "P%s" %n
        else:
            cmd = "D%s" %n
        self.command(cmd)

    #===============================#
    #Speed and Acceleration Commands#
    #===============================#
    def set_slope(self, n):
        cmd = "L%s" %n
        self.command(cmd)
    def set_start_speed(self, n):
        cmd = "v%s" %n
        self.command(cmd)
    def set_top_speed(self, n):
        cmd = "V%s" %n
        self.command(cmd)
    def set_cutoff_speed(self, n):
        cmd = "c%s" %n
        self.command(cmd)
    def set_speed(self, n):
        cmd = "S%s" %n
        self.command(cmd)

    #================#
    #Control Commands#
    #================#
    def terminate_current_command(self):
        self.command("T")

    #===============#
    #Report Commands#
    #===============#
    #queries
    def get_absolute_plunger_position(self):
        return self.query("?")
    def get_start_speed(self):
        return self.query("?1")
    def get_top_speed(self):
        return self.query("?2")
    def get_cutoff_speed(self):
        return self.query("?3")
    def get_actual_plunger_position(self):
        return self.query("?4")
    def get_valve_position(self):
        return self.query("?6")
    def get_command_buffer_status(self):
        return self.query("?10")
    def get_number_of_backlash_increments(self):
        return self.query("?12")
    def get_auxiliary_input_status_1(self):
        return self.query("?13")
    def get_auxiliary_input_status_2(self):
        return self.query("?14")
    def get_number_of_pump_initializations(self):
        return self.query("?15")
    def get_number_of_plunger_movements(self):
        return self.query("?16")
    def get_number_of_valve_movements(self):
        return self.query("?17")
    def get_number_of_valve_movements_since_last_report(self):
        return self.query("?18")
    def get_firmware_checksum(self):
        return self.query("?20")
    def get_firmware_version(self):
        return self.query("?23")
    def get_the_zero_gap_increments(self):
        return self.query("?24")
    def get_slope_code_setting(self):
        return self.query("?25")
    def get_current_mode(self):
        return self.query("?28")
    def get_error_code(self):
        return self.query("?29")
    def get_pump_configuration(self):
        return self.query("?76")
    def get_voltage(self):
        return self.query("*")
    def get_user_data(self):
        return self.query("<")
