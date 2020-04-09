import json
from collections import defaultdict

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

        def beats_to_ms(x, b): return 60*1000*x/b

        self.presets = defaultdict(lambda: ((440,), (1000,)))

        bpm = 120
        freqs = (330, 330, 0, 415, 349, 330, 415, 415, 0, 493, 440, 415, 440, 400, 0, 523, 493, 440, 415, 349, 330, 349, 415)
        beats = (2,   2,   1, 1,   1,   1,   2,   2,   1, 1,   1,   1,   2,   2,   1, 1,   1,   1,   1,   0.5, 0.5, 1,   3)
        self.presets['hava_nagila'] = (
            freqs,
            map(lambda x: int(beats_to_ms(x, bpm)), beats)
        )

        bpm = 125
        freqs = (392,  392,  440, 392, 523, 494)
        beats = (0.75, 0.25, 1,   1,   1,   2)
        self.presets['happy_birthday'] = (
            freqs,
            map(lambda x: int(beats_to_ms(x, bpm)), beats)
        )

        # TODO: find notes for below
        bpm = 100
        freqs = (392,  392,    440,    392,    523,    494)
        beats = (0.75,  0.25,   1,      1,      1,      2)
        self.presets['mario_pipe_theme'] = (
            freqs,
            map(lambda x: int(beats_to_ms(x, bpm)), beats)
        )

        bpm = 100
        freqs = (659, 659, 0,   659, 0,   523, 659,  0,    784,  0,    392)
        beats = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.75, 0.25, 1.75, 0.25)
        self.presets['mario_main_theme'] = (
            freqs,
            map(lambda x: int(beats_to_ms(x, bpm)), beats)
        )


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
                "preset":
                {
                    "label": "Preset",
                    "description": "A preset sequence of tones to play.",
                    "type": "enum",
                    "options": {
                        "none": "None",
                        "hava_nagila": "Hava Nagila",
                        "happy_birthday": "Happy Birthday",
                        "mario_pipe_theme": "Mario (Pipe Theme)",
                        "mario_main_theme": "Mario (Main Theme)"
                    },
                    "default_value": "none"
                },
                "beep_frequency":
                {
                    "label": "Frequency",
                    "description": "Frequency of the beep.",
                    "type": "int",
                    "unit": "Hz",
                    "default_value": 440,
                    "minimum_value": 0,
                    "maximum_value": 10000,
                    "enabled": "preset=='none'"
                },
                "beep_duration":
                {
                    "label": "Duration",
                    "description": "Duration of the beep.",
                    "type": "int",
                    "unit": "ms",
                    "default_value": 500,
                    "minimum_value": 0,
                    "maximum_value": 5000,
                    "enabled": "preset=='none'"
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
        preset = self.getSettingValueByKey("preset")
        event = self.getSettingValueByKey("beep_on")
        do_pause = self.getSettingValueByKey("pause_after_beep")

        if preset == "none":
            frequency = (self.getSettingValueByKey("beep_frequency"),)
            duration = (self.getSettingValueByKey("beep_duration"),)
        else:
            frequency, duration = self.presets[preset]
        target_gcode = '\n'.join(map(lambda f, d: "M300 S" + str(f) + " P"  + str(d), frequency, duration))
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









