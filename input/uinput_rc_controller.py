# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:05:51 2016

@author: jussi
"""



SAMPLES_TO_DETECT_MOVEMENT = 100
STILLNESS_JITTER_MAX = 10
    
import uinput
import serial

def get_channel_vals(ser):
    # Update from RC controller 
    ser.write('p') # ask for reading
    ctr = ser.readline().split(",")
    if len(ctr)==2:
        throttle = int((-float(ctr[1])+1.0)/2.0*255)
        steer = int((-float(ctr[0])+1.0)/2.0*255)
        return throttle,steer
    else:
        return None,None

def main():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1.0)
    prev_throttle = None
    prev_steer = None
    jitter_threshold = 4

    # TODO: Get jitter from RC controller
    print "Turn and throttle to each extrimity few times..."
    dt, ds = [], []
    while True:
        if ds and dt and (max(ds)>STILLNESS_JITTER_MAX or max(dt)>STILLNESS_JITTER_MAX):
            break # the user is moving the throttle / wheel, robably
        throttle, steer = get_channel_vals(ser)
        if throttle!=None and steer!=None:
            if prev_throttle!=None and prev_steer !=None:
                dt.append(abs(prev_throttle-throttle))
                ds.append(abs(prev_steer-steer))
            prev_throttle = throttle
            prev_steer = steer
            
            
    print "...good, good ..."
    while len(ds)<SAMPLES_TO_DETECT_MOVEMENT:
        throttle, steer = get_channel_vals(ser)
        if throttle!=None and steer!=None:
            dt.append(abs(prev_throttle-throttle))
            ds.append(abs(prev_steer-steer))
            prev_throttle = throttle
            prev_steer = steer
        
    print "and when ready, return to neutral position and hooooold..."
    while max(dt)>STILLNESS_JITTER_MAX or max(ds)>STILLNESS_JITTER_MAX:
        throttle, steer = get_channel_vals(ser)
        if throttle!=None and steer!=None:
            dt.pop(0)
            ds.pop(0)
            dt.append(abs(prev_throttle-throttle))
            ds.append(abs(prev_steer-steer))
            prev_throttle = throttle
            prev_steer = steer
    print "calbirated!"
    print dt, ds
    print
        
    events = (
        uinput.BTN_0,
        uinput.ABS_X + (0, 255, 0, 0),
        uinput.ABS_Y + (0, 255, 0, 0),
        )

    device = uinput.Device(events)
    while(True):
        
        throttle, steer = get_channel_vals(ser)
        if throttle!=None and steer!=None:
            if prev_throttle==None or prev_steer==None \
               or abs(prev_throttle-throttle)>=jitter_threshold \
               or abs(prev_steer-steer)>=jitter_threshold:
                
                # TODO emit only when changed
                device.emit(uinput.ABS_X, steer, syn=False)
                device.emit(uinput.ABS_Y, throttle)
                
            prev_throttle = throttle
            prev_steer = steer
            
            # TODO implement joystick button event when at extemes
            #device.emit_click(uinput.BTN_JOYSTICK)

if __name__ == "__main__":
    main()