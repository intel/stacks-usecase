import sys
import os
import handler

def print_os():
    return os.system("cat /etc/*-release")

if __name__ == "__main__":
    st = print_os()
    ret = handler.handle(st)
    if ret != None:
        print(ret)
