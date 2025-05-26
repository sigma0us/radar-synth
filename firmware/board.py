"""
RevG Board Pin Definitions and Power Control Functions

This file defines all GPIO pins used in the VetGuardian RevG radar system
and provides power control functions for different subsystems.
"""

from machine import Pin, SPI, I2C, Timer,ADC,SoftSPI
import time


# ===============================
# ESP32 Native GPIO Pin Definitions
# ===============================

# LED Pins
LED_HEARTBEAT = Pin(1, Pin.OUT)  # health_proc_en (CPU Status LED)


# LMX2572
LMX2572_CE= Pin(3, Pin.OUT)  # lmx2572_ce (Chip Enable)
LMX2572_CSB= Pin(5, Pin.OUT)  # lmx2572_vco (VCO Control)
LMX2572_SCK= Pin(10, Pin.OUT)  # lmx2572_sck (SPI Clock)
LMX2572_SDO= Pin(42, Pin.IN)  # lmx2572_sdo (SPI Data Out)
LMX2572_SDI= Pin(6, Pin.OUT)  # lmx2572_sdi (SPI Data In)
LMX2572_SYNC= Pin(39, Pin.OUT)  # lmx2572_sync (Sync Signal)
LMX2572_RAMPCLK= Pin(4, Pin.OUT)  # lmx2572_rampclk (Ramp Clock)
LMX2572_RAMPDIR = Pin(40, Pin.OUT)  # lmx2572_rampdir (Ramp Direction)
LMX2572_SYSREFFREQ = Pin(41, Pin.OUT)  # lmx2572_sysrefreq (System Reference Frequency)



# UART Pins
UART0_TX = Pin(7, Pin.OUT)  # uart1_tx (UART Transmit)
UART0_RX = Pin(8, Pin.IN)  # uart1_rx (UART Receive)

# I2C Pins
I2C_SCL = Pin(11)  
I2C_SDA = Pin(12)  
I2C_FREQ = 400000  # I2C frequency (400kHz)

#OSC
REF_CLK_EN = Pin(7, Pin.OUT)  # ref_clk_en (Reference Clock Enable)
REF_CLK_SEL = Pin(8, Pin.OUT)  # ref_clk_sel (Reference Clock Select)




# Initialize LMX2572 Pins
LMX2572_CE.value(0)  # Set Chip Enable to low
LMX2572_CSB.value(1)  # Set VCO Control to low
LMX2572_SCK.value(1)  # Set SPI Clock to low
LMX2572_SDI.value(0)  # Set SPI Data In to low
LMX2572_SYNC.value(0)  # Set Sync Signal to low
LMX2572_RAMPCLK.value(0)  # Set Ramp Clock to low   
LMX2572_RAMPDIR.value(0)  # Set Ramp Direction to low
LMX2572_SYSREFFREQ.value(0)  # Set System Reference Frequency to low

# Initialize REFERENCE CLK
REF_CLK_EN.value(0)  # Set Reference Clock Enable to low
REF_CLK_SEL.value(1)  # Set Reference Clock Select to low    (Internal Reference Clock)


def create_default_i2c():
    """Create and return the default I2C interface for power and sensor control"""
    return I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=I2C_FREQ)


def create_lmx2572_spi():
    """Create and return SPI interface for FPGA communications using UC2FPGA pins"""
    return SPI(1, baudrate=20000000, polarity=1, phase=1, 
               sck=LMX2572_SCK, mosi=LMX2572_SDI, miso=LMX2572_SDO)






