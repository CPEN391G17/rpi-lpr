import textwrap
import requests
import time
import binascii
from Connect import *

integer = 7
def print_roundtrip(response, *args, **kwargs):
    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res.text}
    ''').format(
        req=response.request,
        res=response,
        reqhdrs=format_headers(response.request.headers),
        reshdrs=format_headers(response.headers),
    ))
    bytearr = binascii.hexlify(bytearray(response.text, "utf8"))
    print(bytearr)
    j = 0
    for i in range(len(bytearr)):
        if(bytearr[i] == '\xc2'):
            j = i
    print(response.text)
    print("modified bytearr:",format(bytearr))
    bytearr1 = b'000025a7'
    print("int val: {}".format(int(response.text)))
    integer = int(response.text)
    print("Actual integer received: {}".format(integer))
    print("Not returning")
    print("Not returning")
    print("Not returning")

    exit()

# requests.get('http://192.168.4.1/Logo_Terasic.jpg', hooks={'response': print_roundtrip})
# import requests
#
#
#
#
url = 'http://192.168.4.1/led'
# myobj = "data: The ASCII character set is the most common compatible subset of character sets for English-language text files, and is generally assumed to be the default file format in many situations. It covers American English, but for the British Pound sign, the Euro sign, or characters used outside English, a richer character set must be used. In many systems, this is chosen based on the default locale setting on the computer it is read on. Prior to UTF-8, this was traditionally single-byte encodings (such as ISO-8859-1 through ISO-8859-16) for European languages and wide character encodings for Asian languages.A text file (sometimes spelled textfile; an old alternative name is flatfile) is a kind of computer file that is structured as a sequence of lines of electronic text. A text file exists stored as data within a computer file system. In operating systems such as CP/M and MS-DOS, where the operating system does not keep track of the file size in bytes, the end of a text file is denoted by placing one or more special characters, known as an end-of-file marker, as padding after the last line in a text file. On modern operating systems such as Microsoft Windows and Unix-like systems, text files do not contain any special EOF character, because file systems on those operating systems keep track of the file size in bytes. There are for most text files a need to have end-of-line delimiters, which are done in a few different ways depending on operating system. Some operating systems with record-orientated file systems may not use new line delimiters and will primarily store text files with lines separated as fixed or variable length records.\nend\r\n"#{'api_option':'paste'}
myobj = "data: \x07\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\nend\r\n"#(bytearray([1, 2, 3, 4])) here \x77 is the signalling byte
obj2 = "data: \x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\0\nend\r\n"
obj3 = "data: \x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\x0A\x0B\x0C\x0D\x0E\x0F\0\nend\r\n"
# start = "data: "
mid = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
# end = "\nend\r\n"
# realobj = (start + (mid*34) + end)
# TimeDuration = 137
# TimeObj = start + str(TimeDuration) + end

barray = bytearray([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
0x00, 0x01, 0x00, 0x00, 0xFF, 0xE1, 0x00, 0x62, 0x45, 0x78, 0x69, 0x66, 0x00, 0x00, 0x4D, 0x4D,
0x00, 0x2A, 0x00, 0x00, 0x00, 0x08, 0x00, 0x05, 0x01, 0x12, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01,
0x00, 0x01, 0x00, 0x00, 0x01, 0x1A, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x4A,
0x01, 0x1B, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x52, 0x01, 0x28, 0x00, 0x03,
0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x02, 0x13, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01,
0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0xFF, 0xDB, 0x00, 0x43, 0x00, 0x08, 0x06, 0x06,
0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09, 0x09, 0x08, 0x0A, 0x0C, 0x15, 0x0E, 0x0C, 0x0B,
0x0B, 0x0C, 0x19, 0x12, 0x13, 0x0F, 0x15, 0x1E, 0x1B, 0x20, 0x1F, 0x1E, 0x1B, 0x1D, 0x1D, 0x21,
0x25, 0x30, 0x29, 0x21, 0x23, 0x2D, 0x24, 0x1D, 0x1D, 0x2A, 0x39, 0x2A, 0x2D, 0x31, 0x33, 0x36,
0x36, 0x36, 0x20, 0x28, 0x3B, 0x3F, 0x3A, 0x34, 0x3E, 0x30, 0x35, 0x36, 0x33, 0xFF, 0xDB, 0x00,
0x43, 0x01, 0x09, 0x09, 0x09, 0x0C, 0x0B, 0x0C, 0x18, 0x0E, 0x0E, 0x18, 0x33, 0x22, 0x1D, 0x22,
0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33])
# req = requests.Request('POST',url,data=TimeObj)
# prepared = req.prepare()


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

# pretty_print_POST(prepared)

# try:
#     x = requests.post(url, data=TimeObj, hooks={'response': print_roundtrip})
# except:
#     x = requests.post(url, data=TimeObj, hooks={'response': print_roundtrip})
# print("returned")

# resp.hooks['response'] = [print_roundtrip]
# resp.post(url, data=TimeObj, hooks={'response': print_roundtrip})
# print(resp.hooks)
# print("int received: {}".format(integer))
def print_hook(response, *args, **kwargs):
    print("int val: {}".format((response.text)))
    global integer
    integer = int(response.text)
    print("Actual integer received: {}".format(integer))
    return integer

def Request_RFS(Obj):
    resp = requests.Session()
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

