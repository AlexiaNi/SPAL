from machine import Pin, ADC, PWM
import utime
import time
from time import sleep

# Declararea variabilelor globale 
step = Pin(17)
direction = Pin(16, Pin.OUT)
change_dir_button = Pin(14, Pin.IN)    
push_button = Pin(15, Pin.IN)  
servo_1 = PWM(Pin(2))
servo_2 = PWM(Pin(5))
potentiometer_1 = ADC(29)
potentiometer_2 = ADC(26)

# Setare frecventa servomotoare
servo_1.freq(50)
servo_2.freq(50)
# Valori maxime si minime pentru PWN
in_min = 0
in_max = 65535
# Valori minime si maxime pentru gradele de rotatie
out_min = 1000
out_max = 9000

# Miscare motor stepper 
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def move():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [10]
    nop()          [10]
    set(pins, 0)   [31]
    nop()          [10]
    nop()          [10]
    wrap()

motor = rp2.StateMachine(0, move, freq=5000, set_base=step)
motor.active(1)


# Iteratie nesfarsita (atata timp cat microcontrolerul se alimenteaza)
while True:
  logic_state_change = change_dir_button.value()
  logic_state = push_button.value()
  if logic_state == True:
      motor.active(1)
      direction.value(1) 
  else:                       
      motor.active(0)


  value_1 = potentiometer_1.read_u16()
  value_2 = potentiometer_2.read_u16()
    # PWM - grade 
  Servo_1 = (value_1 - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  Servo_2 = (value_2 - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    # Miscare servomotor
  servo_1.duty_u16(int(Servo_1))
