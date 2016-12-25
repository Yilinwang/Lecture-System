from subprocess import *

p = Popen(['python3', 'retrieval.py'], stdout=PIPE, stdin=PIPE)

def send(s):
    return p.communicate(s.encode('utf8'))[0].decode('utf8')
