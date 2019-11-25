
# How to set up and run kioVisits script

1. Install python 3.7
2. Create and activate virtual environment
3. Install requirements
4. Set environment variables


### 1. Install python 3.7

If python 3.7 i already installed, skip this step

### 2. Create and activate virtual env

Create virtual environment:

Run command: `kioVisists$ python3.7 -m venv venv` in terminal in project root directory.

Activate virtual environment:

Run command `kioVisists$ source venv/bin/activate` in terminal in project root directory.

The terminal window should now display the name of the activated virtual env on the left hand side: `(venv) kioVisists$ `

To make sure the virtual env is created with python3.7:
```
(venv) kioVisists$ python --version
Python 3.7.1
```

### 3. Install requirements

In terminal run:

```
(venv) pip install --upgrade pip
(venv) kioVisists$ pip install -r requirements.txt
```

### 4. Set environment variables

To run the script the following environment variables needs to be set.

`
ORIGO_API_CLIENT, ORIGO_API_PASSWORD, ORIGO_ENVIRONMENT, ORIGO_API_KEY
`

To set the environment variables go to home directory in terminal: `kioVisists$ cd`

From home dir run command `$ nano .bashrc`

In the bottom of the .bashrc file paste:
```
# Origo SDK environment
export ORIGO_CLIENT_ID=my-client-id
export ORIGO_CLIENT_SECRET=my-client-secret
export ORIGO_ENVIRONMENT=prod
export ORIGO_API_KEY=your-api-key

^G Get Help        ^O WriteOut        ^R Read File       ^Y Prev Page       ^K Cut Text        ^C Cur Pos
^X Exit            ^J Justify         ^W Where Is        ^V Next Page       ^U UnCut Text      ^T To Spell
```
To save changes and exit the nano editor type: ctrl O -> enter -> ctrl X

Then to activate the changes run command:

`$ source .bashrc`

Or you can restart the terminal.

Note: after running `$ source .bashrc` the python virtual environment will be deactivated and you will need to reactivate it: `kioVisists$ source venv/bin/activate`

You are now set up to run the script :)

