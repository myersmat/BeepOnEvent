import json
import re

from ..Script import Script
from UM.Logger import Logger

class BeepOnEvent(Script):
    def __init__(self):
        super().__init__()
        
    
    def getSettingDataString(self):
        return """{
            "name": "Beep On Event",
            "key": "BeepOnEvent",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "beep_on":
                {
                    "label": "Beep on",
                    "description": "Event type to beep on.",
                    "type": "enum",
                    "options": {"bed_finished_heating": "Bed Finished Heating",
                                "nozzle_finished_heating": "Nozzle Finished Heating",
                                "print_complete": "Print Complete"},
                    "default_value": "bed_finished_heating"
                },
                "beep_frequency":
                {
                    "label": "Frequency",
                    "description": "Frequency of the beep.",
                    "type": "int",
                    "unit": "Hz",
                    "default_value": 440,
                    "minimum_value": 0,
                    "maximum_value": 10000
                },
                "beep_duration":
                {
                    "label": "Duration",
                    "description": "Duration of the beep.",
                    "type": "int",
                    "unit": "ms",
                    "default_value": 500,
                    "minimum_value": 0,
                    "maximum_value": 5000
                },
                "pause_after_beep":
                {
                    "label": "Pause after beep",
                    "description": "If checked, insert a pause after the beep.",
                    "type": "bool",
                    "default_value": false
                }
            }
        }"""
                
    def execute(self, data):
        with open('C:/Users/mattm/xtest.txt', 'w') as f:
            f.write(str(type(data)))
            f.write('\n')
            f.write(str(tdata[0]))
            f.write('\n')
            f.write(str(tdata[1]))
            f.write('\n')
            f.write(str(tdata[2]))
            f.write('\n')
            f.write(str(tdata[3]))
            f.write('\n')
            f.write(str(tdata[4]))
            f.write('\n')
            f.write(str(tdata[5]))
            f.write('\n')
            f.write(str(tdata[6]))
            f.write('\n')
            f.write(str(tdata[7]))
        