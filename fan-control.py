# https://www.instructables.com/PWM-Regulated-Fan-Based-on-CPU-Temperature-for-Ras/
# Used this for finding fan's min % at which the fan started spinning. Which was 35. Used 40 to be safe

import RPi.GPIO as GPIO
import time
import sys

# Configuration
FAN_PIN = 12  # BCM pin used to drive transistor's base
WAIT_TIME = 3  # [s] Time to wait between each refresh
FAN_MIN = 40  # [%] Fan minimum speed at which the fan starts spinning
PWM_FREQ = 25  # [Hz] Change this value if fan has strange behavior

# Configurable temperature and fan speed steps
tempSteps = [53, 65, 75]  # [°C] Fan will start running at 55°C
speedSteps = [55, 80, 100]  # [%]

# Fan speed will change only if the difference of temperature is higher than hysteresis
hyst = 3

# Setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(0)

cpuTemp = 0
fanSpeed = 0
cpuTempOld = 0
fanSpeedOld = 0

# We must set a speed value for each temperature step
if len(speedSteps) != len(tempSteps):
    print("Numbers of temp steps and speed steps are different")
    exit(0)

try:
    while True:
        # Read CPU temperature
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as cpuTempFile:
            cpuTemp = float(cpuTempFile.read()) / 1000

        # Print current CPU temperature
        print(f"CPU {cpuTemp:.1f} °C -- FAN {fanSpeedOld} %")

        # Calculate desired fan speed only if the temperature is above the threshold
        if cpuTemp > tempSteps[0] and abs(cpuTemp - cpuTempOld) > hyst:
            # Below first value, fan will run at min speed.
            if cpuTemp < tempSteps[0]:
                fanSpeed = speedSteps[0]
            # Above last value, fan will run at max speed
            elif cpuTemp >= tempSteps[-1]:
                fanSpeed = speedSteps[-1]
            # If temperature is between 2 steps, fan speed is calculated by linear interpolation
            else:
                for i in range(len(tempSteps) - 1):
                    if (cpuTemp >= tempSteps[i]) and (cpuTemp < tempSteps[i + 1]):
                        fanSpeed = round((speedSteps[i + 1] - speedSteps[i])
                                         / (tempSteps[i + 1] - tempSteps[i])
                                         * (cpuTemp - tempSteps[i])
                                         + speedSteps[i], 1)

            if fanSpeed != fanSpeedOld:
                if (fanSpeed >= FAN_MIN or fanSpeed == 0):
                    fan.ChangeDutyCycle(fanSpeed)
                    fanSpeedOld = fanSpeed
                    print(f"Fan Speed set to: {fanSpeed:.1f}%")

            cpuTempOld = cpuTemp
        else:
            if cpuTemp < tempSteps[0]:  # Ensure fan is off below 55°C
                fan.ChangeDutyCycle(0)
                fanSpeedOld = 0
                print(f"Fan is OFF (Temperature below {tempSteps[0]:.1f} °C)")

        # Wait until next refresh
        time.sleep(WAIT_TIME)

# If a keyboard interrupt occurs (ctrl + c), the GPIO is set to 0 and the program exits.
except KeyboardInterrupt:
    print("Fan control interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
