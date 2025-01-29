# MicroPython-TFTP-Client
A simple TFTP client in MicroPython. Fully functional PUT and GET in the default octet mode, with os and server error reporting. GET is working in netascii mode, while PUT is still work in progress and currently disabled. Check example-use.py for use.

    Class: TFTPClient([host='255.255.255.255'], [port=69])

        Creates a socket for communication with 'host'

        Args:
            host (str): Defaults to '255.255.255.255'
            port (int): Optional. Defaults to 69.

        Returns:
            socket: Socket for communication with TFTP server
        
    Method: put_file('file_name', [mode='octet'])

        PUT's file_name to server using 'mode'

        Args:
            file_name (str): Name of file to be PUT.
            mode (str) Optional. Default 'octet'.

        Returns:
            Bool: Indecates success. True/False.
    

    Method: get_file('file_name', [mode='octet'])

        GET's file_name from server using 'mode'

        Args:
            file_name (str): Name of file to GET.
            mode (str) Optional. Default 'octet'.

        Returns:
            Bool: Indecates success. True/False.
    
