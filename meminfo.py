#!/usr/bin/env python3
#coding:utf-8
import time
import signal
from threading import Timer

def job():
    info = []
    with open('/proc/meminfo') as meminfo:
        for i in range(4):
            line = meminfo.readline()
            name = line.split(':')[0]
            value = line.split(':')[1].strip().split(' ')[0]
            info.append([name, value])

    with open('meminfo.log', 'a+') as outlog:
        outlog.write(time.ctime()+'\t')
        for record in info:
            outlog.write(record[0].strip()+':'+record[1].strip()+'\t')
        outlog.write('\n\r')

def main():
    try:
        while True:
            job()
            time.sleep(5)
    except KeyboardInterrupt:
        print('exit')

if __name__ == '__main__':
    main()
