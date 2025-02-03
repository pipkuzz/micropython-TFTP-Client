import socket
import os


class TFTPClient:
    DEFAULT_PORT = 69
    DEFAULT_TIMEOUT = 2
    DEFAULT_HOST = '255.255.255.255'
    GET_REQ_PKT = b'\x00\x01'
    PUT_REQ_PKT = b'\x00\x02'
    DATA_PKT = b'\x00\x03'
    ACK_PKT = b'\x00\x04'
    ERROR_PKT = b'\x00\x05'
    READ_DATA_SIZE = 512
    READ_BLK_SIZE = 516
    ACK_SIZE = 4

    def __init__(self, host=DEFAULT_HOST,
                 port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def send_request(self, request, sock):
        try:
            sock.sendto(request, (self.host, self.port))
            return True
        except Exception as e:
            print(f"Error: Failed to connect to host {self.host}:",
                  f"{self.port}.\nError: {e}")
            return False

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.DEFAULT_TIMEOUT)
        return sock

    def receive_ack(self, sock):
        try:
            ack, addr = sock.recvfrom(self.ACK_SIZE)
            if ack[:2] == self.ERROR_PKT:
                self.handle_error(ack)
                return None, None
            return ack, addr
        except Exception as e:
            print(f"Error: Failed to receive ACK.\nError: {e}")
            return None, None

    def send_ack(self, ack, addr, sock):
        try:
            sock.sendto(ack, addr)
            return True
        except Exception as e:
            print(f"Error: Failed to send ACK to {addr}.\nError: {e}")
            return False

    def receive_data(self, sock):
        try:
            data, addr = sock.recvfrom(self.READ_BLK_SIZE)
            if data[:2] == self.ERROR_PKT:
                self.handle_error(data)
                return None, None
            return data, addr
        except Exception as e:
            print("Error: Failed to receive data from",
                  f"{self.host}:{self.port}\nError: {e}")
            return None, None

    def send_data(self, data_pkt, addr, sock):
        try:
            sock.sendto(data_pkt, addr)
            return True
        except Exception as e:
            print(f"Error: Failed to send data to {addr}.\nError: {e}")
            return False

# ***********************   put_file   **************

    def put_file(self, file_name, mode='octet'):
        try:
            sock = self.create_socket()
            # Check if the file exists
            try:
                os.stat(file_name)
            except OSError:
                print(f"Error: File '{file_name}' does not exist.")
                return False
            # send request to PUT file
            putrequest = (self.PUT_REQ_PKT + file_name.encode()
                          + b'\x00' + mode.encode()
                          + b'\x00')
            if self.send_request(putrequest, sock):
                ack, addr = self.receive_ack(sock)
                # if it's a valid response to the request
                if ack == (self.ACK_PKT + b'\x00\x00'):
                    try:
                        # open file to send
                        with open(file_name, 'rb') as f:
                            send_blk_num = 1
                            overflow = bytearray()
                            while True:
                                # Read 512 bytes from the file
                                data = f.read(self.READ_DATA_SIZE)
                                # convert to netascii if needed
                                if mode == 'netascii':
                                    data = self.to_netascii(data)
                                # Prepend overflow from the previous chunk
                                data = overflow + data
                                if (len(data) < self.READ_DATA_SIZE):
                                    overflow = data
                                    break
                                # Split data into 512 byte blocks
                                while len(data) >= self.READ_DATA_SIZE:
                                    # Create a TFTP data packet
                                    data_pkt = (self.DATA_PKT +
                                                send_blk_num.to_bytes(2, 'big')
                                                + data[:self.READ_DATA_SIZE])
                                    # Send the packet to the server
                                    if not self.send_data(data_pkt,
                                                          addr, sock):
                                        return False
                                    # Increment the block number
                                    send_blk_num += 1
                                    # Receive ACK
                                    ack, addr = self.receive_ack(sock)
                                    if ack is None:
                                        return False
                                    data = data[self.READ_DATA_SIZE:]
                                # Save overflow for the next chunk
                                overflow = data
                            # Send any remaining overflow
                            if overflow:
                                # Create a TFTP data packet
                                data_pkt = (self.DATA_PKT
                                            + send_blk_num.to_bytes(2, 'big')
                                            + overflow)
                                # Send the packet to the server
                                if not self.send_data(data_pkt, addr, sock):
                                    return False
                                # Increment the block number
                                send_blk_num += 1
                                # Receivesend_request ACK
                                ack, addr = self.receive_ack(sock)
                                if ack is None:
                                    return False
                            # Send zero-byte if last packet was == 512 bytes
                            if len(overflow) == 0 and len(data) % self.READ_DATA_SIZE == 0:
                                zero_pkt = (self.DATA_PKT +
                                            send_blk_num.to_bytes(2, 'big')
                                            + b'')
                                if not self.send_data(zero_pkt, addr, sock):
                                    return False
                        return True
                    except Exception as e:
                        print("Error: An I/O error occurred reading file ",
                              f"'{file_name}' \nError: {e}")
                        return False
                else:
                    return False
            else:
                return False
        finally:
            sock.close()

# **********************   get_file   ********************

    def get_file(self, file_name, mode='octet'):
        try:
            sock = self.create_socket()
            # Send request for 'file_name'
            getrequest = (self.GET_REQ_PKT
                          + file_name.encode() + b'\x00' + mode.encode()
                          + b'\x00')
            if self.send_request(getrequest, sock):
                # Open or create file to write to
                with open(file_name, 'wb') as f:
                    # Loop for as long as we're receiving data
                    while True:
                        # read data and address from the socket
                        data, addr = self.receive_data(sock)
                        # check we have received some data
                        if data is None:
                            return False
                        # check it's a type 3 data packet
                        if len(data) < 4 or data[:2] != self.DATA_PKT:
                            print("ERROR: No data received")
                            return False
                        # Send ACK for the data block
                        recvd_blk_num = int.from_bytes(data[2:4], 'big')
                        ack = (self.ACK_PKT
                               + recvd_blk_num.to_bytes(2, 'big'))
                        if not self.send_ack(ack, addr, sock):
                            return False
                        # get data from packet
                        write_data = data[4:]
                        # convert from netacii if needed
                        if mode == 'netascii':
                            write_data = self.from_netascii(write_data)
                        # write data block to file
                        f.write(write_data)
                        # If received block < 516 bytes we have it all
                        if len(data) < self.READ_BLK_SIZE:
                            return True
            else:
                return False
        finally:
            sock.close()

# **********************   netascii functions   *************

    def to_netascii(self, data):
        # Convert data to Netascii format
        netascii_data = (data.replace(b'\r', b'\r\0')
                         .replace(b'\n', b'\r\n'))
        return netascii_data

    def from_netascii(self, data):
        # Convert data from Netascii format
        from_netascii_data = (data.replace(b'\r\n', b'\n')
                              .replace(b'\r\0', b'\r'))
        return from_netascii_data

# **********************   handle TFTP server error codes   ************

    def handle_error(self, error_pkt):
        error_code = int.from_bytes(error_pkt[2:4], 'big')
        error_msg = error_pkt[4:].decode()
        print(f"TFTP Error {error_code}: {error_msg}")

