import json
import curses

mapping  = {
    'KEY_LEFT': [curses.KEY_LEFT],
    'KEY_RIGHT': [curses.KEY_RIGHT],
    'KEY_UP': [curses.KEY_UP],
    'KEY_DOWN': [curses.KEY_DOWN],
    'KEY_ENTER': [curses.KEY_ENTER, ord('\n'), ord('\r')],
    'KEY_ESC': [27]
}

def to_key_codes(key):
    if key in mapping:
        return mapping[key]

    return [ord(key)]

def flatten(seq):
    return [elem for subseq in seq for elem in subseq]

controls = json.load(open('controls.json'))
controls = {k: [to_key_codes(key) for key in v] for k, v in controls.items()}
controls = {k: flatten(v) for k, v in controls.items()}
