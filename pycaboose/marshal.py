import base64
import pickle


def decode(s):
    return pickle.loads(base64.b64decode(s[2:]))


def encode(data):
    x = base64.b64encode(pickle.dumps(data))
    return b'# ' + x + b'\n'
