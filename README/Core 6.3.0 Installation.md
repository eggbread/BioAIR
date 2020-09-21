# CORE 6.3.0 installation

This document is installation manual for CORE 6.3.0

Recommend Environment
> OS - Ubuntu 18.04
> Default Python - 3.6.0~3.6.9

(If your OS is based on linux and the system python version is 3.6.0~3.6.9,
You can probably install and run CORE 6.3.0 without any problem)

# Set Default Python version

The CORE 6.3.0 is base on python-3.6.0-3.6.9 </br>
We must set python 3.6.0~3.6.9 as the system python version.</br>
(if your default python is 3.6.0-3.6.9, you don't need this step)

> **how to check default python version**
> `python3 --version`

- Download - [Python-3.6.9.tar.xz](https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tar.xz) 
- Extract the .tar.xz.file
- `cd Python-3.6.9`
-  `./configure`<br/>
    `make`<br/>
    `make test`<br/>
    `sudo make install`
# Install Pre-Req package 
For install CORE,
There are some pre-req packages

## 1. Install Linux package
` sudo apt install build-essential quagga python3-pip git`

## 2. Install pip3 pacakge

`pip3 install configparser==4.0.2 future==0.17.1 grpcio==1.23.0 grpcio-tools==1.21.1 lxml==4.4.1 protobuf==3.9.1 six==1.12.0`


# Install CORE
- Download 
  [core_6.3.0_amd64.deb](https://github.com/coreemu/core/releases/download/release-6.3.0/core_6.3.0_amd64.deb)
- Install CORE using .deb file (just open & click)
  
# Run CORE
 To run CORE,
 You have to command these lines on terminal.

`sudo systemctl daemon-reload`<br/>
`sudo systemctl start core-daemon`<br/>
<br/>
`sudo service core-daemon start`<br/>
`sudo core-daemon`<br/>
<br/>
`core-gui`  

 After first initial running,
 You  just need these two line.

 `sudo core-daemon`<br/>
`core-gui`  
