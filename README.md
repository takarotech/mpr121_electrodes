# MPR121 Electrodes
Interactive python test code for MPR121 sensors.

## Install From Repo
```
git clone https://github.com/takarotech/mpr121_electrodes.git
```
#### Windows
```mpr121_electrodes\install.bat```
#### Ubuntu
```./mpr121_electrodes/install.sh```

## Getting Started
#### Flash Arduino code
```arduino --upload ./mpr121_electrodes/src/arduino_uart_i2c_pipe/arduino_uart_i2c_pipe.ino --port /dev/ttyUSB0```
#### Run CLI
```./mpr121_electrodes/run_mpr121_electrodes.sh```

## Snippets:
#### Config the registers and enter reading mode
```app.mpr121.config_regs()```
#### Print registers tree
```app.mpr121.regs```
#### Read touch_status register
```app.mpr121.regs.touch_status.get()```
#### Writes debounce register
```app.mpr121.regs.debounce.touch.set(3)```
#### Logs electrodes touch events
```app.log_electrodes()```

## Enjoy!
Qni team

