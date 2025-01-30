# MicroPython-TFTP-Client
A simple TFTP client in MicroPython. Fully functional PUT and GET in the default octet mode complete with os and server error reporting. GET works fine in netascii mode, while PUT is still work in progress and currently disabled. Check example-use.py for use. Originally written for esp32, but tested and just as functional on Ubuntu 24.04.1 LTS.

    Class: TFTPClient([host='255.255.255.255'], [port=69])

        Creates a socket and methods for communication with TFTP server 'host'

        Args:
            host (str): Defaults to '255.255.255.255'
            port (int): Optional. Defaults to 69.

        Returns:
            TFTPClient: Socket and methods for communication with TFTP server 'host'
        
    Method: put_file('file_name', [mode='octet'])

        PUT's 'file_name' to 'host' using 'mode'

        Args:
            file_name (str): Name of file to be PUT.
            mode (str) Optional. Defaults to 'octet'.

        Returns:
            boolean: Indecates success. True/False.
    

    Method: get_file('file_name', [mode='octet'])

        GET's 'file_name' from 'host' using 'mode'

        Args:
            file_name (str): Name of file to GET.
            mode (str) Optional. Defaults to 'octet'.

        Returns:
            boolean: Indecates success. True/False.
    
