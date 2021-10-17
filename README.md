# WELCOME TO AUTOMATOR BETA 

### This program is able to create automations on your system.
### WARNING: this program is only an experimantal release; infact it works very well on Windows wether in linux did not works always correctly

### Aviable languages:
  * Italian
  * English

### Tested with these systems: 
  * windows10 (build 19043.1237)
  * ubuntu 20.04.03
  * raspbian 10 

# Updates

  - Added file <code>Automator_Toolchain.exe</code>.  
   
# Installation
 - # Prerequisites

   - Python 3.6 =< =>3.9 (CURRENT NOT SUPPORTED PYHON 3.10), pip pakage manager 
   - Linux or Windows system

 - ## Installation

   ### For all systems:
   
    - Download <code>Automator_Toolchain.exe</code>.

    - Open the terminal on the same directory and by typing <code>Automator_Toolchain.exe --install</code> it will install the main program.

   ### On linux:
   
    - You can copy this repositry by the following command:
 
      <code>$ git clone "https://github.com/Davide255/Automator"</code>
     
      Now run the following pip command to install the requirements:
     
      <code>pip install -r requirements_linux.txt</code>
     
    - You can also download and unzip the repository, so follow the above steps.

   ### On Windows:
    
    - Downolad and extract this pakage.
     
    - Install the pakage dipendency by pip: 
     
      <code>pip install -r requirements_win32.txt</code>

    - If you have installed Visual Studio or VSCode you can copy this repository
      and follow the above steps.
      

   ### MacOs X:

    - Ufficially we _**DID NOT TESTED ON MACOS X**_; there are some features
      that required bash or powershell script that (we think) probably doesn't work

# How does it works?

The main programm create a Thread that observe your system and it does actions consequentially.

# Possible errors:

- [CRITICAL] [Cutbuffer ] Unable to find any valuable Cutbuffer provider. (Appared on Ubuntu 20.04.03)
    
  **Fix by installing xclip and xsel (<code>$ sudo apt-get install xclip xsel</code>)**

