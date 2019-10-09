
class SubReg(object):

    def __init__(self, start_bit, bits_count):
        self._reg = None
        self._name = None
        self._start_bit = start_bit
        self._bitmask = (1 << bits_count) - 1

    def get(self, read=True):
        return (self._reg.get(read) >> self._start_bit) & self._bitmask

    def set(self, value, write=True):
        reg_value = self._reg.get(False)
        reg_value &= ~(self._bitmask << self._start_bit)
        reg_value |= (value & self._bitmask) << self._start_bit
        self._reg.set(reg_value, write)

    def __call__(self):
        return self.get()

    def __str__(self):
        return f'{self._name} = {self.get(False)}'

    def __repr__(self):
        return self.__str__()


class Register(object):

    def __init__(self, address, bits_count, default_value, **sub_regs):
        self._dev = None
        self._name = None
        self._address = address
        self._default_value = default_value
        self._bytes_count = (bits_count + 7) // 8
        self._bytes = bytes(self._bytes_count)
        self._write_hook = sub_regs.pop('write_hook', lambda x: None)
        self._sub_regs = sub_regs.values()

        for k, v in sub_regs.items():
            v._name = k
            v._reg = self
            setattr(self, k, v)

    def _read(self):
        data = self._dev.read(self._address, len(self._bytes))
        data = bytes(max(0, self._bytes_count - len(data))) + data[:self._bytes_count]
        self._bytes = data
        return int.from_bytes(self._bytes, self._dev._i2c_endianness)

    def _write(self):
        self._write_hook(True)
        self._dev.write(self._address, self._bytes)
        self._write_hook(False)

    def get(self, read=True):
        if read:
            self._read()
        return int.from_bytes(self._bytes, self._dev._i2c_endianness)

    def set(self, value=None, write=True, default=False, **sub_regs):
        if sub_regs:
            for k, v in sub_regs.items():
                getattr(self, k).set(v, False)
            if not write:
                return
        if value is None:
            if default:
                value = self._default_value
            else:
                value = self.get(False)
        self._bytes = value.to_bytes(len(self._bytes), self._dev._i2c_endianness)
        if write:
            self._write()

    def __call__(self):
        return self.get()

    def __str__(self):
        sub_regs = '\n'.join(f'    {i}' for i in self._sub_regs)
        return f'{self._name}\n{sub_regs}'

    def __repr__(self):
        return self.__str__()


class Registers(object):

    def __init__(self, name, dev, **regs):
        self._name = name
        self._dev = dev
        self._regs = regs.values()

        for k, v in regs.items():
            v._name = k
            v._dev = self._dev
            v.set(default=True, write=False)
            setattr(self, k, v)

    def __str__(self):
        regs = '\n'.join('\n'.join(f'    {i}' for i in str(r).splitlines()) for r in self._regs)
        return f'{self._name}\n{regs}'

    def __repr__(self):
        return self.__str__()
