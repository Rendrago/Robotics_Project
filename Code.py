#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
driveMotors_motor_a = Motor(Ports.PORT9, True)
driveMotors_motor_b = Motor(Ports.PORT10, False)
driveMotors = MotorGroup(driveMotors_motor_a, driveMotors_motor_b)
lightSensor = Light(brain.three_wire_port.a)
distanceSensor = Distance(Ports.PORT1)
rightLineTracker = Line(brain.three_wire_port.b)
middleLineTracker = Line(brain.three_wire_port.c)
leftLineTracker = Line(brain.three_wire_port.d)
motor_2 = Motor(Ports.PORT2, False)
# AI Vision Color Descriptions
visionSensor__RedRing = Colordesc(1, 221, 20, 72, 10, 0.2)
visionSensor__BlueRing = Colordesc(2, 6, 27, 126, 10, 0.2)
# AI Vision Code Descriptions
visionSensor = AiVision(Ports.PORT3, visionSensor__RedRing, visionSensor__BlueRing)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:     Intro to Robotics
#	Author:       
#	Created:
#	Description:  Intro to Robotics Class File
# 
# ------------------------------------------

# Library imports
from vex import *

#Function Section
'''
Description: Moves the robot linearly for a given distance
Arg:
- distance (float): distance in inches
Returns:
- None
''' 
#def linear_movement(distance):
def linear_movement(distance):
    #change motor speed
    driveMotors.set_velocity(200,RPM)

    #calculate number of rotations
    circumfrence = 3.25 * 3.14
    rotations = distance / circumfrence

    #spins motor set number of rotations then stops
    driveMotors.spin_for(FORWARD,rotations,TURNS)
    driveMotors.stop()

'''
Description: Turns robot a set number of degrees manually
Arg:
- degrees (float): a number in degrees
Returns:
- None
''' 

def linear_inertial(velocityOfVehicle, distanceFromObject):
    kp = 0.8
    brain_inertial.set_rotation(0,DEGREES)
    driveMotors.set_velocity(velocityOfVehicle,RPM)
    driveMotors.spin(FORWARD)
    #conditional control group
    while True:
        #if an object is at a set distance
        if distanceReading <= distanceFromObject:
            break
        else:
            #calculate the error from facing straight
            error = 0 - brain_inertial.rotation(DEGREES)
            speed = error * kp

            driveMotors_motor_a.set_velocity(velocityOfVehicle + speed, PERCENT)
            driveMotors_motor_b.set_velocity(velocityOfVehicle - speed, PERCENT)

            driveMotors_motor_a.spin(FORWARD)
            driveMotors_motor_a.spin(FORWARD)
    driveMotors.stop()


def robot_turn(degrees):
    #change motor speed
    driveMotors.set_velocity(25,PERCENT)

    #calculate wheel circumference
    wheelCircumference = 3.25 * 3.14

    #calculate robot circumference
    robotCircumference = 3.14 * 7.75

    #calculate arc length
    arcLength = (degrees/360)* robotCircumference

    #calculate rotations
    rotations = arcLength / wheelCircumference

    #spins motor set number of rotations then stops
    driveMotors_motor_a.spin_for(FORWARD,rotations,TURNS,wait=False)
    driveMotors_motor_b.spin_for(REVERSE, rotations, TURNS)
    driveMotors.stop()

    driveMotors_motor_a.spin_for(FORWARD,2) 
    #activates just motor A
    driveMotors_motor_b.spin_for(FORWARD,2) 
    #activates just motor B



'''
Description: Turns robot using the inertial sensor data
# of Sensors: 1
Arg:
- degrees (float): a number in degrees
Returns:
- None
''' 
def inertial_turn(degrees):
    #proportional percentage
    kp = 0.8
    #reset rotation value
    brain_inertial.set_rotation(0,DEGREES)

    while True:
        #calculate error in relation to closeness of desired degree
        gError = degrees - brain_inertial.rotation(DEGREES)

        #we will stop within 1.5 degrees from the target
        if ( abs(gError) <1.5):
            break

        #adjust speed based on error and proportional
        speed = gError * kp
        driveMotors.set_velocity(-speed,PERCENT)
        driveMotors_motor_a.spin(REVERSE)
        driveMotors_motor_b.spin(FORWARD)

    #stop turn
    driveMotors.stop()    

def inertial_line_follower(motorSpeed,Kp):
    threshold = (ltRightReading + ltMiddleReading + ltLeftReading)/3
    driveMotors.set_velocity(motorSpeed,PERCENT)
    driveMotors.spin(FORWARD)
    '''while True:
        leftError = ltRightReading - threshold
        rightError = ltLeftReading - threshold
        driveMotors.set_velocity(motorSpeed,PERCENT)
        driveMotors.spin(FORWARD)
        if ltLeftReading <= threshold:
            driveMotors_motor_a.set_velocity(Kp*rightError,PERCENT)
            driveMotors_motor_a.spin(REVERSE)
        elif ltRightReading <= threshold:
            driveMotors_motor_b.set_velocity(Kp*leftError,PERCENT)
            driveMotors_motor_b.spin(REVERSE)'''
    while True:
        rightError = threshold - ltRightReading
        leftError = threshold - ltLeftReading
        if ltLeftReading <= threshold:
            driveMotors_motor_b.set_velocity(((Kp*leftError)*motorSpeed)+motorSpeed,PERCENT)
            driveMotors_motor_a.set_velocity(((Kp*rightError)*motorSpeed)+motorSpeed,PERCENT)
        wait(.1,SECONDS)

'''
Description: Collects the current brightness level
# of Sensor: 1 (update to correct value)
Arg:
- None
Returns:
- None
'''
def light_readings():
    while True:
        global lightReading
        lightReading = lightSensor.brightness(PERCENT)
        wait(0.02,SECONDS)

'''
Description: Collects the current distance, object in view velocity, and object in view size
# of Sensor: 1 (update to correct value)
Arg:
- None
Returns:
- None
'''
def distance_readings():
    global distanceReading
    global objectVelocity
    global objectSize
    while True:
        distanceReading = distanceSensor.object_distance(INCHES)
        objectVelocity = distanceSensor.object_velocity()
        objectSize = distanceSensor.object_size()
        wait(.02,SECONDS)
'''
Description: Collects the current color value and if an April Tag is available
# of Sensor: 1 (update to correct value)
Arg:
- None
Returns:
- None
'''
def vision_readings():
    global BlueRingWidth
    global BlueRingHeight
    global BlueRingCenterX
    global BlueRingCenterY
    global BlueRingNumObjects
    global RedRingWidth
    global RedRingHeight
    global RedRingCenterX
    global RedRingCenterY
    global RedRingNumObjects
    BlueRingWidth = None
    BlueRingHeight = None
    BlueRingCenterX = None
    BlueRingCenterY = None
    BlueRingNumObjects = None
    RedRingWidth = None
    RedRingHeight = None
    RedRingCenterX = None
    RedRingCenterY = None
    RedRingNumObjects = None
    while True:
        wait(.02,SECONDS)
        BlueRingObjects = visionSensor.take_snapshot(visionSensor__BlueRing)
        RedRingObjects = visionSensor.take_snapshot(visionSensor__RedRing)
        if BlueRingObjects[0].exists:
            BlueRingNumObjects = len(BlueRingObjects)
            BlueRingWidth = BlueRingObjects[0].width
            BlueRingHeight = BlueRingObjects[0].height
            BlueRingCenterX = BlueRingObjects[0].centerX
            BlueRingCenterY = BlueRingObjects[0].centerY
        else:
            BlueRingWidth = None
            BlueRingHeight = None
            BlueRingCenterX = None
            BlueRingCenterY = None
            BlueRingNumObjects = None
        if RedRingObjects[0].exists:
            RedRingNumObjects = len(RedRingObjects)
            RedRingWidth = RedRingObjects[0].width
            RedRingHeight = RedRingObjects[0].height
            RedRingCenterX = RedRingObjects[0].centerX
            RedRingCenterY = RedRingObjects[0].centerY
        else:
            RedRingWidth = None
            RedRingHeight = None
            RedRingCenterX = None
            RedRingCenterY = None
            RedRingNumObjects = None
def change_ring_color():
    if BlueRingObjects[0].exists and RedRingObjects[0].exists:
        if RedRingWidth * _RingHeight > _RingWidth * _RingHeight:
            #
            pass
        else:
            pass
    elif BlueRingObjects[0].exists:
        pass
    else:
        pass
        
'''
Description: Collects the current reflection value
# of Sensor: 1 (update to correct value)
Arg:
- None
Returns:
- None
'''
def linetracker_readings():
    while True:
        global ltRightReading
        global ltMiddleReading
        global ltLeftReading
        ltRightReading = rightLineTracker.reflectivity(PERCENT)
        ltMiddleReading = middleLineTracker.reflectivity(PERCENT)
        ltLeftReading = leftLineTracker.reflectivity(PERCENT)

        wait(.2,SECONDS)

'''
Description: Opens/Closes the claw a set number of degrees
# of Sensor: 1
Arg:
- degrees (float): a number in degrees
Returns:
- None
'''
#def move_claw(degrees):


'''
Description: Moves the claw arm a set number of degrees up/down
# of Sensor: 1 (update to current value)
Arg:
- degrees (float): a number in degrees
Returns:
- None
'''
#def move_arm(degrees):


'''
Description: Collects the current degree value
# of Sensor: 1 (update to correct value)
Arg:
- None
Returns:
- None
'''
#def potentiometer_readings():


'''
Description: Collects the current hue reading. 
# of Sensors: 1 (update to correct value)
Arg:
- None
Returns: 
- None
'''
#def optical_readings():


'''
Description: Prints the values from desired sensors onto the EXP Brain Screen
Arg:
- None
Returns:
- None
'''
def display_data():
    brain.screen.set_font(FontType.PROP20)
    wait(0.05,SECONDS)
    while True:
        brain.screen.print("Num. Objects: ",BlueRingNumObjects)
        brain.screen.next_row()
        brain.screen.print("Object 1 Width: ",BlueRingWidth)
        brain.screen.next_row()
        brain.screen.print("Object 1 Height: ",BlueRingHeight)
        brain.screen.next_row()
        brain.screen.print("Object 1 CenterX: ",BlueRingCenterX)
        brain.screen.next_row()
        brain.screen.print("Object 1 CenterY: ",BlueRingCenterY)
        brain.screen.print("Num. Objects: ",RedRingNumObjects)
        brain.screen.next_row()
        brain.screen.print("Object 2 Width: ",RedRingWidth)
        brain.screen.next_row()
        brain.screen.print("Object 2 Height: ",RedRingHeight)
        brain.screen.next_row()
        brain.screen.print("Object 2 CenterX: ",RedRingCenterX)
        brain.screen.next_row()
        brain.screen.print("Object 2 CenterY: ",RedRingCenterY)
        '''brain.screen.print("Position:",driveMotors.position(DEGREES))
        brain.screen.next_row()
        brain.screen.print("Light:",lightReading)
        brain.screen.next_row()
        brain.screen.print("Distance:",distanceReading, "m")
        brain.screen.next_row()
        brain.screen.print("Velocity:",objectVelocity, "m/s")
        brain.screen.next_row()
        brain.screen.print("Object Size:",objectSize)
        wait(.75,SECONDS)
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)'''

#Thread Section 
#lightSensorThread = Thread(light_readings)
#lineTrackerThread = Thread(linetracker_readings)
visionSensorReadings = Thread(vision_readings)
#distanceSensorThread = Thread(distance_readings)
displayDataThread = Thread(display_data)
#SD Card File Setup for Writing Data

#Inertial Sensor Setup
brain_inertial.calibrate()
while brain_inertial.is_calibrating():
    wait(50,MSEC)
#Sub-Tasks (custom functions that handle scenarios. Ex: go_up_ramp())
while not brain.sdcard.is_inserted():
    brain.screen.set_cursor(1,1)
    brain.screen.print("Sd Card Missing")
    wait(5,MSEC)
    brain.screen.clear_screen()

#file = open("myRobot.csv","w")
#file.write("{},{}\n".format("Position","Light"))
#Main Program
countWalls = 0


while True:
   linear_inertial(45, 2.5)

   if distanceReading <= 2.5:
       countWalls +=1
      
       if countWalls == 1:
           wait(0.5,SECONDS)
           
           driveMotors.set_velocity(45, PERCENT)
           driveMotors.spin(REVERSE)
           driveMotors.stop()
           wait(0.25,SECONDS)
           inertial_turn(90)
           driveMotors.set_velocity(45, PERCENT)
           driveMotors.spin(FORWARD)
      
       elif countWalls == 2:
           wait(0.5, SECONDS)
           inertial_turn(180)
