import sys
from time import sleep as s
import RPi.GPIO as g

g.setmode(g.BCM)
p = 17
g.setup(p, g.OUT)
g.output(p, g.HIGH)
s(.1)

max_time = 7.446
light_dim = float(sys.argv[1]) * .01

if light_dim == 0:
    # g.output(p, g.HIGH)
    print('off')
elif light_dim == 1:
    g.output(p, g.LOW)
    s(max_time)
    print('highest')
else:
    print('dim at', light_dim)
    dim_time = max_time * light_dim
    #on
    print('on')
    g.output(p, g.LOW)
    s(dim_time)
    #off
    print('off')
    g.output(p, g.HIGH)
    s(.1)
    #on
    print('stay in dim')
    g.output(p, g.LOW)
# print(max_time * light_dim)


# print (sys.argv[1])