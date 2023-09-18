from hcsr04 import HCSR04
from imu import MPU6050
from time import sleep
import machine
import time
import math
import _thread

# Define GPIO pins for Motor A
motor_a_enable = machine.Pin(13, machine.Pin.OUT)  # Enable pin for Motor A
motor_a_1 = machine.Pin(12, machine.Pin.OUT)       # Control pin 1 for Motor A
motor_a_2 = machine.Pin(14, machine.Pin.OUT)       # Control pin 2 for Motor A

# Define GPIO pins for Motor B
motor_b_enable = machine.Pin(27, machine.Pin.OUT)  # Enable pin for Motor B
motor_b_1 = machine.Pin(26, machine.Pin.OUT)       # Control pin 1 for Motor B
motor_b_2 = machine.Pin(25, machine.Pin.OUT)       # Control pin 2 for Motor B

# Create PWM objects for motor speed control
motor_a_pwm = machine.PWM(motor_a_enable, freq=1000, duty=512)  # Motor A PWM
motor_b_pwm = machine.PWM(motor_b_enable, freq=1000, duty=512)  # Motor B PWM

# Define GPIO pins for Motor encoders
encoder_a_pin = machine.Pin(35, machine.Pin.IN)
encoder_b_pin = machine.Pin(34, machine.Pin.IN)

# Create variables to keep track of encoder counts
encoder_a_count = 0
encoder_b_count = 0

# Define encoder callback functions
def encoder_a_callback(pin):
    global encoder_a_count
    if encoder_b_pin.value():
        encoder_a_count -= 1
    else:
        encoder_a_count += 1

def encoder_b_callback(pin):
    global encoder_b_count
    if encoder_a_pin.value():
        encoder_b_count -= 1
    else:
        encoder_b_count += 1

# Attach interrupts to encoder pins
encoder_a_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=encoder_a_callback)
encoder_b_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=encoder_b_callback)

# ESP32
sensor_middle = HCSR04(trigger_pin=17, echo_pin=5, echo_timeout_us=10000)
sensor_left = HCSR04(trigger_pin=15, echo_pin=2, echo_timeout_us=10000)
sensor_right = HCSR04(trigger_pin=4, echo_pin=16, echo_timeout_us=10000)

# Initialize I2C
#i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)

# Create an instance of the MPU6050 sensor
#mpu = MPU6050(i2c)

# Initialize variables
z_rotation = 0.0
last_time = 0.0

# Define a function to continuously update the angle in a separate thread
#def update_angle_thread():
#    global z_rotation, last_time
 #   while True:
  #      # Read accelerometer and gyroscope data
   #     accel_data = mpu.accel.xyz
    #    gyro_data = mpu.gyro.xyz

        # Extract gyro rate components
     #   gyro_z = gyro_data[2]

        # Calculate time delta (dt) since the last reading
      #  current_time = time.ticks_ms() / 1000
       # dt = current_time - last_time
        #last_time = current_time

        # Calculate yaw angle using gyroscope data (in degrees)
        #z_rotation += gyro_z * dt  # Yaw rate integrated over time

        # Ensure z_rotation stays within [-180, 180] degrees
        #z_rotation = (z_rotation + 180) % 360 - 180
        #print(z_rotation)

     #   time.sleep(0.1)  # Adjust the sleep duration as needed

# Start the update_angle_thread function in a separate thread
#_thread.start_new_thread(update_angle_thread, ())

# Function to set motor A direction and speed
def set_motor_right(direction, speed):
    motor_a_1.value(direction)
    motor_a_2.value(not direction)
    motor_a_pwm.duty(speed)

# Function to set motor B direction and speed
def set_motor_left(direction, speed):
    motor_b_1.value(direction)
    motor_b_2.value(not direction)
    motor_b_pwm.duty(speed)

# Function to control the motors using encoder counts
def control_motors(target_counts, speed):
    global encoder_a_count, encoder_b_count

    # Reset encoder counts
    encoder_a_count = 0
    encoder_b_count = 0

    # Set motor directions
    set_motor_right(1, speed)
    set_motor_left(1, speed)

    while True:
        if abs(encoder_a_count) >= target_counts or abs(encoder_b_count) >= target_counts:
            break

    # Stop motors
    set_motor_right(0, 0)
    set_motor_left(0, 0)

# Function to make the robot move forward
def forward():
#     control_motors(1000, 1023)  # Adjust target_counts and speed as needed
    set_motor_right(1, 1023)  # Motor A forward at half speed
    set_motor_left(1, 1023)  # Motor B forward at full speed

# Function to make the robot turn right
def right():
    set_motor_right(0, 500)  # Motor A forward at half speed
    set_motor_left(1, 1023)  # Motor B forward at full speed

# Function to make the robot turn left
def left():
    set_motor_right(1, 1023)  # Motor A forward at full speed
    set_motor_left(0, 500)  # Motor B forward at half speed

# Function to stop the robot
def stop():
    set_motor_right(0, 0)
    set_motor_left(0, 0)

def reverse():
    set_motor_right(0, 1023)  # Motor A forward at half speed
    set_motor_left(0, 1023)  # Motor B forward at full speed
# ESP8266
# sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

def main():
    global encoder_a_count, encoder_b_count  # Add this line to access the global encoder count variables
   

def check_minimum(reading):
    fall_back = 5
    if reading < fall_back:
        reverse()
    return

def find_largest_sensor(left, middle, right):
    sensor_dict = {
        "left": left,
        "middle": middle,
        "right": right
    }
    
    # Find the name of the variable with the largest value
    largest_sensor = max(sensor_dict, key=sensor_dict.get)
    
    return largest_sensor, sensor_dict(largest_sensor)

def where_to_go(sensor_left, sensor_middle, sensor_right):
    largest, value = find_largest_sensor(sensor_left, sensor_middle, sensor_right)
    if largest == "left":
        check_minimum(sensor_left)
        return left()
    elif largest == "right":
        check_minimum(sensor_right)
        return right()
    elif largest == "middle":
        check_minimum(sensor_middle)
        return forward()
        
   
  

while True:
    distance_middle = sensor_middle.distance_cm()
    distance_left = sensor_left.distance_cm()
    distance_right = sensor_right.distance_cm()
    
    if distance_middle >5:
        forward()
    else:
        if distance_left > 5:
            left()
            time.sleep(0.3)
        elif distance_right >5:
            right()
            time.sleep(0.3)
        else:
            reverse()
    
            