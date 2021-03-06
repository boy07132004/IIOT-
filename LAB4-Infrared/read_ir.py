#!/usr/bin/env python3
"""
argv[1] : [input]
argv[2] : [led pin]
argv[3] : [signal key map]
"""
import RPi.GPIO as GPIO
import time
import sys
import json

#-----------------------DEF------------------------#
def initEnv(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.IN)

def initPin(lp):
    GPIO.setup(lp, GPIO.OUT)
    pwm = GPIO.PWM(lp, 1000)
    pwm.start(0)
    return pwm

def getSignal(pin):
    start, stop = 0, 0
    signals = []

    while True:
        while GPIO.input(pin) == 0:
            None
    
        start = time.time()
    
        while GPIO.input(pin) == 1:
            stop = time.time()
            duringUp = stop - start
            if duringUp > 0.1 and len(signals) > 0:
                return signals[1:]
    
        signals.append(duringUp)

def compairSignal(s1, s2, rang):
    min_len = min(len(s1), len(s2))

    for i in range(min_len):
        if abs(s1[i] - s2[i]) > rang:
            return False
    
    return True

def decodeSignal(s, signal_map, rang):
    for name in signal_map.keys():
        if compairSignal(s, signal_map[name], rang):
            return name

    return None
#-----------------------MAIN------------------------#
def main():
    # read argv
    p1  = sys.argv[1]
    l1  = sys.argv[2]
    m1  = sys.argv[3]
    PIN = int(p1[1:len(p1)-1])
    led = int(l1[1:len(l1)-1])
    smap= m1[1:len(m1)-1]
    
    # open map
    src = open(smap, 'r')
    signal_map = json.loads(src.read())
    src.close()
    
    
    # init PIN
    initEnv(PIN)
    pwms=initPin(led)
    
    # function 
    print("1    :LED on\n0    :LED off\nPower:poweroff\n\
+    :Plus Duty\n-    :Minus Duty")

    # start .........
    while True:  
        s = getSignal(PIN)
        sig=decodeSignal(s,signal_map,0.001)
        
        if sig == str('on'):
            print('----LED on----\n')
            duties=50
            pwms.ChangeDutyCycle(duties)
            shining=True
            while shining:
                ss = getSignal(PIN)
                sigg=decodeSignal(ss,signal_map,0.001)
                
                if sigg == str('plus'):
                    if duties==100:
                        print('duty limit :100')
                        continue
                    duties+=10
                    print('duty++  now duty:',duties)
                    pwms.ChangeDutyCycle(duties)
                
                elif sigg == str('minus'):
                    if duties==0:
                        print('duty limit :0')
                        continue
                    duties-=10
                    print('duty--  now duty:',duties)
                    pwms.ChangeDutyCycle(duties)
                
                elif sigg == str('off'):
                    print('----LED off----\n')
                    duties=0
                    pwms.ChangeDutyCycle(duties)
                    shining=False
                elif sigg == str('power'):
                    print('Turn off the led first')

        elif sig == str('plus'):print('Turn on the led first')
        elif sig == str('minus'):print('Turn on the led first')
        elif sig == str('off'):print('Led is off now')
        elif sig == str('power'):
            print('----Good Bye----\n')
            break
        
        else:print('not record\n')
    
    # end
    pwms.stop()
    GPIO.cleanup()
    
if __name__ == "__main__":
    main()
