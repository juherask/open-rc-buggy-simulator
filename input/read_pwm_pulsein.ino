/*
## DISCLAIMER ##
The author is in no way responsible for any problems or damage caused by
using this code and instructions. By using this code and instructions 
you acknowledge these terms. Use at your own risk.

## DESCRIPTION ##

Script that allows reading PWM channel output out of a RC receiver (RX).
When the RC transmitter is operated the RC channel readings can be read
using the serial-over-USB.

## USAGE ##

1) Upload the code to the Arduino using Arduino IDE and a USB-cable

2) Do the wiring. What you need is 4 female-male jumper wires connected
as follows:
	Arduino 5V -> RX BAT or CH1 VCC.
		Usually the middle pin in the RX
	Arduino GND -> RX BAT or CH1 GND.
		Usually the outer pin = furthest away fron the connector notch.
	Arduino Digital 2 -> RX CH1 Signal.
		Usually the inner pin = closest to the connector notch.
	Arduino Digital 2 -> RX CH3 Signal.
		Usually the inner pin = closest to the connector notch.
Doublecheck everything from secondary sources, especially anything
concerning the wiring diagram as the pinouts may vary from model to model.

3) Turn on the TX, reset the Arduino and open Arduino serial terminal with 
115200 baud rate. By sending a letter 'p' (input it in the seiral terminal 
field and press [Send]) you should recieve some data.

4) Note that the code running on the Arduino autocalibrates. This means
that to get correct readings you should use issue the 'p' command when
the steering/throttle/other in the TX is in it's extremities.

TODO:
- add command 'n' to set the neutral state (it is not always half way of the range)
- add command 'c' to toggle autocalibraiton off/on (default is on)
- add command 's' to save calibraton data in pwm_channel structs to the EEPROM,
this data should be loaded automatically when Arduino is reset if it exists. 
Also, the autocalibration should be turned off if the data load is successfull.
The 'c' command needs then to be modified to reset the calibraion data on calibraiton
enable.
*/

byte PWM_PIN_CH1 = 2;
byte PWM_PIN_CH2 = 3;

struct pwm_channel {
  int min_val;
  float cur_val; // range -1.0 to 1.0
  int max_val;
};

pwm_channel pwm_ch1 = {32767, 0, 0};
pwm_channel pwm_ch2 = {32767, 0, 0};
 
void setup() {
  pinMode(PWM_PIN_CH1, INPUT);
  pinMode(PWM_PIN_CH2, INPUT);
  Serial.begin(115200);
}

// Autocalibrating normalization
void normalize(pwm_channel& channel, int new_val){
  if (new_val>channel.max_val){
    channel.max_val = new_val;
  }
  if (new_val<channel.min_val){
    channel.min_val = new_val;
  }
  int range = float(max(1, channel.max_val-channel.min_val))
  channel.cur_val = 2.0*(new_val-channel.min_val)/range-1.0;
}
 
void loop() {
  int ch1_new_val = pulseIn(PWM_PIN_CH1, HIGH);
  int ch2_new_val = pulseIn(PWM_PIN_CH2, HIGH);

  char cmd=Serial.read();
  if (cmd=='p')
  {
    normalize(pwm_ch1, ch1_new_val); 
    normalize(pwm_ch2, ch2_new_val);
    
    Serial.print(pwm_ch1.cur_val);
    Serial.print(",");
    Serial.print(pwm_ch2.cur_val);
    Serial.print("\n");
    // delay(100);
  }
}
