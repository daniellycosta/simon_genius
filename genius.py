# -*- coding: utf-8 -*-

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import random

#GPIO's
b0 = "P8_7"
b1 = "P8_8"
b2 = "P8_9"

da = "P8_15"
db = "P8_14"
dc = "P8_13"
dd = "P8_18"
de = "P8_19"
df = "P8_17"
dg = "P8_16"

l0 = "P9_23"
l1 = "P9_24"
l2 = "P9_30"

off = "P9_26"
on = "P9_27"

#LED VECTOR
LEDS = [l0,l1,l2]
display = [da,db,dc,dd,de,df,dg]

game_sequence = []
player_sequence = []

GPIO.setup(b0, GPIO.IN)
GPIO.setup(b1, GPIO.IN)
GPIO.setup(b2, GPIO.IN)

GPIO.setup(da, GPIO.OUT)
GPIO.setup(db, GPIO.OUT)
GPIO.setup(dc, GPIO.OUT)
GPIO.setup(dd, GPIO.OUT)
GPIO.setup(de, GPIO.OUT)
GPIO.setup(df, GPIO.OUT)
GPIO.setup(dg, GPIO.OUT)

GPIO.setup(l0, GPIO.OUT)
GPIO.setup(l1, GPIO.OUT)
GPIO.setup(l2, GPIO.OUT)

GPIO.setup(off, GPIO.OUT)
GPIO.setup(on, GPIO.OUT)

GPIO.add_event_detect(b0, GPIO.FALLING)
GPIO.add_event_detect(b1, GPIO.FALLING)
GPIO.add_event_detect(b2, GPIO.FALLING)

current_round = 1
game_started = False
player_points = 0


def seven_seg_digits(number):
    if number == 0:
        return [0,0,0,0,0,0,1]
    elif number == 1:
        return [1,0,0,1,1,1,1]
    elif number == 2:
        return [0,0,1,0,0,1,0]
    elif number == 3:
        return [ 0,0,0,0,1,1,0]
    elif number == 4:
        return [1,0,0,1,1,0,0]
    elif number == 5:
        return [0,1,0,0,1,0,0]
    elif number == 6:
        return [0,1,0,0,0,0,0]
    elif number == 7:
        return [0,0,0,1,1,1,1]
    elif number == 8:
        return [0,0,0,0,0,0,0]
    else:
        return [0,0,0,1,1,0,0]


def show_points(number):
    print(number)
    array_Leds = seven_seg_digits(number)
    for i in range(len(array_Leds)):
        if(array_Leds[i] == 1):
            GPIO.output(display[i], GPIO.LOW)
        else:
            GPIO.output(display[i], GPIO.HIGH)



def blink(led,tempo):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(tempo)
    GPIO.output(led, GPIO.LOW)
    time.sleep(tempo)

def flag():
    blink(on,0.5)
    blink(off,0.5)
    blink(on,0.5)
    blink(off,0.5)

def generate_round():
    #Start with 1 led e add more one every round
    current_led = random.randint(0,2)
    game_sequence.append(current_led)
    for count in range(0,current_round):
        blink(LEDS[game_sequence[count]],0.5)
        #add leds in the sequence    

def get_play():
    if(current_round > 1):
        del player_sequence[:]
    number_of_plays = 0
    play_time_begin = time.time() #Return the number of seconds since epoch
    play_time_end = time.time()

    while((play_time_end - play_time_begin) < current_round + 3):

        if(GPIO.input(b0)):
            player_sequence.append(0)
            number_of_plays += 1
            print("B0")
            time.sleep(0.25)

        if(GPIO.input(b1)):
            player_sequence.append(1)
            number_of_plays += 1
            print("B1")
            time.sleep(0.25)

        if(GPIO.input(b2)):
            player_sequence.append(2)
            number_of_plays += 1
            print("B2")
            time.sleep(0.25)

        play_time_end = time.time()
        if(number_of_plays == current_round):
            break
    if(number_of_plays < current_round):
        while True:
            blink(off,0.1)
        
def validate_current_round():
    for i in range(0,current_round):
        if(player_sequence[i] != game_sequence[i]):
            return(False)
    return(True)

while True:
    GPIO.output(off, GPIO.HIGH)
    while(GPIO.input(b0) or GPIO.input(b1) or GPIO.input(b2)):
        game_started = True
        show_points(player_points)
        GPIO.output(on, GPIO.HIGH)
        GPIO.output(off, GPIO.LOW)
        flag()
        while game_started:
            generate_round()    
            
            #Detect player's play
            get_play()

            #DEBUG
            print(game_sequence)
            print(player_sequence)

            if(not(validate_current_round())):
                while True:
                    blink(off,0.1)

            player_points +=1
            flag()
            show_points(player_points)
            current_round += 1