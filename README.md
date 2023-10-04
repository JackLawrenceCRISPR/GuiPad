# GuiPad
A simple module to use your gamepad as a mouse with pygame and PyAutoGUI.

# Installation
*Download GuiPad.py and run it with python.*

**OR**

Use ```pip install GuiPad``` in your Operating System terminal, then in a python terminal or script:  
```python
import GuiPad
GuiPad.GuiPad()
```

# Configuration
A csettings.ini file can be used in Guipad.Guipad("PathToSettings.ini") for additional customisation.

Generate a standard settings file using:
```python
import os
import GuiPad
Make_In_Directory = os.path.join("C:\\Users","JackLawrenceCRISPR","Desktop","Folder") #put your own deployment directory!
MakeGuiPadini(Make_In_Directory, "GuiPad.ini")  #you can also choose a custom name
```
Edit the .ini file to your preference then provide the _Path = os.path.join("C:\\Users","JackLawrenceCRISPR","Desktop","Folder","GuiPad.ini")_ in your _GuiPad.GuiPad(Path)_
