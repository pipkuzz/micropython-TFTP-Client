# MicroPython-TFTP-Client
A simple TFTP client in MicroPython. Fully functional PUT and GET in the default octet mode, with os and server error reporting. GET is working in netascii mode, while PUT is still work in progress and currently disabled. Check example-use.py for use.

    Class: TFTPClient([host='255.255.255.255'], [port=69], [mode='octet'])

        Creates a socket and methods for communication with 'host'

        Args:
            host (str): Defaults to '255.255.255.255'
            port (int): Optional. Defaults to 69.
            mode (str) Optional. Defaults to 'octet'.
        Returns:
            socket: Socket for communication with TFTP server
        
    Method: put_file('file_name')

        PUT's 'file_name' to 'host' using 'mode'

        Args:
            file_name (str): Name of file to be PUT.

        Returns:
            boolean: Indecates success. True/False.
    

    Method: get_file('file_name')

        GET's 'file_name' from 'host' using 'mode'

        Args:
            file_name (str): Name of file to GET.

        Returns:
            boolean: Indecates success. True/False.
    
