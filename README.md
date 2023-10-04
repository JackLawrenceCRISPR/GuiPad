<h1 align="center">GuiPad</h1>
<p align="center">
  <picture>
    <source srcset="./GuiPad_Icon.ico"> 
    <img src="./GuiPad_Icon.ico">
  </picture>
</p>
<h3 align="center">Use your gamepad as a mouse with pygame and PyAutoGUI.</h3>


## Installation
**Make sure that pygame is at least version 2.0**  
*Download GuiPad.py and run it with python.*  
**OR**  
Use ```pip install GuiPad``` in your Operating System terminal, then in a python terminal or script:  
```python
import GuiPad
GuiPad.GuiPad()
```
https://pypi.org/project/GuiPad/

## Configuration
A settings.ini file can be used in Guipad.Guipad("PathToSettings.ini") for additional customisation.  
Generate a standard settings file using:
```python
import os
import GuiPad
Make_In_Directory = os.path.join("C:\\Users","JackLawrenceCRISPR","Desktop","Folder") #put your own deployment directory!
MakeGuiPadini(Make_In_Directory, "GuiPad.ini")  #you can also choose a custom name
```
Edit the .ini file to your preference then provide  
_Path = os.path.join("C:\\Users","JackLawrenceCRISPR","Desktop","Folder","GuiPad.ini")_ in your _GuiPad.GuiPad(Path)_

## Controls
| Input | Output | Effect |
| :---         |     :---:      |          --- |
| Left joystick | Mouse | Move cursor  |
| Right trigger | Slow Mouse | Slow movment  |
| Right joystick | Arrow Keys | Page Scrolling / Time & Sound (videos)|
| A Button | Left click | Normal click |
| B Button | Right click | Right click|
| X Button | Double click | Open file / select a word in text  |
| Y Button | Middle click | Open link in new tab|
| D-Pad up | Ctrl + + | Zoom in |
| D-Pad down | Ctrl + - | Zoom out |
| D-Pad right | Ctrl + T | New tab |
| D-Pad left | Ctrl + W | Close window |
| Left shoulder | Ctrl + Shift + Tab | Next tab  |
| Right shoulder | Ctrl + Tab | Previous tab  |
| Left stick | Alt + Left | Go back  |
| Right stick | Alt + Right | Go forward |
| Select button | Ctrl + C | Copy |
| Start button | Ctrl + V | Paste |

**Do not hold the right stick down on startup.**  
It's used in a neat hack to automatically detect your controller type.
