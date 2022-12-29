monitorOn = False
controlCloseLoop = False


def switchODrive(frame, toggle):
    global monitorOn
    if toggle.get() == 1:
        monitorOn = True
    elif toggle.get() == 0:
        monitorOn = False
        
        
def switchControlLoop(toggle):
    global controlCloseLoop
    if toggle.get() == 1:
        controlCloseLoop = True
        print('Mode: Close Loop')
    elif toggle.get() == 0:
        controlCloseLoop = False
        print('Mode: Open Loop')


def movementControls(input):
    # Speed Control Input
    if input == 'up':
        print('Speed Up')
    if input == 'down':
        print('Speed Down')
        
    # Steering Control Input
    if input == 'left':
        print('Steer Left')
    if input == 'right':
        print('Steer Right')
    
    # Brake Control Input
    if input == 'brake':
        print('Braking...')
        
        
def calibrateControls(input):
    # Calibrate Motor Input
    if input == 'M1':
        print('Calibrating M1')
    if input == 'M2':
        print('Calibrating M2')
    if input == 'Both':
        print('Calibrating Both')

    # Calibrate ODrive Input
    if input == 'ODrive':
        print('Calibrating Odrive')
    
    # Calibrate Steering Input
    if input == 'steering':
        print('Calibrating Steering')


def stopODrive():
    print('Stop Odrive')
    
print('Imported LiveDashboard.py')
