#!/usr/bin/python3

import sys
if not sys.version_info.major >= 3 and sys.version_info.minor >= 6:
    print('Python 3.6 or higher is required! this is {}'.format(sys.version))
    sys.exit(1)
import logging
import serial.tools.list_ports
import IPython.terminal.embed as _ipython

import logor
import mpr121
import constants
import electrodes
import uart_i2c_dev
from ansi import C


class App(object):
    _logger = logging.getLogger('app')

    def __init__(self):
        # Print banner to terminal
        print(constants.BANNER)
        # Configure logger stuff
        logor.config_logger(
            constants.LOG_FORMATS, constants.LOG_LEVEL, constants.LOG_COLOR_MAP)
        # Get uart port from user if needed
        if constants.UART_PORT is None:
            constants.UART_PORT = self._get_port_from_user()
        # Create uart <-> i2c pipe
        self._dev = uart_i2c_dev.UartI2cDev(
            constants.UART_PORT, constants.UART_BAUDRATE, constants.MPR121_ADDRESS)
        # Create mpr121 and electrodes objects
        self.mpr121 = mpr121.Mpr121(self._dev, constants.MPR121_ELECTRODES_COUNT)
        self.electrodes = electrodes.Electrodes(self.mpr121.elec_count)

    def _get_port_from_user(self):
        self._logger.warning('constants.py: UART_PORT=None, searching...')
        ports = serial.tools.list_ports.comports()
        ports_count = len(ports)
        if ports_count == 0:
            self._logger.error('No uart ports were found, please connect one and re-run')
            self.__exit__(1)
        if ports_count == 1:
            self._logger.warning('Found single uart port, connecting...')
            return ports[0].device
        self._logger.warning('Found %s uart ports:', ports_count)
        sep = f'\n{C.DEFAULT}{"="*80}{C.ESC}\n'
        print(sep)
        for i in ports:
            print(f'{C.CYAN|C.BRIGHT}{i.device}{C.YELLOW|C.BRIGHT} - {i.description}{C.ESC}')
        print(sep)
        ports = [i.device for i in ports]
        while True:
            try:
                port = input(f'Enter the arduino uart port name (like {ports[0]}): ')
            except KeyboardInterrupt:
                self.__exit__(2)
            if port in ports:
                return port

    def _update_electrodes(self):
        # bitmask = self.mpr121.raw_read_num(0x00, 1) # faster for <=8 electrodes
        bitmask = self.mpr121.regs.touch_status.get()
        for i in range(self.mpr121.elec_count):
            self.electrodes.electrodes[i]._set_touched(bitmask & 1)
            bitmask >>= 1

    def log_electrodes(self):
        if not self.mpr121._configured:
            self._logger.warning('MPR121 is not configured, calling config_regs()!')
            self.mpr121.config_regs()
        try:
            while True:
                self._update_electrodes()
                for i in self.electrodes.get_newly_touched():
                    self._logger.info('E_%02d touched!', i.index)
                for i in self.electrodes.get_newly_released():
                    self._logger.info('E_%02d released!', i.index)
        except KeyboardInterrupt:
            pass

    def log_electrodes_raw(self):
        if not self.mpr121._configured:
            self._logger.warning('MPR121 is not configured, calling config_regs()!')
            self.mpr121.config_regs()
        try:
            while True:
                self.mpr121.regs.electrode_value.get()
                values = [getattr(self.mpr121.regs.electrode_value, f'e{i:02}').get() for i in range(8)]
                self._logger.info('%s', values)
        except KeyboardInterrupt:
            pass

    def __exit__(self, exit_code=None):
        print('\n')
        self._logger.warning('Goodbye!\n')
        try:
            self._dev.close()
        except Exception:
            pass
        if exit_code is not None:
            sys.exit(exit_code)


def main():
    _ipython_shell = _ipython.InteractiveShellEmbed()
    _ipython_shell.banner1 = ''
    _ipython_shell.confirm_exit = False
    app = App()
    _ipython_shell()
    app.__exit__()


if __name__ == '__main__':
    main()
