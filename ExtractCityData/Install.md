# Install Notes

## Install pre-requisite tools

````
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install virtualenv      # Mind the sudo or the install will happen in `$(HOME)/.local/...`
````

## Deploy a virtual environment

This step is not mandatory; it is useful for having local dependencies to the
packages installed next.

````
virtualenv -p /usr/bin/python3 venv
. venv/bin/activate
````

## Install Python dependencies

````
pip install --upgrade setuptools
pip install -e .
````

[Setuptools](https://pypi.python.org/pypi/setuptools) allows to
"Easily download, build, install, upgrade, and uninstall Python packages".

`pip install -e .` gets the requirements from setup.py and install them automatically.
