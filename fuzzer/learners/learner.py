#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 

'''

from pylstar.LSTAR import LSTAR
from I2C import I2CMachineKnowledgeBase
from CoffeeMachineTest import CoffeeMachineKnowledgeBase

# list of messages accepted by the coffee machine
input_vocabulary = [
    "REFILL_WATER",
    "REFILL_COFFEE",
    "PRESS_BUTTON_A",
    "PRESS_BUTTON_B",
    "PRESS_BUTTON_C"
]
# instanciates our CoffeeMachine MAT
Device = CoffeeMachineKnowledgeBase("CoffeeMachineTest.py")
try:
    # starts the coffee machine
    Device.start()
    # learns its grammar
    lstar = LSTAR(input_vocabulary, Device, max_states=10)
    # stores the coffee machine state machine
    i2c_state_machine = lstar.learn()

    # displays the DOT code of the state machine
    print(i2c_state_machine.build_dot_code())
finally:
    Device.stop()    