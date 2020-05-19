import os
import platform

if platform.system() == 'Linux':
    def clear():
        """
        Clears terminal window
        """
        os.system('clear')

    def get_terminal_size():
        """
        Returns terminal window size on Unix
        Have no idea why it works
        """
        import fcntl
        import termios
        import struct

        env = os.environ

        def get_cr(fd):
            try:
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                     '1234'))
            except Exception:
                return
            return cr

        cr = get_cr(0) or get_cr(1) or get_cr(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = get_cr(fd)
                os.close(fd)
            except Exception:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
        return int(cr[1])

    def print_wall():
        """
        Prints line of '='.
        Number of them equals to terminal window size
        """
        for _ in range(get_terminal_size()):
            print('=', end='')
else:
    def clear():
        """
        Clears cmd window
        """
        os.system('cls')

    def print_wall():
        """
        Prints a wall of '=' in Windows
        """
        for _ in range(80):
            print('=', end='')
        print()
