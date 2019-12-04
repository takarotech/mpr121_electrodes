import time
import serial
import logging
import binascii


class UartI2cDev(object):
    _logger = logging.getLogger('uart_i2c_dev')
    _UART_TERMINATOR = b'\n'
    _UART_TIMEOUT = 0.018
    _RESET_TIMEOUT = 2

    def __init__(self, uart_port, uart_baudrate, i2c_address, i2c_endianness='little'):
        self._i2c_address = i2c_address
        self._i2c_endianness = i2c_endianness
        self._uart = serial.serial_for_url(
            uart_port, uart_baudrate, timeout=self._UART_TIMEOUT, do_not_open=True) 
        self._uart._dtr_state = False
        self._uart.open()
        self._logger.info('Connected to %s at %s baudrate, i2c address is 0x%02X',
            uart_port, uart_baudrate, i2c_address)

    def _write(self, reg_address, data=b'', size=0):
        data = bytes([self._i2c_address, size, reg_address]) + data
        data = binascii.hexlify(data) + self._UART_TERMINATOR
        self._logger.debug('uart: write(%s) -> "%s"', len(data) - 2, str(data)[2:-3])
        self._uart.write(data)
        time.sleep(self._UART_TIMEOUT)

    def read(self, reg_address, size=1):
        self._write(reg_address, size=size)
        data = self._uart.read_until(self._UART_TERMINATOR)[:-1]
        self._logger.debug('uart: read(%s) -> "%s"', len(data), data)
        try:
            data = binascii.unhexlify(data)
        except binascii.Error:
            self._logger.exception('Failed to unhexlify %s (expected %s bytes)', data, size)
            data = bytes(size)
        return data

    def write(self, reg_address, data):
        self._write(reg_address, data)

    def read_num(self, reg_address, size=1):
        return int.from_bytes(self.read(reg_address, size), self._i2c_endianness)

    def write_num(self, reg_address, value, size=1):
        self.write(reg_address, value.to_bytes(size, self._i2c_endianness))

    def reset(self):
        self._uart.setDTR(True)
        self._uart.setDTR(False)
        time.sleep(self._RESET_TIMEOUT)

    def close(self):
        self._uart.close()
