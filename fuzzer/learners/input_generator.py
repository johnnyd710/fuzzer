#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 

'''

from pylstar.LSTAR import LSTAR
from abstraction.i2c_machine import I2CMachineKnowledgeBase

# list of messages accepted by the coffee machine
input_vocabulary = [
    "REFILL_WATER",
    "REFILL_COFFEE",
    "PRESS_BUTTON_A",
    "PRESS_BUTTON_B",
    "PRESS_BUTTON_C"
]
# instanciates our CoffeeMachine MAT
I2CBase = I2CMachineKnowledgeBase()
try:
    # starts the coffee machine
    I2CBase.start()
    # learns its grammar
    lstar = LSTAR(input_vocabulary, I2CBase, max_states = 10)
    # stores the coffee machine state machine
    i2c_state_machine = lstar.learn()

    # displays the DOT code of the state machine
    print(i2c_state_machine.build_dot_code())
finally:
   I2CBase.stop()
        