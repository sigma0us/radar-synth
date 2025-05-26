from machine import I2C

class Si570:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        self.FXTAL = 114.285e6  # Fixed XTAL frequency in Hz (114.285 MHz)

        # Initialize variables
        self.REG = [0] * 6
        self.INITIAL_HSDIV = None
        self.INITIAL_N1 = None
        self.DCO = None
        self.FOUT = None

    def read_startup_configuration(self):
        # Write to register 135 to recall NVM bits into RAM
        self.i2c.writeto_mem(self.address, 135, bytearray([0x01]))

        # Read registers 7 to 12 and store them in REG
        self.REG = [self.i2c.readfrom_mem(self.address, i + 7, 1)[0] for i in range(6)]

        # Print register values to debug
        print(f"Register Values (Hex): {[hex(reg) for reg in self.REG]}")

        # Extract INITIAL_HSDIV from REG[0]
        self.INITIAL_HSDIV = ((self.REG[0] & 0xE0) >> 5) + 4
        print(f"Extracted INITIAL_HSDIV: {self.INITIAL_HSDIV}")

        # Extract INITIAL_N1 from REG[0] and REG[1]
        self.INITIAL_N1 = ((self.REG[0] & 0x1F) << 2) + ((self.REG[1] & 0xC0) >> 6)
        print(f"Raw INITIAL_N1 Value: {self.INITIAL_N1}")

        # Handle special cases for N1
        if self.INITIAL_N1 == 0:  # If N1 is 0, set it to 1
            self.INITIAL_N1 = 1
        elif (self.INITIAL_N1 % 2) != 0:  # Ensure N1 is always even
            self.INITIAL_N1 += 1
        
        print(f"FINAL INITIAL_N1: {self.INITIAL_N1}")

    def calculate_frequencies(self):
        if self.REG is None:
            print("REG is not initialized. Please call read_startup_configuration first.")
            return

        # Initialize FRAC_BITS with double precision
        FRAC_BITS = 0.0

        # Calculate the fractional portion as described
        FRAC_BITS += ((self.REG[2] & 0xF) * (2 ** 24))  # Extract bits 0-3 (4 bits)
        FRAC_BITS += (self.REG[3] * (2 ** 16))          # Extract bits 4-11 (8 bits)
        FRAC_BITS += (self.REG[4] * 256)                 # Extract bits 12-19 (8 bits)
        FRAC_BITS += self.REG[5]                         # Extract bits 20-27 (8 bits)

        # Debug output for FRAC_BITS
        print(f"FRAC_BITS: {FRAC_BITS}")

        # RFREQ is initially the fractional part divided by 2^28 for scaling
        RFREQ_FRAC = FRAC_BITS / (2 ** 28)

        # Read the initial value for RFREQ. A 34-bit number is fit into a 32-bit space
        # by ignoring lower 2 bits.
        INITIAL_RFREQ_LONG = (self.REG[1] & 0x3F)         # Use only valid bits from Register 8
        INITIAL_RFREQ_LONG = (INITIAL_RFREQ_LONG << 8) + self.REG[2]  # Register 9
        INITIAL_RFREQ_LONG = (INITIAL_RFREQ_LONG << 8) + self.REG[3]  # Register 10
        INITIAL_RFREQ_LONG = (INITIAL_RFREQ_LONG << 8) + self.REG[4]  # Register 11
        INITIAL_RFREQ_LONG = (INITIAL_RFREQ_LONG << 6) + (self.REG[5] >> 2)  # Shifted Register 12

        # Add the integer portion to RFREQ
        RFREQ_INT = ((self.REG[1] & 0x3F) << 4) + ((self.REG[2] & 0xF0) >> 4)

        print(f"RFREQ_INT: {RFREQ_INT}: RFREQ_FRAC: {RFREQ_FRAC}")  # Debug output for RFREQ_INT

        RFREQ = RFREQ_INT + RFREQ_FRAC  # Combine integer and fractional parts
        # Final RFREQ output in hexadecimal
        print(f"RFREQ: {RFREQ}")  # Print RFREQ

        # The DCO frequency calculation (DCO in proper units)
        self.DCO = RFREQ * self.FXTAL

        # Ensure DCO is within acceptable range
        if not (4.85e9 <= self.DCO <= 5.67e9):
            print(f"Warning: DCO frequency {self.DCO / 1e9:.6f} GHz is out of acceptable range!")

        print(f"Calculated DCO: {self.DCO / 1e9:.6f} GHz")  # DCO in GHz
        self.FOUT = self.DCO / (self.INITIAL_N1 * self.INITIAL_HSDIV)
        print(f"Calculated FOUT: {self.FOUT / 1e6:.6f} MHz")  # FOUT in MHz

    def dump_register(self):
        # Ensure REG is not None
        if self.REG is None:
            print("REG is not initialized. Please call read_startup_configuration first.")
            return
        
        # Ensure frequencies are calculated
        if self.DCO is None or self.FOUT is None:
            print("Please call calculate_frequencies() before dumping register values.")
            return

        # Print the register values in hexadecimal
        print("Register Values (Hex):")
        for i, reg_value in enumerate(self.REG):
            print(f"Register {i + 7}: {reg_value:#0X}")

        # Print calculated key parameters
        print("\nKey Parameters:")
        print(f"XTAL Frequency: {self.FXTAL / 1e6:.6f} MHz")  # XTAL frequency in MHz
        print(f"INITIAL_HSDIV: {self.INITIAL_HSDIV}")
        print(f"INITIAL_N1: {self.INITIAL_N1}")
        print(f"DCO Frequency: {self.DCO / 1e9:.6f} GHz")      # DCO in GHz
        print(f"FOUT Frequency: {self.FOUT / 1e6:.6f} MHz")    # FOUT in MHz

    def set_freq(self, desired_freq):
        """Set the output frequency (FOUT) to the desired value."""
        # Calculate the new DCO frequency
        # Ensure INITIAL_N1 and INITIAL_HSDIV are obtained beforehand.
        if self.INITIAL_N1 is None or self.INITIAL_HSDIV is None:
            print("INITIAL_N1 or INITIAL_HSDIV not set. Please call read_startup_configuration first.")
            return

        fdco = desired_freq * self.INITIAL_N1 * self.INITIAL_HSDIV
        print(f"Calculated new DCO frequency: {fdco / 1e9:.6f} GHz")

        # Calculate RFREQ based on the new DCO
        rf_freq = fdco / self.FXTAL
        rf_freq_scaled = rf_freq * (2 ** 28)
        
        # Prepare register settings
        reg0 = (self.INITIAL_HSDIV - 4) << 5 | (self.INITIAL_N1 >> 2)
        reg1 = (self.INITIAL_N1 & 0x03) << 6 | ((int(rf_freq_scaled) >> 28) & 0x3F)  # 0x3F = 63
        reg2 = (int(rf_freq_scaled) >> 24) & 0x0F
        reg3 = (int(rf_freq_scaled) >> 16) & 0xFF
        reg4 = (int(rf_freq_scaled) >> 8) & 0xFF
        reg5 = int(rf_freq_scaled) & 0xFF

        # Freeze DCO and set the new frequency configuration
        self.i2c.writeto_mem(self.address, 137, bytearray([0x10]))  # Freeze DCO (bit 4)
        self.i2c.writeto_mem(self.address, 7, bytearray([reg0]))  # Write new REG[0]
        self.i2c.writeto_mem(self.address, 8, bytearray([reg1]))  # Write new REG[1]
        self.i2c.writeto_mem(self.address, 9, bytearray([reg2]))  # Write new REG[2]
        self.i2c.writeto_mem(self.address, 10, bytearray([reg3]))  # Write new REG[3]
        self.i2c.writeto_mem(self.address, 11, bytearray([reg4]))  # Write new REG[4]
        self.i2c.writeto_mem(self.address, 12, bytearray([reg5]))  # Write new REG[5]

        # Unfreeze DCO
        self.i2c.writeto_mem(self.address, 137, bytearray([0x00]))  # Unfreeze DCO (bit 4 = 0)
        print(f"Frequency set to: {desired_freq} MHz")

# Example usage
# from machine import Pin
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Initialize your I2C pins
# si570 = Si570(i2c, address=0x55)         # Initialize Si570 with the correct I2C address
# si570.read_startup_configuration()        # Read the startup configuration
# si570.calculate_frequencies()              # Calculate the frequencies
# si570.dump_register()                      # Output register values
# si570.set_freq(161.132812)                # Set a new output frequency