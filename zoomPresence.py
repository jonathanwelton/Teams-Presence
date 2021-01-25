# !/usr/bin/env python
# Python script to show Zoom presence status on led
# Author: Jonathan Welton
# Date 09.01.2021

version = 1.0
workday_start = None
workday_end = None
workdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
width = 0
height = 0
blinkThread = None
after_work = False
globalRed = 0
globalGreen = 0
globalBlue = 0
points = []
brightness_led = 0.5
sleepValue = 30  # seconds

# Define Error Logging


def printerror(ex):
    print('\033[31m' + str(ex) + '\033[0m')


def printwarning(warn):
    print('\033[33m' + str(warn) + '\033[0m')


def printgreen(msg):
    print('\033[32m' + str(msg) + '\033[0m')


def printyellow(msg):
    print('\033[33m' + str(warn) + '\033[0m')


def printred(msg):
    print('\033[31m' + str(ex) + '\033[0m')


def printblue(msg):
    print('\033[34m' + str(ex) + '\033[0m')


def printblink(msg):
    print('\033[5m' + str(ex) + '\033[0m')


print("Loading modules...")

try:
    import requests
    import socket
    import os
    import argparse
    from random import randint
    from urllib.error import HTTPError
    import json
    import unicornhat as unicorn
    import threading
    import sys
    import urllib.parse
    import configparser
    from time import sleep
    from datetime import datetime, time
    from signal import signal, SIGINT
    from gpiozero import CPUTemperature
except ModuleNotFoundError as ex:
    printerror("The app could not be started.")
    printerror("Please run 'sudo ./install.sh' first.")
    printerror(ex)
    exit(2)
except:
    printerror("An unknown error occured while loading modules.")
    exit(2)

# Check for arguments
parser = argparse.ArgumentParser()
parser.add_argument("--version", "-v",
                    help="Prints the version", action="store_true")
parser.add_argument("--refresh", "-r",
                    help="Sets the refresh value in seconds", type=int)
parser.add_argument("--brightness", "-b",
                    help="Sets the brightness of the LED display. Value must be between 0.1 and 1", type=int)
parser.add_argument("--afterwork", "-aw",
                    help="Check for presence after working hours", action="store_true")
parser.add_argument("--nopulse", "-np",
                    help="Disables pulsing, if after work hours", action="store_true")

args = parser.parse_args()
if args.version:
    print(str(version))
    exit(0)

if args.nopulse:
    printwarning("Option: No pulsing")

if args.refresh:
    if args.refresh < 10:
        printerror("Refresh value must be greater than 10")
        exit(4)
    sleep = args.refresh
    printwarning("Option: Sleep set to " + str(sleep))

if args.brightness:
    if args.brightness < 0.1 and args.brightness > 1:
        printerror("Value must be between 0.1 and 1")
        exit(5)
    brightness = args.brightness
    printwarning("Option: Brightness set to " + str(brightness))

if args.afterwork:
    printwarning("Option: Set after work to true")

# Get the width and height of the hardware
width, height = unicorn.get_shape()

workday_start = time(9)
workday_end = time(18)

# Handles Ctrl+C


def handler(signal_received, frame):
    # Handle any cleanup here
    print()
    printwarning(
        'SIGINT or CTRL-C detected. Please wait until the service has stopped.')
    blinkThread.do_run = False
    blinkThread.join()
    switchOff()
    exit(0)

# Disable Printing


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Printing


def enablePrint():
    sys.stdout = sys.__stdout__

# Check times


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    try:
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else:  # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    except:
        printerror("Could not verify times. " + sys.exc_info()[0])
        return False

# Countdown for minutes


def countdown(t):
    total = t
    progvalue = 0
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Time until next run: " + timer, end="\r")
        sleep(1)
        t -= 1
    print("                                      ", end="\r")


# Check or internet connection


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# Checks for updates


def checkUpdate():
    updateUrl = "https://raw.githubusercontent.com/maxi07/Teams-Presence/master/doc/version"
    try:
        f = requests.get(updateUrl, timeout=10)
        latestVersion = float(f.text)
        if latestVersion > version:
            printwarning("There is an update available.")
            printwarning(
                "Head over to https://github.com/maxi07/Teams-Presence to get the latest features.")
        else:
            print("Application is running latest version.")
    except Exception as e:
        printerror("An error occured while searching for updates.")
        printerror(e)

# ############################
#        UNICORN SETUP
# ############################


def setColor(r, g, b, brightness, speed):
    global crntColors, globalBlue, globalGreen, globalRed
    globalRed = r
    globalGreen = g
    globalBlue = b

    if brightness == '':
        unicorn.brightness(brightness_led)

    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, r, g, b)
            unicorn.show()


def pulse():
    for b in range(0, 7):
        blockPrint()
        unicorn.brightness(b/10)
        enablePrint()
        for y in range(height):
            for x in range(width):
                unicorn.set_pixel(x, y, 102, 255, 255)
                unicorn.show()
        sleep(0.05)
    sleep(1)
    for b in range(6, 0, -1):
        blockPrint()
        unicorn.brightness(b/10)
        enablePrint()
        for y in range(height):
            for x in range(width):
                unicorn.set_pixel(x, y, 102, 255, 255)
                unicorn.show()
        sleep(0.05)


def switchBlue():
    red = 0
    green = 0
    blue = 250
    blinkThread = threading.Thread(
        target=setColor, args=(red, green, blue, '', ''))
    blinkThread.do_run = True
    blinkThread.start()


def switchRed():
    red = 250
    green = 0
    blue = 0
    blinkThread = threading.Thread(
        target=setColor, args=(red, green, blue, '', ''))
    blinkThread.do_run = True
    blinkThread.start()


def switchGreen():
    red = 0
    green = 250
    blue = 0
    blinkThread = threading.Thread(
        target=setColor, args=(red, green, blue, '', ''))
    blinkThread.do_run = True
    blinkThread.start()


def switchPink():
    red = 255
    green = 108
    blue = 180
    blinkThread = threading.Thread(
        target=setColor, args=(red, green, blue, '', ''))
    blinkThread.do_run = True
    blinkThread.start()


def switchYellow():
    red = 255
    green = 255
    blue = 0
    blinkThread = threading.Thread(
        target=setColor, args=(red, green, blue, '', ''))
    blinkThread.do_run = True
    blinkThread.start()


def switchOff():
    global blinkThread, globalBlue, globalGreen, globalRed
    globalRed = 0
    globalGreen = 0
    globalBlue = 0
    if blinkThread != None:
        blinkThread.do_run = False
    unicorn.clear()
    unicorn.off()


class LightPoint:

    def __init__(self):
        self.direction = randint(1, 4)
        if self.direction == 1:
            self.x = randint(0, width - 1)
            self.y = 0
        elif self.direction == 2:
            self.x = 0
            self.y = randint(0, height - 1)
        elif self.direction == 3:
            self.x = randint(0, width - 1)
            self.y = height - 1
        else:
            self.x = width - 1
            self.y = randint(0, height - 1)

        self.colour = []
        for i in range(0, 3):
            self.colour.append(randint(100, 255))


def update_positions():

    for point in points:
        if point.direction == 1:
            point.y += 1
            if point.y > height - 1:
                points.remove(point)
        elif point.direction == 2:
            point.x += 1
            if point.x > width - 1:
                points.remove(point)
        elif point.direction == 3:
            point.y -= 1
            if point.y < 0:
                points.remove(point)
        else:
            point.x -= 1
            if point.x < 0:
                points.remove(point)


def plot_points():

    unicorn.clear()
    for point in points:
        unicorn.set_pixel(point.x, point.y,
                          point.colour[0], point.colour[1], point.colour[2])
    unicorn.show()


def blinkRandom(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        if len(points) < 10 and randint(0, 5) > 1:
            points.append(LightPoint())
        plot_points()
        update_positions()
        sleep(0.03)

##################################################


def printHeader():
    # Get CPU temp
    cpu = CPUTemperature()

    os.system('clear')
    print("============================================")
    print("               Zoom Presence")
    print("============================================")
    print()
    cpu_r = round(cpu.temperature, 2)
    print("Current CPU:\t\t" + str(cpu_r) + "°C")


# Check for Weekend


def check_weekend():
    now = datetime.now()
    while now.strftime("%A") not in workdays:
        printHeader()
        now = datetime.now()
        print("It's " + now.strftime("%A") +
              ", weekend! Grab more beer! \N{beer mug}")
        print()
        if args.nopulse:
            switchOff()
        else:
            pulsethread = threading.Thread(target=pulse)
            pulsethread.start()

        countdown(30)


# Check for working hours


def check_workingtimes():
    if args.afterwork:
        return

    # Get CPU temp
    cpu = CPUTemperature()

    while is_time_between(workday_start, workday_end) == False:
        printHeader()
        now = datetime.now()
        print("Work is over for today, grab a beer! \N{beer mug}")
        print()

        if args.nopulse:
            switchOff()
        else:
            pulsethread = threading.Thread(target=pulse)
            pulsethread.start()

        countdown(30)


# Main


def run():
    print("Welcome to Zoom presence for Pi!")

    print("Booting v" + str(version))

    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    # Check internet
    if is_connected == False:
        printerror(
            "No network. Please connect to the internet and restart the app.")
        exit(3)

    # Check for updates
    checkUpdate()

    # Setup Unicorn light
    setColor(50, 50, 50, 1, '')
    unicorn.set_layout(unicorn.AUTO)
    unicorn.brightness(0.5)

    blinkThread = threading.Thread(target=blinkRandom, args=("task",))
    blinkThread.do_run = True
    blinkThread.start()

    while True:
        check_weekend()
        check_workingtimes()

        # Check network
        if is_connected() == False:
            printerror("No network is connected. Waiting for reconnect.")
            countdown(30)
            continue

        print("Fetching new data")
        config = configparser.ConfigParser()
        config.read("config.ini")
        url = config.get('presence_api', 'url')
        token = config.get('presence_api', 'token')

        headers = {'Authorization': token}

        jsonresult = ''

        trycount = 0

        try:
            result = requests.get(
                f'{url}', headers=headers, timeout=5)
            result.raise_for_status()
            jsonresult = result.json()

        except requests.exceptions.Timeout as timeerr:
            printerror(
                "The request for Zoom Presence API timed out! " + str(timeerr))
            continue

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                printerror("Zoom Presence API URL is invalid!")
                exit(5)
            elif err.response.status_code == 401:
                blinkThread = threading.Thread(
                    target=blinkRandom, args=("task",))
                blinkThread.do_run = True
                blinkThread.start()

                trycount = trycount + 1
                printerror(
                    "Zoom Presence API is not authorized. Please reauthorize the app (401). Try count: " + str(trycount))
                print()
                Authorize()
                continue

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Will try again. Try count: " + str(trycount))
            print()
            countdown(int(sleepValue))
            continue

        trycount = 0

        # Check for jsonresult
        if jsonresult == '':
            printerror("JSON result is empty! Will try again.")
            printerror(jsonresult)
            countdown(5)
            continue

        # Stop random blinking
        if blinkThread != None:
            blinkThread.do_run = False
            blinkThread.join()

        # Get CPU temp
        cpu = CPUTemperature()

        # Print to display
        os.system('clear')
        print("============================================")
        print("               Zoom Presence")
        print("============================================")
        print()
        now = datetime.now()
        print("Last API call:\t\t" + now.strftime("%Y-%m-%d %H:%M:%S"))
        cpu_r = round(cpu.temperature, 2)
        print("Current CPU:\t\t" + str(cpu_r) + "°C")

        if args.brightness:
            printwarning("Option:\t\t\t" +
                         "Set brightness to " + str(brightness))

        if args.refresh:
            printwarning("Option:\t\t\t" + "Set refresh to " + str(sleepValue))

        if args.nopulse:
            printwarning("Option:\t\t\t" + "Pulsing disabled")

        if args.afterwork:
            printwarning("Option:\t\t\t" + "Set display after work to True")

        if jsonresult['activity'] == "Available":
            print("Zoom presence:\t\t" + '\033[32m' + "Available" + '\033[0m')
            switchGreen()
        elif jsonresult['activity'] == "In_Calendar_Event":
            print("Zoom presence:\t\t" +
                  '\033[31m' + "In Calendar Event" + '\033[0m')
            switchPink()
        elif jsonresult['activity'] == "Away":
            print("Zoom presence:\t\t" + '\033[33m' + "Away" + '\033[0m')
            switchGreen()
        elif jsonresult['activity'] == "Do_Not_Disturb":
            print("Zoom presence:\t\t" +
                  '\033[31m' + "Do Not Disturb" + '\033[0m')
            switchPink()
        elif jsonresult['activity'] == "In_Meeting":
            print("Zoom presence:\t\t" +
                  '\033[31m' + "In a meeting" + '\033[0m')
            switchPink()
        elif jsonresult['activity'] == "Presenting":
            print("Zoom presence:\t\t" +
                  '\033[31m' + "Presenting" + '\033[0m')
            switchRed()
        else:
            print("Zoom presence:\t\t" + "Unknown")
            switchBlue()
        print()
        countdown(int(sleepValue))
