# MicroPython-TFTP-Client
A simple TFTP client in MicroPython. Fully functional PUT and GET in both the default octet and optional netascii modes. RFC 1350 and RFC 764 complient. Complete with os and server error reporting. Check example-use.py for use. Originally written for the esp32 micro controller, tested and working on Ubuntu 24.04.1 LTS.

    Class: TFTPClient([host='255.255.255.255'], [port=69])

        Creates a TFTPClient with methods for communication with TFTP server 'host'

        Args:
            host (str): Defaults to '255.255.255.255'
            port (int): Optional. Defaults to 69.

        Returns:
            TFTPClient: TFTPClient for communication with TFTP server 'host'
        
    Method: put_file('file_name', [mode='octet'])

        PUT 'file_name' to 'host' using 'mode'

        Args:
            file_name (str): Name of file to be PUT.
            mode (str): Optional. Defaults to 'octet'.

        Returns:
            boolean: Indicates success. True/False.
    

    Method: get_file('file_name', [mode='octet'])

        GET 'file_name' from 'host' using 'mode'

        Args:
            file_name (str): Name of file to GET.
            mode (str): Optional. Defaults to 'octet'.

        Returns:
            boolean: Indicates success. True/False.
    
