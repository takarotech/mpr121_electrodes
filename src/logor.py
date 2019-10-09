import logging


def config_logger(formats, level, color_map):
    '''
    Colorize root log records.
    '''
    logging.root.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(formats[0], formats[1], color_map))
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    logging.root.addHandler(handler)

    logging.root.log(
        logging.root.level,
        f'Logging level: {logging.getLevelName(logging.root.level)}')


class ColorFormatter(logging.Formatter):
    '''
    Colorize log records fields with the given color_map.
    '''

    def __init__(self, fmt=None, datefmt=None, color_map=None):
        if color_map is None:
            color_map = {}
        self._esc = color_map.pop('esc')
        self._default = color_map.pop('default')
        self._asctime = color_map.pop('asctime', self._default)
        self._fields_codes = {
            k: v for k, v in color_map.items() if type(k) is str}
        self._levels_codes = {
            k: v for k, v in color_map.items() if type(k) is int}
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        record.msg = f'{self._levels_codes.get(record.levelno, self._default)}{record.msg}{self._esc}'
        for field, codes in self._fields_codes.items():
            setattr(record, field, f'{codes}{getattr(record, field)}{self._esc}')
        return logging.Formatter.format(self, record)

    def formatTime(self, record, datefmt=None):
        return f'{self._asctime}{logging.Formatter.formatTime(self, record, datefmt)}{self._esc}'
