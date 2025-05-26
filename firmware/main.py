from machine import Pin, SPI, I2C, Timer
import time
import board as pins
# Import pin definitions and power control functions
from lmx2572 import LMX2572
from si570 import Si570

# For heartbeat LED
def heartbeat_callback(timer):
    pins.LED_HEARTBEAT.value(not pins.LED_HEARTBEAT.value())

if __name__ == '__main__':
    # Create and start a timer for the heartbeat LED
    # Timer frequency: 2Hz (on for 0.25s, off for 0.25s)
    heartbeat_timer = Timer(0)  # Use timer 0
    heartbeat_timer.init(period=250, mode=Timer.PERIODIC, callback=heartbeat_callback)

    i2c = pins.create_default_i2c()
    spi = pins.create_lmx2572_spi()

      # Select external clock
    pins.REF_CLK_SEL.value(1)  # Set to internal reference clock
    pins.REF_CLK_EN.value(0)  # Enable the reference clock
    #si570 = Si570(i2c,0x55)  # Initialize with desired frequency of 100 MHz and specific I2C address
    
    pll = LMX2572(spi=spi,cs=pins.LMX2572_CSB,en=pins.LMX2572_CE,ref_freq=100.0e6)
    pll.enable()
    pll.setup()
    pll.set_freq(5.8e9)


    

