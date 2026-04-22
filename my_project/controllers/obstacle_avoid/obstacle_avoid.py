from controller import Robot

TIME_STEP = 32
MAX_SPEED = 6.0
RED_THRESHOLD = 0.9

robot = Robot()

# motor wheels and numbering
wheel1 = robot.getDevice("wheel1")
wheel2 = robot.getDevice("wheel2")
wheel3 = robot.getDevice("wheel3")
wheel4 = robot.getDevice("wheel4")

wheels = [wheel1, wheel2, wheel3, wheel4]
for w in wheels:
    w.setPosition(float('inf'))
    w.setVelocity(0.0)

# cam for rumba
camera = robot.getDevice("CAM")
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

while robot.step(TIME_STEP) != -1:

    objects = camera.getRecognitionObjects()
    obstacle_detected = False
    turn_direction = 0

    for obj in objects:
        colors = obj.getColors()
        r, g, b = colors[0], colors[1], colors[2]

        if r > RED_THRESHOLD and g < 0.1 and b < 0.1:
            obstacle_detected = True
            x, y, z = obj.getPosition()
            turn_direction = -1 if x < 0 else 1
            break

    if obstacle_detected:
        print("Roomba detected an obstacle changing directions")
        if turn_direction == -1:
            # Turn left
            wheel1.setVelocity(-MAX_SPEED/2)
            wheel2.setVelocity(MAX_SPEED/2)
            wheel3.setVelocity(-MAX_SPEED/2)
            wheel4.setVelocity(MAX_SPEED/2)
        else:
            # Turn right
            wheel1.setVelocity(MAX_SPEED/2)
            wheel2.setVelocity(-MAX_SPEED/2)
            wheel3.setVelocity(MAX_SPEED/2)
            wheel4.setVelocity(-MAX_SPEED/2)
    else:
        # Move forward
        for w in wheels:
            w.setVelocity(MAX_SPEED)