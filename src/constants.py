import logging
from ansi import C


UART_PORT = None # 'COM15'
UART_BAUDRATE = 115200

MPR121_ADDRESS = 0x5A
MPR121_ELECTRODES_COUNT = 12

LOG_LEVEL = logging.INFO
LOG_FORMATS = (
    '%(asctime)s %(name)s %(levelname)s: %(message)s', '%Y_%m_%d_%H_%M_%S')
LOG_COLOR_MAP = {
    logging.CRITICAL: C.YELLOW|C.BRIGHT|C.RED_BG,
    logging.ERROR: C.RED|C.BRIGHT,
    logging.WARNING: C.YELLOW|C.BRIGHT,
    logging.INFO: C.CYAN|C.FAINT,
    logging.DEBUG: C.CYAN|C.BRIGHT,
    'name': C.GREEN|C.FAINT,
    'asctime': C.BLACK|C.BRIGHT,
    'levelname': C.MAGENTA|C.BRIGHT,
    'default': C.WHITE|C.BRIGHT,
    'esc': C.ESC,
}

BANNER = f'''
{C.GREEN|C.BRIGHT}MPR121 Electrodes CLI:{C.ESC}
    Press <dot> follow by <tab> for auto completion!
    Press <ctrl>+d to exit!

    {C.GREEN}Examples:{C.ESC}
        {C.CYAN|C.BRIGHT}app.mpr121.config_regs()      {C.BLACK|C.BRIGHT}# Config the registers and enter reading mode.
        {C.CYAN|C.BRIGHT}app.mpr121.regs               {C.BLACK|C.BRIGHT}# Print registers tree.
        {C.CYAN|C.BRIGHT}app.mpr121.touch_status.get() {C.BLACK|C.BRIGHT}# Read touch_status register.
        {C.CYAN|C.BRIGHT}app.log_electrodes()          {C.BLACK|C.BRIGHT}# Logs electrodes touch events (<ctrl>+c exit) 
{C.ESC}
'''
