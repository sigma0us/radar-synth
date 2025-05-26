import time

lmx2572_registers_default = [
    0x00211C,  # R0
    0x010808,  # R1
    0x020500,  # R2
    0x030782,  # R3
    0x040A43,  # R4
    0x0530C8,  # R5
    0x06C802,  # R6
    0x0700B2,  # R7
    0x082000,  # R8
    0x090004,  # R9
    0x0A10F8,  # R10
    0x0BB018,  # R11
    0x0C5001,  # R12
    0x0D4000,  # R13
    0x0E1820,  # R14
    0x0F060E,  # R15
    0x100080,  # R16
    0x110096,  # R17
    0x120064,  # R18
    0x1327B7,  # R19
    0x144848,  # R20
    0x150409,  # R21
    0x160001,  # R22
    0x17007C,  # R23
    0x18071A,  # R24
    0x190624,  # R25
    0x1A0808,  # R26
    0x1B0002,  # R27
    0x1C0488,  # R28
    0x1D0000,  # R29
    0x1E18A6,  # R30
    0x1FC3E6,  # R31
    0x2005BF,  # R32
    0x211E01,  # R33
    0x220010,  # R34
    0x230004,  # R35
    0x24003C,  # R36
    0x250305,  # R37
    0x260000,  # R38
    0x2703E8,  # R39
    0x280000,  # R40
    0x290000,  # R41
    0x2A0000,  # R42
    0x2B0000,  # R43
    0x2C1FA3,  # R44
    0x2DC61F,  # R45
    0x2E07F0,  # R46
    0x2F0300,  # R47
    0x3003E0,  # R48
    0x314180,  # R49
    0x320080,  # R50
    0x330080,  # R51
    0x340421,  # R52
    0x350000,  # R53
    0x360000,  # R54
    0x370000,  # R55
    0x380000,  # R56
    0x390020,  # R57
    0x3A9001,  # R58
    0x3B0001,  # R59
    0x3C03E8,  # R60
    0x3D00A8,  # R61
    0x3E00AF,  # R62
    0x3F0000,  # R63
    0x401388,  # R64
    0x410000,  # R65
    0x4201F4,  # R66
    0x430000,  # R67
    0x4403E8,  # R68
    0x450000,  # R69
    0x46C350,  # R70
    0x470081,  # R71
    0x480001,  # R72
    0x49003F,  # R73
    0x4A0000,  # R74
    0x4B0800,  # R75
    0x4C000C,  # R76
    0x4D0000,  # R77
    0x4E0001,  # R78
    0x4F0000,  # R79
    0x500000,  # R80
    0x510000,  # R81
    0x520000,  # R82
    0x530000,  # R83
    0x540000,  # R84
    0x550000,  # R85
    0x560000,  # R86
    0x570000,  # R87
    0x580000,  # R88
    0x590000,  # R89
    0x5A0000,  # R90
    0x5B0000,  # R91
    0x5C0000,  # R92
    0x5D0000,  # R93
    0x5E0000,  # R94
    0x5F0000,  # R95
    0x600000,  # R96
    0x610000,  # R97
    0x620000,  # R98
    0x630000,  # R99
    0x640000,  # R100
    0x650000,  # R101
    0x660000,  # R102
    0x670000,  # R103
    0x680000,  # R104
    0x694440,  # R105
    0x6A0007,  # R106
    0x6B0000,  # R107
    0x6C0000,  # R108
    0x6D0000,  # R109
    0x6E0000,  # R110
    0x6F0000,  # R111
    0x700000,  # R112
    0x710000,  # R113
    0x727802,  # R114
    0x730000,  # R115
    0x740000,  # R116
    0x750000,  # R117
    0x760000,  # R118
    0x770000,  # R119
    0x780000,  # R120
    0x790000,  # R121
    0x7A0000,  # R122
    0x7B0000,  # R123
    0x7C0000,  # R124
    0x7D2288,  # R125
]




class LMX2572:  
    """  
    MicroPython driver for the LMX2572 wideband frequency synthesizer  
    
    This class provides methods to read and write registers for the LMX2572 chip  
    via SPI communication.  
    """  
    
    # Register descriptions dictionary - contains key registers and their functions  
    REGISTER_DESCRIPTIONS = {  
        0: "Main control: RAMP_EN, VCO_PHASE_SYNC_EN, FCAL settings, RESET, POWERDOWN",  
        1: "Calibration clock divider settings",  
        3: "Reset control: RESET_R123_TO_R4, etc.",  
        4: "VCO settings and charge pump settings",  
        5: "Input buffer configuration",  
        6: "LDO delay settings",  
        7: "Output force control",  
        9: "OSC doubler and divider settings",  
        10: "Charge pump linearity settings",  
        12: "Analog enables for VCO subsystem",  
        14: "VCO calibration settings",  
        17: "Charge pump settings",  
        19: "Phase detector trim settings",  
        20: "VCO calibration configuration",  
        24: "VCO subsystem configuration",  
        31: "VCO subsystem configuration",  
        36: "PLL_N: Integer division ratio",  
        37: "PLL_NUM[31:16]: Upper 16 bits of fractional numerator",  
        38: "PLL_DEN[31:16]: Upper 16 bits of fractional denominator",  
        39: "PLL_DEN[15:0]: Lower 16 bits of fractional denominator",  
        42: "PLL_NUM[31:16]: Upper 16 bits of fractional numerator",  
        43: "PLL_NUM[15:0]: Lower 16 bits of fractional numerator",  
        44: "Output power and MASH control settings",  
        45: "OUTA_MUX and OUTB_PWR settings",  
        46: "OUTB_MUX settings",  
        71: "SYSREF configuration",  
        72: "SYSREF divider",  
        108: "Status register containing VCO calibration information", 
        110: "Readback for LD_VTUNE and VCO_SEL",  
        111: "Readback for VCO_CAPCTRL",  
        112: "Readback for VCO_DACISET",  
        114: "FSK mode configuration",  
    }  
    
    # Field descriptions for selected important registers  
    FIELD_DESCRIPTIONS = {  
        0: {  
            "15": "RAMP_EN: Enables frequency ramping (0: Normal, 1: Start ramping)",  
            "14": "VCO_PHASE_SYNC_EN: Enables phase sync mode",  
            "9-8": "FCAL_HPFD_ADJ: Fast calibration high PFD adjustment",  
            "7-6": "FCAL_LPFD_ADJ: Fast calibration low PFD adjustment",  
            "4": "FCAL_EN: Enables fast calibration (writing 0 is prohibited)",  
            "2": "MUXOUT_LD_SEL: MUXout function (0: Register readback, 1: Lock detect)",  
            "1": "RESET: Reset device (0: Normal operation, 1: Reset - self-clearing)",  
            "0": "POWERDOWN: Power down device (0: Normal operation, 1: Power down)"  
        },  
        3: {  
            "3": "RESET_R123_TO_R4: When set, R4-R123 load from predefined state",  
        },  
        36: {  
            "15-0": "PLL_N: Integer division ratio"  
        },  
        44: {  
            "15-12": "OUTA_PWR: Output A power level",  
            "11": "OUTB_PD: Output B power down",  
            "10": "OUTA_PD: Output A power down",  
            "9": "MASH_RESET_N: MASH reset (active low)",  
            "2-0": "MASH_ORDER: MASH modulator order (0: Integer-N, 1: MASH1, 2: MASH2, 3: MASH3, 4: MASH4)"  
        },  
        45: {  
            "15-12": "OUTA_MUX: Output A multiplexer",  
            "3-0": "OUTB_PWR: Output B power level"  
        },  
        110: {  
            "10-9": "rb_LD_VTUNE: Vtune lock detect (0/1: Unlocked, 2: Locked, 3: Invalid)",  
            "7-5": "rb_VCO_SEL: Selected VCO (1-6)"  
        }  
    }  
    
    def __init__(self, spi, cs, en, ref_freq=100e6,verbose=False):  
        """  
        Initialize the LMX2572 driver  
        
        Args:  
            spi: Initialized SPI object  
            cs_pin: Chip select pin object (active low)  
            pll_select_pin: Pin used to select between synthesizers  
            synthesizer_type: 'txs' or 'los' to indicate which synthesizer this instance represents  
            ref_freq: Reference frequency in Hz  
        """  
        self.spi = spi  
        self.cs = cs 
        self.en = en
    

        #Iniitiale conditions
        #self.cs.value(1)  # CS is active low, so set it high initially  
        self.en.value(0)  # ENsure its off to start synthesizer
      
        self.is_enabled = False  # Track if the chip is enabled
        
        # Initialize the register values from the provided array  
        self.registers = {}  
        self.ref_freq = ref_freq  
        self.pfd_freq = ref_freq 

        self.verbose = verbose  # Verbose output flag

 
        
    def setup(self, port="A", power=50):  
        """  
        Debug configuration method with simplified output port setup  
        
        Args:  
            port: 'A' or 'B' to specify which port to enable (default: 'A')  
        """  
        self.reset()  
        time.sleep(0.1)  
        self.configure_default()  
        self.set_ref()  
        self.set_osc_single_ended()  
        time.sleep(0.1)  
        
        # Normalize port to uppercase  
        port = port.upper()  
        
        if port == "A":  
            # Enable port A with power 50, disable port B  
            self.set_output_port(['A'])  
            self.set_output_power('A', power)  
        else:  
            # Enable port B with power 50, disable port A  
            self.set_output_port(['B'])  
            self.set_output_power('B', power) 

        time.sleep(0.1)
        self.set_freq(5.87e9)  
        return self.is_locked()
    

    def enable(self):  
        """  
        Enable the LTC5594 by setting the enable pin high  
        """  
        if not self.en:  
            return  
        
        if not self.is_enabled:
            self.en.on()  
            self.is_enabled = True

        time.sleep_ms(10)  # Allow device to initialize  

    def disable(self):
        """  
        Disable the LTC5594 by setting the enable pin low  
        """  
        if not self.en:  
            return  
        
        if self.is_enabled:
            self.en.off()  
            self.is_enabled = False

        time.sleep_ms(10)
          
    
    def configure_default(self, registers=None, reverse=True):  
        """  
        Configure device with default register values  
        
        Args:  
            registers: List of register data in format [(addr << 16) | value]  
                    If None, uses lmx2572_registers_default  
            reverse: If True, writes registers in reverse order (highest address first)  
                    If False (default), writes in original list order  
        """  
        if registers is None:  
            registers = lmx2572_registers_default  
        
        # Create a copy of the registers list to avoid modifying the original  
        reg_list = list(registers)  
    
        # Reverse the list if requested  
        if reverse:  
            reg_list.reverse()  
        
        for reg_data in reg_list:  
            reg_addr = (reg_data >> 16) & 0x7F  # Extract address from upper byte  
            reg_value = reg_data & 0xFFFF       # Extract 16-bit value  
            self.write_register(reg_addr, reg_value)
        
    
    def write_register(self, reg_addr, data):  
        """  
        Write data to a register  
        
        Args:  
            reg_addr: Register address (0-127)  
            data: 16-bit data to write  
        """  

        # Update local register cache  
        self.registers[reg_addr] = data  
        
        # Format: [R/W bit (0) + 7-bit address + 16-bit data]  
        # R/W bit 0 = write  
        msg = bytearray(3)  
        msg[0] = reg_addr & 0x7F  # 7-bit address, R/W bit = 0 for write  
        msg[1] = (data >> 8) & 0xFF  # Upper 8 bits of data  
        msg[2] = data & 0xFF  # Lower 8 bits of data  
        
        self.cs.value(0)  # Pull CS low to begin transaction  
        self.spi.write(msg)  
        self.cs.value(1)  # Pull CS high to end transaction  
    
    def read_register(self, reg_addr):  
        """  
        Read data from a register  
        
        Args:  
            reg_addr: Register address (0-127)  
            
        Returns:  
            16-bit register data  
        """  
        
        # Check if register is a special case  
        if reg_addr in [55, 110, 111, 112]:  
            print(f"Note: Register R{reg_addr} is a special status register")  
            
        # Check if readback is enabled  
        r0_value = self.registers.get(0, 0)  
        if (r0_value & 0x4) != 0:  # Check if MUXOUT_LD_SEL (bit 2) is set  
            print("Warning: Register readback is disabled. Enabling temporarily.")  
            # Store original value  
            orig_r0 = r0_value  
            # Clear bit 2 temporarily  
            self.write_register(0, r0_value & ~0x4)  
        
        # Format: [R/W bit (1) + 7-bit address] followed by 16 dummy bits  
        # R/W bit 1 = read  
        tx_data = bytearray(3)  
        tx_data[0] = (reg_addr & 0x7F) | 0x80  # 7-bit address, R/W bit = 1 for read  
        tx_data[1] = 0  # Dummy bytes for reading  
        tx_data[2] = 0  
        
        rx_data = bytearray(3)  
        
        # Ensure CS is initially high  
        self.cs.value(1)  
        
        # Perform read operation with proper timing  
        self.cs.value(0)  # Pull CS low to begin transaction  
        self.spi.write_readinto(tx_data, rx_data)  
        self.cs.value(1)  # Pull CS high to end transaction  
        
        # Extract the 16-bit data (last 2 bytes)  
        reg_value = (rx_data[1] << 8) | rx_data[2]  
        
        # If we temporarily enabled readback, restore original R0 value  
        if 'orig_r0' in locals():  
            self.write_register(0, orig_r0)  
        
        # Update local register cache  
        self.registers[reg_addr] = reg_value  
        
        return reg_value  
    
    def enable_readback(self):  
        """Enable register readback by clearing MUXOUT_LD_SEL bit in R0"""  
        r0_value = self.registers.get(0, 0x221C)  
        # Clear bit 2 (MUXOUT_LD_SEL) to enable readback  
        new_r0_value = r0_value & ~0x4  
        
        print(f"Enabling register readback. R0: 0x{r0_value:04X} → 0x{new_r0_value:04X}")  
        self.write_register(0, new_r0_value)  
        
        return new_r0_value  
    
    def disable_readback(self):  
        """Disable register readback by setting MUXOUT_LD_SEL bit in R0"""  
        r0_value = self.registers.get(0, 0x221C)  
        # Set bit 2 (MUXOUT_LD_SEL) to disable readback and enable lock detect on MUXOUT  
        new_r0_value = r0_value | 0x4  
        
        print(f"Disabling register readback. R0: 0x{r0_value:04X} → 0x{new_r0_value:04X}")  
        self.write_register(0, new_r0_value)  
        
        return new_r0_value  
    
    
    def reset(self):  
        """Reset the device by setting the RESET bit in R0"""  
        # Get current R0 value, set RESET bit, preserve other bits  
        r0_value = self.registers.get(0, 0x221C)  # Default if not available  
        self.write_register(0, r0_value | 0x2)  # Set RESET bit (bit 1)  
    
    def power_down(self, enable=True):  
        """Power down the device"""  
        # Get current R0 value  
        r0_value = self.registers.get(0, 0x221C)  # Default if not available  
        
        if enable:  
            # Set POWERDOWN bit  
            self.write_register(0, r0_value | 0x1)  
        else:  
            # Clear POWERDOWN bit  
            self.write_register(0, r0_value & ~0x1)  
    

    
    def dump_registers(self, start_reg=0, end_reg=125):  
        """  
        Read and display all register values in hex format  
        
        Args:  
            start_reg: Starting register address (default: 0)  
            end_reg: Ending register address (default: 125)  
        """  
        print("LMX2572 Register Dump (Hex Values)")  
        print("==================================")  
        
        # Check if readback is enabled, enable it temporarily if needed  
        r0_value = self.registers.get(0, 0)  
        readback_disabled = False  
        if (r0_value & 0x4) != 0:  # Check if MUXOUT_LD_SEL (bit 2) is set  
            print("Enabling register readback temporarily")  
            orig_r0 = r0_value  
            self.write_register(0, r0_value & ~0x4)  
            readback_disabled = True  
        
        # Print register values in groups of 4 per line  
        for i in range(start_reg, end_reg + 1, 4):  
            values = []  
            for reg_addr in range(i, min(i + 4, end_reg + 1)):  
                try:  
                    reg_value = self.read_register(reg_addr)  
                    values.append(f"R{reg_addr:03d}=0x{reg_value:04X}")  
                except Exception as e:  
                    values.append(f"R{reg_addr:03d}=ERROR")  
            
            print(" | ".join(values))  
        
        # Restore original R0 if we temporarily enabled readback  
        if readback_disabled:  
            self.write_register(0, orig_r0)  
            print("Restored original register readback setting")  


    def simple_register_dump(self):  
        """Minimal register dump showing hex values only"""  
        
        # Enable readback if needed  
        r0 = self.read_register(0)  
        readback_was_disabled = False  
        if (r0 & 0x4) != 0:  
            self.write_register(0, r0 & ~0x4)  
            readback_was_disabled = True  
            
        # Read and display all registers  
        for reg in range(126):  
            value = self.read_register(reg)  
            print(f"R{reg:03d}: 0x{value:04X}")  
            
        # Restore original state  
        if readback_was_disabled:  
            self.write_register(0, r0)  


    def set_output(self, enable_a=True, power_a=40, enable_b=False, power_b=40):  
        """  
        Configure the output settings for the LMX2572  
        
        Args:  
            enable_a: Boolean, True to enable output A, False to disable  
            power_a: Integer (0-63), power level for output A  
            enable_b: Boolean, True to enable output B, False to disable  
            power_b: Integer (0-63), power level for output B  
            
        Returns:  
            0 on success  
        """  
        # Ensure power values are in valid range (6 bits, 0-63)  
        power_a &= 0x3F  
        power_b &= 0x3F  
        
        # Configure register 44 for output A  
        reg44 = 0x22 | (power_a << 8)  
        if not enable_a:  
            reg44 |= 0x40  # Set bit 6 to disable output A  
        if not enable_b:  
            reg44 |= 0x80  # Set bit 7 to disable output B  
        
        # Write register 44  
        self.write_register(44, reg44)  
        
        # Configure and write register 45 for output B  
        # Preserve upper bits, set lower 6 bits to power_b  
        reg45 = (self.registers.get(45, 0) & 0xFFC0) | power_b  
        self.write_register(45, reg45)  
        
        return 0
    
    def set_output_port(self, ports):  
        """  
        Enable or disable output ports for the synthesizer  
        
        Args:  
            ports: List of ports to enable. Can be ['A'], ['B'], or ['A', 'B']  
        
        Returns:  
            0 on success  
        """  
        if not isinstance(ports, list):  
            raise ValueError("Ports must be provided as a list")  
        
        ports = [port.upper() for port in ports]  
        
        if 'A' not in ports and 'B' not in ports:  
            raise ValueError("At least one port must be specified")  
        
        # Use the existing set_output method with appropriate parameters  
        if 'A' in ports and 'B' in ports:  
            return self.set_output(enable_a=True, enable_b=True)  
        elif 'A' in ports:  
            return self.set_output(enable_a=True, enable_b=False)  
        else:  # 'B' in ports  
            return self.set_output(enable_a=False, enable_b=True)  

    def set_output_power(self, port, power):  
        """  
        Set the power level for a specific output port  
        
        Args:  
            port: 'A' or 'B'  
            power: Integer power level (0-63)  
        
        Returns:  
            0 on success  
        """  
        port = port.upper()  
        if port not in ['A', 'B']:  
            raise ValueError("Port must be 'A' or 'B'")  
        
        power = int(power)  
        if power < 0 or power > 63:  
            raise ValueError("Power must be between 0 and 63")  
        
        # Use the existing set_output method with appropriate parameters  
        if port == 'A':  
            return self.set_output(power_a=power, enable_a=True, enable_b=False)  
        else:  
            return self.set_output(power_b=power, enable_a=False, enable_b=True)
        
    def is_locked(self):  
        """  
        Check if the PLL is locked by reading the digital lock detect status  
        
        Returns:  
            Boolean: True if the PLL has achieved digital lock, False otherwise  
        """  
        # Ensure readback is enabled  
        r0_value = self.registers.get(0, 0x221C)  
        temp_enable_readback = False  
        
        if (r0_value & 0x4) != 0:  # Check if MUXOUT_LD_SEL (bit 2) is set  
            # Temporarily enable readback  
            temp_enable_readback = True  
            original_r0 = r0_value  
            self.write_register(0, r0_value & ~0x4)  
        
        # Read the status register  
        status = self.read_register(110)  
        
        # Restore original R0 value if we modified it  
        if temp_enable_readback:  
            self.write_register(0, original_r0)  
        
        # Check bits [10:9] for digital lock detect (value of 2)  
        return ((status >> 9) & 3) == 2  

    
    def read_bit(self, reg_addr, bit_pos):
        """  
        Read a specific bit from a register  
        
        Args:  
            reg_addr: Register address (0-127)  
            bit_pos: Bit position to read (0-15)  
            
        Returns:  
            Boolean: True if the bit is set, False otherwise  
        """  
        # Read the register value  
        reg_value = self.read_register(reg_addr)  
        
        # Extract the specified bit and return its value  
        return (reg_value >> bit_pos) & 1 == 1
    
    def set_bit(self, reg_addr, bit_pos, value):
        """  
        Set or clear a specific bit in a register  
        
        Args:  
            reg_addr: Register address (0-127)  
            bit_pos: Bit position to set/clear (0-15)  
            value: Boolean value to set (True for set, False for clear)  
            
        Returns:  
            0 on success, -1 on failure  
        """  
        # Read the current register value  
        reg_value = self.read_register(reg_addr)  
        
        # Set or clear the specified bit based on the value argument  
        if value:  
            reg_value |= (1 << bit_pos)
        else:
            reg_value &= ~(1 << bit_pos)
        # Write the modified value back to the register
        self.write_register(reg_addr, reg_value)
        return 0 if value else -1  # Return 0 on success, -1 on failure
    


    
    def set_ref(self, doubler=False, pre_R=1, multiplier=1, R=1, diff=False):  
        """  
        Configure the reference path of the LMX2572  
        
        Args:  
            ref_freq: Reference frequency in Hz  
            doubler: True to enable the frequency doubler  
            pre_R: Pre-R divider value (12-bit)  
            multiplier: Frequency multiplier (5-bit)  
            R: R divider value (8-bit)  
            diff: True for differential input, False for single-ended (default)  
            
        Returns:  
            0 on success  
        """  
        # Apply doubler if enabled  
        if doubler:  
            self.ref_freq *= 2  
        
        # Apply bit masks to ensure valid values  
        pre_R &= 0xFFF      # 12-bit pre-R  
        multiplier &= 0x1F   # 5-bit multiplier  
        R &= 0xFF           # 8-bit R  
        
        # Calculate PFD frequency  
        self.pfd_freq = self.ref_freq * multiplier // pre_R // R  
        
        # Configure register 11 (R divider)  
        self.registers[11] = 0xB008 | (R << 4)  
        
        # Configure register 10 (multiplier and pre-R)  
        self.registers[10] = 0x1078 | (multiplier << 7)  
        
        # Configure register 9 (doubler and high/low frequency selector)  
        self.registers[9] = 0x4  
        if doubler:  
            self.registers[9] |= 0x1000  
        if self.pfd_freq > 100000000:  # 100 MHz threshold  
            self.registers[9] |= 0x4000  
        
        # Write registers 9-11  
        for i in range(9, 12):  
            self.write_register(i, self.registers[i])  
        
        # Configure register 5 for differential/single-ended input  
        self.registers[5] = 0x28C8 if diff else 0x30C8  
        self.write_register(5, self.registers[5])  
        
        return 0  
    

    def set_freq(self, freq, sync_en=False, force_vco=False):  
        """  
        Configure LMX2572 to output the specified frequency  
        
        Args:  
            freq: Desired output frequency in Hz  
            sync_en: Enable VCO phase synchronization mode  
            force_vco: Enable manual VCO parameter override to reduce spurs  
                
        Returns:  
            0 on success, -1 on failure  
        """  
        # Make sure we're working with integers  
        freq = int(freq)  
        denum = 0xFFFFFF  
        
        # Allowed VCO range: 3.2G to 6.4G  
        vco_freq = freq  
        div = 0  
        while vco_freq < 3200000000:  
            div += 1  
            vco_freq *= 2  
        
        if div > 8:  
            return -1  
        
        if sync_en and freq < 3200000000:  
            vco_freq //= 2  
        
        # Make sure all calculations result in integers  
        N = int(vco_freq // self.pfd_freq)  
        FRAC = int((vco_freq - N * self.pfd_freq) * denum // self.pfd_freq)  
        
        if sync_en and freq < 3200000000:  
            vco_freq *= 2  
        
        self.registers[34] = ((N >> 16) & 0x7) | 0x10  
        self.registers[36] = N & 0xFFFF  
        self.registers[38] = denum >> 16  
        self.registers[39] = denum & 0xFFFF  
        self.registers[42] = FRAC >> 16  
        self.registers[43] = FRAC & 0xFFFF  
        self.registers[45] = ((0x0800 if div == 0 else 0) | (self.registers[45] & 0xE7FF))  # OUT_A MUX  
        self.registers[46] = 0x07F1 if div == 0 else 0x07F0                               # OUT_B MUX  
        
        # Strange divider table of R75  
        divider_tbl = [0, 0, 1, 3, 5, 7, 9, 12, 14]  
        self.registers[75] = 0x0800 | (divider_tbl[div] << 6)  
        
        # Check if we need to recalibrate the VCO  
        if not hasattr(self, 'last_vco_sel_freq'):  
            self.last_vco_sel_freq = 0  
        
        VCO_CAL_THRESHOLD = 100000000  # 100 MHz threshold  
        freq_delta = abs(self.last_vco_sel_freq - freq)  
        
        # Convert to MHz for easier comparison  
        freq_mhz = freq / 1000000  
        vco_freq_mhz = vco_freq / 1000000  
        
        # Detect problematic frequency range (~5.81-5.99 GHz with 6.9 GHz leakage)  
        problematic_range = (5810 <= freq_mhz <= 5990)  
        
        if freq_delta > VCO_CAL_THRESHOLD or force_vco:  
            self.last_vco_sel_freq = freq  
            self.registers[78] &= ~0x200  
                
            # Partial Assist  
            mhz = int(vco_freq // 1000000)  
            assist_tbl = [  
                [3200, 3650, 131, 19, 138, 137],  
                [3650, 4200, 143, 25, 162, 142],  
                [4200, 4650, 135, 34, 126, 114],  
                [4650, 5200, 136, 25, 195, 172],  
                [5200, 5750, 133, 20, 190, 163],  
                [5750, 6400, 151, 27, 256, 204],  
            ]  
                
            select = -1  
            for i in range(6):  
                if mhz >= assist_tbl[i][0] and mhz <= assist_tbl[i][1]:  
                    select = i  
            
            if mhz > 6400:  
                select = 5  
            
            fmin = assist_tbl[select][0]  
            fmax = assist_tbl[select][1]  
            cmin = assist_tbl[select][2]  
            cmax = assist_tbl[select][3]  
            amin = assist_tbl[select][4]  
            amax = assist_tbl[select][5]  
                
            # Calculate C and A values for VCO selection - ensure integer result  
            C = int(0.5 + cmin - float(mhz - fmin) * (cmin - cmax) / (fmax - fmin))  
            A = int(0.5 + amin - float(mhz - fmin) * (amin - amax) / (fmax - fmin))  
            vco = select + 1  
                
            C += 10  
            
            # === VCO FORCE MODE HANDLING ===  
            if problematic_range or force_vco:  
                # Force values to use a different VCO band to avoid the 6.9 GHz leakage  
                # For the 5.81-5.99 GHz range, try using VCO from lower band  
                if 5750 <= vco_freq_mhz <= 6400:  
                    # Force to a different VCO configuration  
                    vco = 5  # Use band 5 instead of 6  
                    
                    # Adjust tuning parameters - these may need experimentation  
                    C += 5  
                    A -= 10  
                    
                # Set force bits in registers  
                self.registers[20] = self.registers.get(20, 0) | (1 << 4)  # VCO_SEL_FORCE = 1  
                self.registers[19] = self.registers.get(19, 0) | (1 << 5)  # VCO_CAPCTRL_FORCE = 1  
                self.registers[16] = self.registers.get(16, 0) | (1 << 4)  # VCO_DACISET_FORCE = 1  
            else:  
                # Normal operation - ensure force bits are cleared  
                self.registers[20] = self.registers.get(20, 0) & ~(1 << 4)  # VCO_SEL_FORCE = 0  
                self.registers[19] = self.registers.get(19, 0) & ~(1 << 5)  # VCO_CAPCTRL_FORCE = 0  
                self.registers[16] = self.registers.get(16, 0) & ~(1 << 4)  # VCO_DACISET_FORCE = 0  
            
            # Continue with register setup  
            self.registers[78] = 0x000 | (C << 1)  
            self.registers[20] = (self.registers[20] & (1 << 4)) | 0x4448 | (vco << 11)  # Preserve force bit  
            self.registers[17] = A  
            self.registers[8] = 0x6000  
            self.write_register(20, self.registers[20])  
            self.write_register(17, self.registers[17])  
            self.write_register(8, self.registers[8])  
                
            # Full calibration  
            self.registers[16] = (self.registers[16] & (1 << 4)) | A  # Preserve force bit  
            self.registers[19] = (self.registers[19] & (1 << 5)) | 0x2700 | C  # Preserve force bit  
            self.write_register(16, self.registers[16])  
            self.write_register(19, self.registers[19])  
        else:  
            self.registers[78] |= 0x200  
            
        # Set PFD delay based on VCO frequency  
        pfd_dly_needed = 2 if vco_freq > 4000000000 else 1  
            
        # Get current value with default of 0 if not set  
        curr_reg37 = self.registers.get(37, 0)  
        if ((curr_reg37 >> 8) & 0x3F) != pfd_dly_needed:  
            self.registers[37] = (pfd_dly_needed << 8) | 5  
            self.write_register(37, self.registers[37])  
            
        # Write registers in specific order  
        self.write_register(78, self.registers[78])  
        self.write_register(75, self.registers[75])  
        self.write_register(46, self.registers[46])  
        self.write_register(45, self.registers[45])  
        self.write_register(39, self.registers[39])  
        self.write_register(38, self.registers[38])  
        self.write_register(43, self.registers[43])  
        self.write_register(42, self.registers[42])  
        self.write_register(36, self.registers[36])  
        self.write_register(34, self.registers[34])  # Write N last  
            
        # Sync mode configuration  
        if sync_en:  
            self.registers[58] &= ~(1 << 15)  
            self.registers[0] |= 1 << 14  
            self.registers[69] = 0  
            self.registers[70] = 30000  
            self.write_register(58, self.registers[58])  
            self.write_register(69, self.registers[69])  
            self.write_register(70, self.registers[70])  
        else:  
            self.registers[58] |= 1 << 15  
            self.registers[0] &= ~(1 << 14)  
            self.write_register(0, self.registers[0])  # FCAL_EN = 1  
            
        self.write_register(58, self.registers[58])  
            
        return 0
    
    def trigger_calibration(self, timeout_ms=1000):  
        """  
        Trigger VCO calibration by setting the FCAL bit, wait for completion,  
        and read out calibration status  
        
        Args:  
            timeout_ms: Maximum time to wait for calibration (milliseconds)  
            
        Returns:  
            Dictionary with calibration status:  
            {  
                'success': Boolean indicating if calibration completed,  
                'lock_status': Boolean indicating if PLL is locked,  
                'vco_num': Selected VCO number (1-6),  
                'time_ms': Time taken for calibration in ms  
            }  
        """  

        
        # Store original readback state and make sure readback is enabled  
        r0_value = self.registers.get(0, 0x221C)  
        readback_was_enabled = (r0_value & 0x4) == 0  
        
        if not readback_was_enabled:  
            # Enable readback mode temporarily  
            self.write_register(0, r0_value & ~0x4)  
        
        # Set the FCAL bit (bit 6 of R0)  
        self.registers[0] |= (1 << 6)  
        self.write_register(0, self.registers[0])  
        
        # Get start time  
        start_time = time.ticks_ms()  
        elapsed = 0  
        cal_complete = False  
        
        # Poll until FCAL bit clears or timeout occurs  
        while elapsed < timeout_ms:  
            # Read register 0  
            reg0 = self.read_register(0)  
            
            # Check if FCAL bit (bit 6) has cleared  
            if (reg0 & (1 << 6)) == 0:  
                cal_complete = True  
                break  
            
            # Small delay to avoid hammering the SPI bus  
            time.sleep_ms(5)  
            elapsed = time.ticks_diff(time.ticks_ms(), start_time)  
        
        # Read lock status from R110  
        lock_status = self.is_locked()  
        
        # Read VCO status from R110 bits [14:12] - indicates selected VCO num  
        reg110 = self.read_register(110)  
        vco_num = (reg110 >> 12) & 0x7  
        
        # Restore original readback setting if needed  
        if not readback_was_enabled:  
            self.write_register(0, r0_value)  
        
        # Calculate time taken  
        time_ms = time.ticks_diff(time.ticks_ms(), start_time)  
        
        return {  
            'success': cal_complete,  
            'lock_status': lock_status,  
            'vco_num': vco_num,  
            'time_ms': time_ms  
        }  
    
    def set_pd_gain(self, gain_setting):  
        """  
        Set the charge pump current gain  
        
        Args:  
            gain_setting: Integer value (0-15)  
            
        Returns:  
            str: Confirmation message  
        """  
        if gain_setting < 0 or gain_setting > 15:  
            raise ValueError("Charge pump gain must be 0-15")  
            
        # Read current register value  
        reg_14 = self.read_register(14)  
        
        # Clear bits [6:3] using mask 0x78 (0b01111000)  
        # Then set new value (shifted to position)  
        new_reg_14 = (reg_14 & ~0x78) | ((gain_setting & 0xF) << 3)  
        
        # Write back to register  
        self.write_register(14, new_reg_14)  
        
        return f"Charge pump gain set to {gain_setting}"  


    def get_pd_gain(self):  
        """  
        Get the current charge pump gain setting  
        
        Returns:  
            int: Current gain setting (0-15)  
        """  
        # Read register 14  
        reg_14 = self.read_register(14)  
        
        # Extract bits [6:3]  
        # Mask with 0x78 (0b01111000) and shift right by 3  
        gain_setting = (reg_14 & 0x78) >> 3  
        
        return gain_setting    
    
    def set_osc_single_ended(self):  
        """  
        Configure the reference clock input for single-ended operation.  
        
        This function sets bit 2 of Register 5 to enable single-ended   
        input mode for the reference clock.  
        
        Returns:  
            str: Confirmation message  
        """  
        # Read current register value  
        reg_5 = self.read_register(5)  
        
        # Set bit 2 to enable single-ended mode (mask 0x04 = 0b00000100)  
        new_reg_5 = reg_5 | 0x04  
        
        # Write back to register  
        self.write_register(5, new_reg_5)  
        
        # Verify the configuration  
        if self.read_register(5) & 0x04:  
            return "Clock input configured for single-ended mode"  
        else:  
            return "Error: Failed to set single-ended mode"  
    