def GuiPad(GuiPadiniFile:str = None):
    """GuiPad is a simple module for using your Gamepad on your desktop. \n
    Gamepad inputs are detected by pygame: https://www.pygame.org/docs/ref/joystick.html \n
    Actions on your PC are performed by pyautogui: https://pyautogui.readthedocs.io/en/latest/ \n

    Args:
        SettingsFile (str, optional): Path of a custom GuiPad.ini file. Construct with os.path.join("C://path","to","file.ini") for safety!
    """
##Dependencies
    import subprocess
    import sys
    import time
    import os
    import configparser
    config = configparser.ConfigParser()
#Non-core dependencies (with auto-installer backup! neat)
    def QuickInstallModule(ModuleName):
        print(f"{ModuleName} module not found, would you like to install? [Y/N]")
        if input()[:1].lower()==("y"):
            subprocess.run([sys.executable, "-m", "pip", "install", ModuleName], check=True) 
        else:
            raise ImportError(f"Please install {ModuleName} with >pip install {ModuleName}")
            
    try: #specifically to catch pygame errors from Raspberry Pi's where PiOs uses outdated pygame version 1.9.0!
        import pygame
    except ImportError:
        QuickInstallModule("pygame")
        import pygame
    if pygame.version.ver[:2] == "1.":
        print("Pygame module must be at least Version 2.0.0, can Python upgrade pygame? [Y/N]")
        if input()[:1].lower()==("y"):
            try:
                import pip
                pip.main(['install', '--upgrade', "pygame"])
            except ImportError:
                raise ImportError('Pygame has failed to upgrade. Please "pip install pygame -U" in your OS terminal.')
            finally:
                raise ImportError('Please restart GuiPad.')
        else:
            raise ImportError('Pygame must be at least Version 2.0.0! Please "pip install pygame -U" in your OS terminal.')
    try:
        import pyautogui
    except ImportError:
        QuickInstallModule("pyautogui")
        import pyautogui

##Variables
    #pygame
    pyautogui.PAUSE = 0.01
    ButtonDelayTime = 0.2
    #Initialise    
    pyautogui.FAILSAFE = False  #uh oh :^)
    PrintDebugInfo = False      #very messy
    pygame.init()
    GuiPadLeftMouseIsDown = [False] # this is a dumb hack instead of using a global variable - you WILL lose IQ if you read this

    #Config
    MouseSensitivity = int(60)/10
    ScrollSpeed = int(100)
    BonusSpeed = int(240)/100
    SlowMultiplier = int(25)/10
    DeadzoneL = int(40)/1000
    DeadzoneR = int(450)/1000
    FPSTime = int(1600)/1000000  #60 FPS by default
    Axis2IsLeftTrigger = "Auto"   #Autoconfigure
    AutoAxis2Clock = [100]
    AutoAxis2Counter = [0]
    AutoAxis2SwapThreshold = 15

    if not GuiPadiniFile is None:
        if GuiPadiniFile == "cwd":
            GuiPadiniFile= os.path.join(os.getcwd(),"GuiPad.ini")
        if os.path.exists(GuiPadiniFile):
            config.read(GuiPadiniFile)
            MouseSensitivity = int(config["Settings"]["MouseSensitivity"])/10
            ScrollSpeed = int(config["Settings"]["ScrollSpeed"])
            BonusSpeed = int(config["Settings"]["BonusSpeed"])/100
            SlowMultiplier = int(config["Settings"]["SlowMultiplier"])/10
            DeadzoneL = int(config["Settings"]["DeadzoneL"])/1000
            DeadzoneR = int(config["Settings"]["DeadzoneR"])/1000
            FPSTime = int(config["Settings"]["FPSTime"])/1000000
            Axis2IsLeftTrigger = config["Settings"]["Axis2IsLeftTrigger"]
            if Axis2IsLeftTrigger.lower().strip() == "true":
                Axis2IsLeftTrigger = True
            elif Axis2IsLeftTrigger.lower().strip() == "false":
                Axis2IsLeftTrigger = False
            else:
                Axis2IsLeftTrigger = "Auto"
                AutoAxis2Clock[0] = 30
                AutoAxis2Counter = [0]
            print("GuiPad.ini loaded!")
        else:
            print("GuiPad.ini not found, using default setting values.")

    if Axis2IsLeftTrigger == True:
        RStickXIndex = [3]
        RStickYIndex = [4]
        LTriggerIndex = [2]
    else:
        #default
        RStickXIndex = [2]
        RStickYIndex = [3]
        LTriggerIndex = [4]

##Button bindings
    def pressB0(): #Cross button
        if not GuiPadLeftMouseIsDown[0]:
            pyautogui.mouseDown()
            GuiPadLeftMouseIsDown[0] = True
    def pressB1(): #Circle button
        pyautogui.rightClick()
    def pressB2(): #Square button
        pyautogui.doubleClick()
    def pressB3(): #Triangle button
        #webbrowser.open(HelpHTML,new=2)
        pyautogui.middleClick()
    def pressB4(): #Left Trigger
        pyautogui.hotkey('ctrl', 'shift', 'tab')
    def pressB5(): #Right Trigger
        pyautogui.hotkey('ctrl', 'tab')
    def pressB6(): #Select button
        pyautogui.hotkey('ctrl', 'c')
    def pressB7(): #Start button
        pyautogui.hotkey('ctrl', 'v')
    def pressB8(): #Left Sitck button
        pyautogui.hotkey('alt', 'left')    
    def pressB9(): #Right Stick button
        pyautogui.hotkey('alt', 'right')    
    ListOfButtonFunctions = [pressB0,pressB1,pressB2,pressB3,pressB4,pressB5,pressB6,pressB7,pressB8,pressB9]

## Input handling
    def HandleControllerButtons(joystick, ButtonID, Pressed, ButtonDelay): #"joystick" argument only included for consistency
        if Pressed == 1 and ButtonDelay < 0 and not len(ListOfButtonFunctions)>ButtonID:
            ListOfButtonFunctions[ButtonID]()
            #print(ButtonID) #, Pressed)
            return ButtonDelayTime
        elif Pressed ==0 and ButtonID == 0 and GuiPadLeftMouseIsDown[0]:
            pyautogui.mouseUp()
            GuiPadLeftMouseIsDown[0] = False
        return ButtonDelay
    
    def HandleDPad(joystick, hats, ButtonDelay):
        for i in range(hats):
                if ButtonDelay < 0:
                    hat = joystick.get_hat(i)
                    if hat[0] == -1:
                        #left
                        pyautogui.hotkey('ctrl', 'w')
                        return ButtonDelayTime
                    elif hat[0] == 1:
                        #right
                        pyautogui.hotkey('ctrl', 't')
                        return ButtonDelayTime
                    if hat[1]== -1:
                        #down
                        pyautogui.hotkey('ctrl', '-')
                        return ButtonDelayTime
                    elif hat[1]== 1:
                        #up
                        pyautogui.hotkey('ctrl', '+')
                        return ButtonDelayTime
        return ButtonDelay
    
    def HandleControllerSticks(joystick, axes, ButtonDelay):
        if AutoAxis2Clock[0] > 0:
            AutoAxis2Clock[0]-=1
            if AutoAxis2Counter[0] > AutoAxis2SwapThreshold:
                print("Right stick is stuck down!? Swapping axis mode.")
                print("If you see this a lot try MakeGuiPadini() and setting: Axis2IsLeftTrigger = true then passing the path to the ini file through GuiPad(here)")
                #we've detected a problem! try flipping it
                RStickXIndex[0] = 3
                RStickYIndex[0] = 4
                LTriggerIndex[0] = 2
                AutoAxis2Clock[0] = 0

        CanScrollSideways = True
        try:
            if joystick.get_axis(3):
                if abs(float(f"{joystick.get_axis(RStickYIndex[0]):>6.3f}")) > 0.3:       #is this causing crash?
                    CanScrollSideways = False
        finally:
            XToMoveMouse = 0
        TriggerStates=[joystick.get_axis(LTriggerIndex[0]),joystick.get_axis(5)]

        for i in range(axes):
            Stick = i 
            axis = joystick.get_axis(i)
            Dir = float(f"{axis:>6.3f}")
            if PrintDebugInfo:
                print(f"Axis {i} value: {axis:>6.3f}")
            if abs(Dir) > DeadzoneL or abs(XToMoveMouse) > DeadzoneL:
                if Stick == 0:
                    XToMoveMouse = Dir
                
                if Stick == 1:
                    SlowerSpeed = 1/(((round(TriggerStates[1], 2)+1)*SlowMultiplier)+1)
                    XMoveFinal = XToMoveMouse*abs(XToMoveMouse)
                    YMoveFinal = Dir*abs(Dir)
                    if abs(XToMoveMouse) > 0.99 :
                        XMoveFinal = XToMoveMouse*BonusSpeed
                    if abs(Dir) > 0.99:
                        YMoveFinal = Dir*BonusSpeed
                    pyautogui.move(MouseSensitivity*XMoveFinal*(SlowerSpeed+0.1), MouseSensitivity*YMoveFinal*(SlowerSpeed+0.1))            
                    XToMoveMouse = 0
                
                elif Stick == RStickXIndex[0] and ButtonDelay<=0 and CanScrollSideways:
                    if Dir > DeadzoneR :
                        pyautogui.press("right")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                    elif Dir < -DeadzoneR:
                        pyautogui.press("left")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                
                elif Stick == RStickYIndex[0] and ButtonDelay<=0:
                    if Dir > DeadzoneR :
                        pyautogui.press("down")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                        print(AutoAxis2Clock[0])
                        if AutoAxis2Clock[0] > 0:
                            AutoAxis2Counter[0]+=1
                            print(AutoAxis2Counter)

                    elif Dir < -DeadzoneR:
                        pyautogui.press("up")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                if PrintDebugInfo:
                    print(Stick, Dir)
        return ButtonDelay
##Core script
    joysticks = {}
    ButtonDelay = 0.1
    while True: #oh boy here we go!
        time.sleep(FPSTime)
        if ButtonDelay > 0:
            ButtonDelay-=FPSTime
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                if PrintDebugInfo:
                    print(f"Joystick {joy.get_instance_id()} connencted")
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                if PrintDebugInfo:
                    print(f"Joystick {event.instance_id} disconnected")
#Detect inputs:         
        for joystick in joysticks.values():
            axes = joystick.get_numaxes()
            buttons = joystick.get_numbuttons()
            hats = joystick.get_numhats()

            if PrintDebugInfo:
                print(f"Joystick {joystick.get_instance_id()}")
                print(f"Joystick name: {joystick.get_name()}")
                print(f"GUID: {joystick.get_guid()}")
                print(f"Joystick's power level: {joystick.get_power_level()}")
                print(f"Number of axes: {axes}")
                print(f"Number of hats: {hats}")
                print(f"Number of buttons: {buttons}")

            ButtonDelay = HandleControllerSticks(joystick, axes, ButtonDelay)
            for i in range(buttons):
                button = joystick.get_button(i)
                ButtonID = int(f"{i:>2}")
                ButtonDelay = HandleControllerButtons(joystick, ButtonID, button, ButtonDelay)
                if PrintDebugInfo:
                    print(f"Button {i:>2} value: {button}")
            ButtonDelay = HandleDPad(joystick, hats, ButtonDelay)

def MakeGuiPadini(Directory:str=None,Name:str="GuiPad.ini"):
    """Makes a GuiPad.ini file to be provided in RunGuiPad(ini_path)

    Args:
        Directory (str, optional): Directory where the ini file will be generated. Defaults to current work directory. Construct with os.path.join("C://path","to","file.ini") for safety!
        Name (str, optional): Name of the GuiPad.ini file. Defaults to "GuiPad.ini".
    """
    if Directory is None:
        import os
        Directory = os.getcwd() #just dump it in their cwd

    with open(os.path.join(Directory,Name), 'w') as ini:
        ini.writelines([
            "[Settings] \n",
            "#ONLY INTEGERS ARE ACCEPTED! \n",
            "MouseSensitivity = 60 \n",
            "ScrollSpeed = 100 \n",
            "BonusSpeed = 240 \n",
            "SlowMultiplier = 25 \n",
            "#Deadzones are /10 where 100 is 100% \n",
            "DeadzoneL = 40 \n",
            "DeadzoneR = 450 \n",
            "#FPSTime is /1000000, so 1600 is 60FPS \n",
            "FPSTime = 1600 \n",
            '#Some gamepads make Axis 3 Right Trigger instead of Right Stick X. If you have problems, try setting Axis2IsLeftTrigger to "True" or "False": \n'
            "Axis2IsLeftTrigger = Auto"
        ])
    print(f"GuiPad.ini file written to {os.path.join(Directory,Name)}")

if __name__ == "__main__":
    GuiPad("cwd")
