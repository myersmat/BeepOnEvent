import json

from ..Script import Script
from UM.Logger import Logger


class BeepOnEvent(Script):
    # TODO: Add print_complete support
    def __init__(self):
        self.event_gcode_dict = {
            'bed_finished_heating': 'M190',
            'tool_finished_heating': 'M109',
            'pause': 'M226',
            'print_complete':';End of Gcode'
        }        
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
                                "tool_finished_heating": "Tool Finished Heating",
                                "pause": "Pause",
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
        event = self.getSettingValueByKey("beep_on")
        f = self.getSettingValueByKey("beep_frequency")
        duration = self.getSettingValueByKey("beep_duration")
        do_pause = self.getSettingValueByKey("pause_after_beep")
        target_gcode = "M300 S" + str(f) + " P"  + str(duration)
        search_gcode = self.event_gcode_dict[event]
        if do_pause:
            target_gcode += "\n" + self.event_gcode_dict['pause']
        for layer_idx, layer in enumerate(data):
            lines = layer.split('\n')
            line_inc = 0 if event == 'print_complete' else 1
            for line_idx, line in enumerate(lines[:]):
                if event != 'print_complete':
                    if len(line) > 0 and line[0] != ';' and search_gcode in line:
                        lines.insert(line_idx + line_inc, target_gcode)
                        line_inc += 1
                else:
                    if search_gcode in line:
                        lines.insert(line_idx + line_inc, target_gcode)
                        line_inc += 1

            data[layer_idx] = '\n'.join(lines)
        return data

                    


                        
                        



        