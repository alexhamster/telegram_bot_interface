#!/usr/bin/python3
import time
import subprocess
import datetime


def main():
    while True:
        try:
            process = subprocess.Popen(['python3', './run.py'])
            code = process.wait()
            if not (code == 0):
                now_time = str(datetime.datetime.now())
                print('Crash!' + now_time)
        except Exception as e:
            print(repr(e))
        time.sleep(5)


if __name__ == '__main__':
    print('Running...')
    main()