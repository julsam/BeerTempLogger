#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import serial
from datetime import datetime
import time
import threading

# change this stuff:
PORT = '/dev/cu.usbmodem1421'
BAUD = 9600
# interval in seconds to log
TIMER = 600

class ProgressPrint(object):
    def __init__(self):
        self.text = ''
        self.max_size = 0

        # write an empty line because reprint() goes up 1 line and clears it
        sys.stdout.write('\n')
        sys.stdout.flush()

    def reprint(self, text, timeout=0.5):
        # goes one line up and to the first character
        sys.stdout.write('\033[1A\r')
        # Clear previous output
        sys.stdout.write(' ' * self.max_size)
        sys.stdout.flush()

        # Print new text
        sys.stdout.write('\r%s\n' % text)
        sys.stdout.flush()

        if len(text) > self.max_size:
            self.max_size = len(text)
        self.text = text

        time.sleep(timeout)

class ArduinoTempLogger(object):
    """seconds is used to define the interval between temperature checks. By default it's 10 minutes (600 seconds)"""
    def __init__(self, seconds=600):
        self.port = PORT
        self.baud = BAUD
        self.connection = None
        self.progress = None
        self.timer = seconds

    def connect(self):
        self.progress = ProgressPrint()
        attempts = 0
        while True:
            try:
                self.connection = serial.Serial(self.port, self.baud, timeout=1)
                self.connection.write(str(chr(42)))
                self.progress.reprint('Connected to Arduino!')
                print self.connection
                break
            except:
                dots_anim = '...'
                if attempts % 3 == 0:
                    dots_anim = '.'
                elif attempts % 3 == 1:
                    dots_anim = '..'
                self.progress.reprint('Waiting for Arduino connection on \'%s\'%s' % (self.port, dots_anim))
                attempts += 1
                continue

    def get_data(self):
        # while True:
        #     setTemp1 = str(42)
        #     self.connection.write(setTemp1)
        #     time.sleep(1)
        #
        #     # Serial read section
        #     msg = self.connection.readline()
        #     print "Message from arduino: '%s'" % msg

        time.sleep(1)
        self.connection.write(str(self.timer))
        time.sleep(1)
        print self.connection.readline().rstrip()

        filename = 'temp-' + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'
        while True:
            temp_read = self.connection.readline().rstrip()
            if temp_read != '':
                read_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                temp_line = read_time + ': ' + temp_read + '\n'

                with open(filename, "a") as myfile:
                    myfile.write(temp_line)

                print temp_line.rstrip()
                time.sleep(self.timer)

if __name__ == '__main__':
    print 'Arduino Temperature Logger. Press <Ctrl> + <C> to quit.'
    arduino = ArduinoTempLogger(TIMER)
    try:
        arduino.connect()
        arduino.get_data()
    except KeyboardInterrupt:
        print '' # line return after "ˆC"
        # close serial connection
        if arduino.connection != None and arduino.connection.is_open:
            arduino.connection.close()
        raise
    except:
        # close serial connection
        if arduino.connection != None and arduino.connection.is_open:
            arduino.connection.close()
        raise
