import os

GamepadMaps = {
    'ljoycon': [[1, 0], [0, 1, 2, 3, 4, 5, False, False, 6, False, 8, False, False, 7, 9, 10]], 
    'rjoycon': [[1, 0], [0, 1, 2, 3, 4, 5, False, False, False, 6, False, 8, 7, False, 9, 10]], 
    'switchpro': [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 6, 10, 7, 8, 9, 4, 5, False, False, False, False, 11], [0, 1, 2, 3]],  #12,13,14,15
    'xbox_windows': [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 0]], 
    'xbox': [[0, 1, 4, 2, 3, 5], [0, 1, 2, 3, 4, 5, 6, 7, 10, 8, 9], [1, 0]], 
    'ps4': [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 6, 7, 10, 8, 9, 4, 5, False, False, False, False, 11], [3, 2, 0, 1]], 
    'ps5': [[0, 1, 4, 2, 3, 5], [0, 1, 2, 3, 4, 5, False, False, 6, 7, 10, 8, 9], [1, 0]], 
    'xbox_pygame1x': [[0, 1, 5, 3, 2], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 0]], 
    'ps4_pygame1x': [[0, 1, 2, 3, 5, 4], [0, 1, 2, 3, 4, 5, False, False, 6, 7, 8, 9, 10, 11], [1, 0]]
}

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
    RebindButtons = False

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
            RebindButtons = config["Settings"]["RebindButtons"]
            print("GuiPad.ini loaded!")
        else:
            print("GuiPad.ini not found, using default setting values.")

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
    def pressB10(): #Undefined
        pyautogui.press('enter')
    def pressB11(): #Undefined
        print("Button pressed!")
    def pressB12(): #Undefined
        print("Button pressed!")
    def pressB13(): #Undefined
        print("Button pressed!")
    def pressB14(): #Undefined
        print("Button pressed!")
    def pressB15(): #Undefined
        print("Button pressed!")

    ListOfButtonFunctions = [pressB0,pressB1,pressB2,pressB3,pressB4,pressB5,pressB6,pressB7,pressB8,pressB9,pressB10,pressB11,pressB12,pressB13,pressB14,pressB15]

    try:
        if RebindButtons != "false" and RebindButtons != "False" and not RebindButtons is None:
            ListOfButtonFunctions = []
            print("Rebinding buttons.")
            while RebindButtons.find("|") > -1:
                ListOfButtonFunctions.append(locals()["press"+RebindButtons[:RebindButtons.find("|")]])
                RebindButtons = RebindButtons[RebindButtons.find("|")+1:]
    except:
        ListOfButtonFunctions = [pressB0,pressB1,pressB2,pressB3,pressB4,pressB5,pressB6,pressB7,pressB8,pressB9]



## Input handling
    def HandleControllerButtons(joystick, joystickMAP, ButtonID, Pressed, ButtonDelay): #"joystick" argument only included for consistency
        ButtonID = joystickMAP[ButtonID]
        if Pressed == 1 and ButtonDelay < 0 and len(ListOfButtonFunctions)>ButtonID: #should be one bigger (since it starts from zero)
            ListOfButtonFunctions[ButtonID]()
            #print(ButtonID) #, Pressed)
            return ButtonDelayTime
        elif Pressed ==0 and ButtonID == 0 and GuiPadLeftMouseIsDown[0]:
            pyautogui.mouseUp()
            GuiPadLeftMouseIsDown[0] = False
        return ButtonDelay
    
    def HandleDPad(joystick, joystickMAP, hats, ButtonDelay):
        for i in range(hats):
                if ButtonDelay < 0:
                                                                                                            #WRITE CODE IN HERE TO HAND THE SWTICH BUTTON HATS
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
    
    def HandleControllerSticks(joystick, joystickMAP, axes, ButtonDelay):

        CanScrollSideways = True
        try:
            if joystick.get_axis( joystickMAP[3] ):
                if abs(float(f"{joystick.get_axis( joystickMAP[3] ):>6.3f}")) > 0.3:       #is this causing crash?
                    CanScrollSideways = False
        finally:
            XToMoveMouse = 0
        TriggerStates=[joystick.get_axis( joystickMAP[4] ),joystick.get_axis( joystickMAP[5] )]

        for i in range(axes):
            Stick = joystickMAP[i] 
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
                
                elif Stick == 2 and ButtonDelay<=0 and CanScrollSideways:
                    if Dir > DeadzoneR :
                        pyautogui.press("right")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                    elif Dir < -DeadzoneR:
                        pyautogui.press("left")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                
                elif Stick == 3 and ButtonDelay<=0:
                    if Dir > DeadzoneR :
                        pyautogui.press("down")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100

                    elif Dir < -DeadzoneR:
                        pyautogui.press("up")
                        ButtonDelay = (1-abs(Dir))*0.25*ScrollSpeed/100
                if PrintDebugInfo:
                    print(Stick, Dir)
        return ButtonDelay

#Gamepad Mapping
    def GetGamepadMapIDFromName(UserGamepadName,UserGamepadInputCounts):
        originalwd = os.getcwd()
        os.chdir( os.path.dirname(os.path.realpath(__file__)) )
        RawGamepadMappingSettings = []
        if os.path.exists(os.path.join(os.getcwd(),"GamepadMappings.py")):
            with open("GamepadMappings.py", "r") as gamepadmappingfile:
                for line in gamepadmappingfile:
                    RawGamepadMappingSettings.append(line.strip())
        os.chdir(originalwd)
        originalwd = None

        for l in RawGamepadMappingSettings:
            if "!!!@" in l:
                LineGamepadName = l[:l.find("!!!@")].strip() 
                if UserGamepadName.strip()  == LineGamepadName:
                    return l[l.find("!!!@")+4:].strip()

        print("Gamepad map not defined, automatically predicting appropriate map...")

        UserGamepadName = UserGamepadName.lower()
        ##Guess gamepad map by name of the gamepad...
        import platform
        if any([ x in UserGamepadName for x in ["xbox","microsoft","horipad"] ]):
            if "window" in platform.system().lower():
                return "xbox_windows" #it probably uses DirectInput instead of XInput?
            return "xbox"
        if any([ x in UserGamepadName for x in ["ps5","dualshock5","dualshock 5","playstation 5","playstation5"] ]):
            return "ps5"
        if any([ x in UserGamepadName for x in ["ps4","ps3","ps2","dualshock","playstation","sony"] ]):
            return "ps4"
        
        if "joycon" in UserGamepadName:
            if "left" in UserGamepadName:
                return "ljoycon"
            else:
                return "rjoycon"
        if "switch" in UserGamepadName and "pro" in UserGamepadName:
            return "switchpro"

        #we didn't find any keywords in the gamepad name!
        #now guess gamepad map by number of axes/buttons/hats on the gamepad...

        axs = UserGamepadInputCounts[0]
        but = UserGamepadInputCounts[1]
        hat = UserGamepadInputCounts[2]

        if but == 10:
            if "dual" in UserGamepadName or "shock" in UserGamepadName:
                return "ps5"
            return "xbox"
        if axs==2 and but==15:
            if "left" in UserGamepadName:
                return "ljoycon" 
            return "rjoycon"
        if hat==4:
            if "dual" in UserGamepadName or "shock" in UserGamepadName:
                return "ps4"
            return "switchpro"
        if but==13:
            return 'ps4_pygame1x'
        
        #we didn't detect anything! -- it's probably xbox?
        if "window" in platform.system().lower():
            return "xbox_windows" #it probably uses DirectInput instead of XInput?
        return "xbox" #unix systems are fine


    joysticks = {}
    ButtonDelay = 0.1


##Core script
    while True: #oh boy here we go!
        time.sleep(FPSTime)
        if ButtonDelay > 0:
            ButtonDelay-=FPSTime
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joydata = [joy.get_name(), [joy.get_numaxes(), joy.get_numbuttons(), joy.get_numhats()]]
                GamepadMapID = GetGamepadMapIDFromName(joydata[0],joydata[1])
                joysticks[joy.get_instance_id()] = [ joy,GamepadMaps[GamepadMapID]]
                #if PrintDebugInfo:
                print(f"Joystick {joy.get_instance_id()} is has the Name:")
                print(f"{joy.get_name()}") 
                print(f"...and connencted as map type: {GamepadMapID}")
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                #if PrintDebugInfo:
                print(f"Joystick {event.instance_id} disconnected")
#Detect inputs:         
        for joystickdata in joysticks.values():
            joystick = joystickdata[0]
            joystickMAP = joystickdata[1] #[ axisref, buttonref, hatref]        #if hatref = 4 then they are buttons, if hatref=2 then it is a right[-1,0,1],up[-1,0,1]

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

            ButtonDelay = HandleControllerSticks(joystick, joystickMAP[0], axes, ButtonDelay)
            for i in range(buttons):
                button = joystick.get_button(i)
                ButtonID = int(f"{i:>2}")
                ButtonDelay = HandleControllerButtons(joystick, joystickMAP[1], ButtonID, button, ButtonDelay)
                if PrintDebugInfo:
                    print(f"Button {joystickMAP[1][ButtonID]} value: {button}")

            #handledpad is different for switch type!
            ButtonDelay = HandleDPad(joystick, joystickMAP[2], hats, ButtonDelay)

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
            
            '#Rebind your controls: \n'
            "RebindButtons = B1|B2|B3|B4|B5|B6|B7|B8|B9|None|None|None|None|None|None|\n"
        ])
    print(f"GuiPad.ini file written to {os.path.join(Directory,Name)}")

def MapGamepad(GamepadName=False,MapType=False):
    """Manually set the button map for your controller type, GuiPad will remember the name of your controller type
    GuiPad tries to predict your controller's button map based on https://www.pygame.org/docs/ref/joystick.html
    If GuiPad is incorrectly mapping your controller, use this function to manually set the map.

    1. Run GuiPad() and get the full exact Name of the gamepad
    2. Run MapGamepad function with no inputs, and get a list of controller MapTypes
    3. Run MapGamepad(Name, MapType) 

    Args: 
        GamepadName (str): Name of your gamepad. Leave empty for help. 
        MapType(str): Name of your Map. Leave empty to delete an entry (assuming it exists).

    Output: Sets your gamepad's MapType
    """

    GamepadMapName = MapType
    if not GamepadName:
        GamepadMapName="Help for gamepad mapping." 
    if GamepadMapName and not GamepadMapName in GamepadMaps.keys():
        print("The first variable should be a gamepad Name, the second variable is a MapType (or false to delete mapping for named gamepad)") 
        print("Get gamepad Name from running Guipad (they will be printed)")
        print("Gamepad MapType is not recognised, please select one from:")
        for m in GamepadMaps.keys():
            print(m)
        print("Rerun this function with as MapGamepad(GamepadName, MapType)")

    elif GamepadName:
        originalwd = os.getcwd()
        os.chdir( os.path.dirname(os.path.realpath(__file__)) )
        if not os.path.exists(os.path.join(os.getcwd(),"GamepadMappings.py")):
            open("GamepadMappings.py", "w").close() #create new empty file if one doesnt' exist

        NewFileContents = ['"""\n']
        with open("GamepadMappings.py","r") as gamepadmappingfile:
            AlreadySetNewValue = False
            for line in gamepadmappingfile:
                NewLine = line
                if "!!!@" in line:
                    if line.find(GamepadName.strip()+"!!!@") == 0:  #replace only if we exactly match the name
                        NewLine = "_remove"
                        if GamepadMapName and not AlreadySetNewValue:
                            NewLine = f"{GamepadName.strip()}!!!@{GamepadMapName}\n"#rewrite line
                        AlreadySetNewValue = True
                    if NewLine != "_remove":
                        NewFileContents.append(NewLine)
            if GamepadMapName and not AlreadySetNewValue:
                print("NewLine")
                NewFileContents.append(f"{GamepadName.strip()}!!!@{GamepadMapName}\n") #create a new line if we aren't replacing an old one

        with open("GamepadMappings.py","w") as gamepadmappingfile:
            NewFileContents.append('\n"""')
            gamepadmappingfile.writelines(NewFileContents)

        os.chdir(originalwd)
        print("New gamepad mapping Set.")


def CreateShortcut():
    import platform
    if "window" in platform.system().lower():
        print("Windows OS detected, creating shortcut...")

    #Make Batch file to run GuiPad...
        import sys
        PythonExePath = sys.executable
        #note - "{PythonExePath}" can be "python" if PYTHONPATH is available on windows
        originalwd = os.getcwd()
        os.chdir( os.path.dirname(os.path.realpath(__file__)) )
        with open("GuiPad.bat","w") as gamepadmappingfile:
            gamepadmappingfile.writeline(f"""echo off & {PythonExePath} -x "%~f0" %* & goto :eof \nimport GuiPad;\nGuiPad.GuiPad()""")
        BatchFile = os.path.join(os.getcwd(),"GuiPad.bat")

        try:
            print("Attempting to get icon")
            import urllib.request
            urllib.request.urlretrieve("https://raw.githubusercontent.com/JackLawrenceCRISPR/GuiPad/main/Icons/GuiPad_Icon.ico", "GuiPad_Logo.ico")
        except:
            print("Failed to get icon...")
            print('You can download an icon for your shortcut at: https://github.com/JackLawrenceCRISPR/GuiPad/blob/main/Icons/GuiPad_Icon.ico"')
        os.chdir(originalwd)

    #python -m pip install pywin32
        MakeStandardShortcut = True
        try:
            from win32com.client import Dispatch
        except ImportError:
            print("WindowsAPI (pywin32) module not found.")
            print("GuiPad can help you quickly make your own shortcut")
            print("OR it can be automatically generated if you let GuiPad install pywin32")
            print("if you would like to install pywin32 type 'y' type 'n' for guidance")
            if input()[:1].lower()==("y"):
                import subprocess
                subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], check=True) 
                from win32com.client import Dispatch
            else:
                MakeStandardShortcut = False
                print(f"Right click any file and find 'send to' -> 'desktop (shortcut)'")
                print(f"Now right click the shortcut you just made on your desktop and go to 'properties'")
                print('Finally set "Target" to: "{BatchFile}"')
                print("Press enter several times to close this terminal when you are done...")
                print(f"If the icon downloaded successfully it is on your pc already at {os.path.join(os.path.dirname(BatchFile), 'GuiPad_Logo.ico')}")
                print("if the icon failed to dnwload see above to find where you can download one.")
                input()
                input()
                

    #Make Shortcut to batch file...
        if MakeStandardShortcut:
            #create windows shortcut from: https://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create-shortcuts/
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') )
            shortcut.Targetpath = BatchFile
            shortcut.WorkingDirectory = os.path.dirname(BatchFile)
            if os.path.join(os.path.dirname(BatchFile), "GuiPad_Logo.ico"):
                shortcut.IconLocation = os.path.join(os.path.dirname(BatchFile), "GuiPad_Logo.ico")
            shortcut.save()
        print("A shortcut has been generated on your Desktop.")
        input()
    else:
        print("Unix system detected, creating desktop python file...")
        os.chdir(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') ) #Linux Desktop
        with open("Launch_GuiPad.py","w") as gamepadmappingfile:
            gamepadmappingfile.writeline(f"import GuiPad;\nGuiPad.GuiPad()")
        print("Go to your menu editor (in preferences) and add 'New Item'")
        print("" )
        print("Modify the targ" )

        print("Download an icon at https://github.com/JackLawrenceCRISPR/GuiPad/blob/main/Icons/GuiPad_Logo.svg'")


if __name__ == "__main__":
    GuiPad("cwd")
