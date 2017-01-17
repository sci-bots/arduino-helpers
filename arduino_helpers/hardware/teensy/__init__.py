# -*- coding: utf-8 -*-
import pandas as pd

HIGH = 1
LOW = 0
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2
LSBFIRST = 0
MSBFIRST = 1
_BV = lambda n: (1 << (n))
CHANGE = 4
FALLING = 2
RISING = 3

LED_BUILTIN = 13

ADC_0 = 0
ADC_1 = 1
ADC_VERY_LOW_SPEED = 0
ADC_LOW_SPEED = 1
ADC_MED_SPEED = 2
ADC_HIGH_SPEED_16BITS = 3
ADC_HIGH_SPEED = 4
ADC_VERY_HIGH_SPEED = 5

CAN_RX = 4
CAN_TX = 3

RX1 = 0
TX1 = 1
RX2 = 9
TX2 = 10
RX3 = 7
TX3 = 8

CS = 10
SCK = 13
DOUT = 11
DIN = 12
MOSI = 11
MISO = 12

SCL = 19
SDA = 18

A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A5 = 19
A6 = 20
A7 = 21
A8 = 22
A9 = 23
A10 = 34
A11 = 35
A12 = 36
A13 = 37
A14 = 40
A15 = 26
A16 = 27
A17 = 28
A18 = 29
A19 = 30
A20 = 31

ADC_REF_DEFAULT = 0
ADC_REF_ALT = 1
ADC_REF_3V3 = ADC_REF_DEFAULT
ADC_REF_1V2 = ADC_REF_ALT

ANALOG_CHANNELS = pd.Series([A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11,
                             A12, A13, A14, A15, A16, A17, A18, A19, A20],
                            index=['A%d' % i for i in xrange(21)])
