from GUI import *

# FRAMES in Tk lets you organise and group widgets. It works like a container in which widgets can be placed.
# WIDGETS are the little components or controls of the Graphical User Interface (GUI) such as buttons, labels, scrollbars, radio buttons, and text boxes used in a GUI application.


# systemPower() toggles all children state (Enabled/Disabled) to be interacted
def systemGUI(frame, toggle):
    global powerOn
    if toggle.get() == 1:
        powerOn = True
        toggleAllChildren(frame, True)
    elif toggle.get() == 0:
        powerOn = False
        toggleAllChildren(frame, False)
        
        
# systemShutdown() closes GUI window
def systemShutdown(root):
    print("System Shutting Down")
    root.quit()
    root.destroy()


# keyPress() changes the widget state to selected (highlight) when pressed
def keyPress(widget, pressed):
    # If the button is disabled don't do anything
    if widget.instate(['disabled']):
        return

    # If pressed set state to selected
    if pressed and widget.instate(['!selected']):
        widget.state(['selected'])
        widget.invoke()
    elif not pressed and widget.instate(['selected']):
        widget.state(['!selected'])


# toggleAllChildren() toggles all children state (Enabled/Disabled)
def toggleAllChildren(frame, toggle):
    # hasattr('winfo_children') check if the attribute is defined
    # len(frame.winfo_children()) checks for any children from the parent frame
    if not hasattr(frame, 'winfo_children') or len(frame.winfo_children()) == 0:
        # Check if the frame should be toggled.
        if shouldToggle(frame):
            # Toggle the frame using state attribute
            if toggle:
                frame.state(['!disabled'])
            else:
                frame.state(['disabled'])
    else:
        for frame in frame.winfo_children():
            # Continue toggling parent frame children
            toggleAllChildren(frame, toggle)


# ShouldToggle() forces the frame to be in Enabled state 
def shouldToggle(frame):
    # Check if the item should be toggled (Default = True)
    shouldToggle = True

    # hasattr('shouldToggle') check if the attribute is defined
    # shouldToggle() will override all other overrides (You can put other overrides here)
    if hasattr(frame, 'shouldToggle'):
        shouldToggle = frame.shouldToggle

    if shouldToggle:
        return True
    else:
        return False


print('Imported LiveButtons.py')
