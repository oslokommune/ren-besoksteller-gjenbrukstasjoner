
# How to set up and run kioVisits script

1. Install python 3.7
2. Create and activate virtual environment
3. Install requirements
4. Set environment variables
5. Set up autostart for raspberry pi


### 1. Install python 3.7

If python 3.7 is already installed, skip this step. If not run install_python37.sh:

`$sh install_python37.sh`

The steps in the install-script is taken from this guide: [How to install Python 3.7 on Raspberry PI (Raspbian)](https://installvirtual.com/install-python-3-7-on-raspberry-pi/)

### 2. Create and activate virtual env

Create virtual environment:

Run command: `$python3.7 -m venv venv` in terminal in project root directory.

Activate virtual environment:

Run command `$source venv/bin/activate` in terminal in project root directory.

The terminal window should now display the name of the activated virtual env on the left hand side: `(venv) $ `

To make sure the virtual env is created with python3.7:
```
(venv) $python --version
Python 3.7.1
```

### 3. Install requirements

In terminal run:

```
(venv) $pip install --upgrade pip
(venv) $pip install -r requirements.txt
```

### 4. Set environment variables

To run the script the following environment variables needs to be set.

`
ORIGO_CLIENT_ID, ORIGO_CLIENT_SECRET, ORIGO_ENVIRONMENT, ORIGO_API_KEY
`

To set the environment variables go to home directory in terminal: `$cd`

From home dir run command `$nano .profile`.

In the bottom of the .bashrc file paste:
```
# Origo SDK environment
export ORIGO_CLIENT_ID=<my-client-id>
export ORIGO_CLIENT_SECRET=<my-client-secret>
export ORIGO_ENVIRONMENT=prod
export ORIGO_API_KEY=<your-api-key>

^G Get Help        ^O WriteOut        ^R Read File       ^Y Prev Page       ^K Cut Text        ^C Cur Pos
^X Exit            ^J Justify         ^W Where Is        ^V Next Page       ^U UnCut Text      ^T To Spell
```
To save changes and exit the nano editor type: ctrl O -> enter -> ctrl X

Then to activate the changes run command:

`$source .profile`

Or you can restart the terminal.

Note: after running `$source .profile` the python virtual environment will be deactivated and you will need to reactivate it: `$source venv/bin/activate`

You are now set up to run the script :)

### 5. Set up autostart for raspberry pi

First make sure that the repository resides in the raspberry pi's home directory, e.g. path to repository is `home/pi/ren-besoksteller-gjenbrukstasjoner`.

Then run `nano .config/lxsession/LXDE-pi/autostart` and update the file with the following content:
```
@lxterminal -e bash /home/pi/ren-besoksteller-gjenbrukstasjoner/start_trigger.sh
```

The `start_trigger.sh` script will ensure that the python program runs with the virtual environment created in step 2.  
 

### 6. Not working?
If for some reason virtual environment is not working and turning out to be troublesome. Then use this commands instead:
```
$sudo pip3.7 install --upgrade pip
$sudo pip3.7 install -r requirements.txt
$python3.7 kioVisits.py
```
