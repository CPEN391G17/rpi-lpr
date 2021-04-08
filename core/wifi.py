import requests
import time
import binascii
from Connect import *


integer = 7 #Global Variable





def print_hook(response, *args, **kwargs):
    print("int val: {}".format((response.text)))
    global integer
    integer = int(response.text)
    print("Actual integer received: {}".format(integer))
    return integer

def Request_RFS(Obj):
    resp = requests.Session()
    url = 'http://192.168.4.1/led'
    try:
        resp.hooks['response'] = [print_hook]
        resp.post(url, data=Obj)
    except:
        print(7)
        print("Finally the received integer: {}".format(integer))
    return

def error_handling(exp, num):
    if (exp != num):
        print("Expected: {}".format(exp))
        if (exp > num):
            error = exp - num
            num = num + error
        else:
            error = integer - exp
            num = num - error
    return num


def Call_Everything():
    start = "data: "
    end = "\nend\r\n"
    TimeDuration = 137
    TimeObj = start + str(TimeDuration) + end
    """Post Data After Connection to RFS"""
    print()  # Change_Connection() #Connect to RFS
    Connect_RFS()
    print("Connection To RFS estabilished")
    time.sleep(7)  # wait for connection to be estabilished
    expected = (TimeDuration * 7)
    Request_RFS(TimeObj)
    print("FINALLY THE INTEGER OUT OF THE HOOK: {}".format(integer))
    num = integer
    e_integer = error_handling(expected, num)
    print("Correct Integer: {}".format(integer))

    Connect_Home()
    print("Connection to HOME NETWORK estabilished")
    time.sleep(2)
    # Change_Connection() #Connect to Home
    # with requests.get(url, data=TimeObj, hooks={'response': print_hook}) as r:
    #     print(r.content)

Call_Everything()
