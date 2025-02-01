import logging
import glob
import os.path
import shutil
import socket
import subprocess

from CProtocol import *


class CProtocol27(CProtocol):

    def __init__(self):
        super().__init__()
        self.HEADER_SIZE: int = 4
        self.ARG_SEPARATOR = '<'
        self.COMMAND_SEPARATOR = '>'
        self.NUM_OF_COPY_ARGS = 2
        self.COMMAND_INDEX = 0
        self.ARG_INDEX = 1
        self.SOURCE_INDEX = 0
        self.DEST_INDEX = 1



    def check_cmd(self, data) -> bool:
        # write to log
        write_to_log("[PROTOCOL] - CHECK_CMD - data is " + data)
        # we check if the command entered by user aligns with our list of commands
        """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
        if (
                data == "DIR" or data == "DELETE" or data == "SEND_PHOTO" or data == "COPY" or data == "EXECUTE" or data == "TAKE_SCREENSHOT" or data == "REG" or data == DISCONNECT_MSG):
            # if it is one of our values we return true
            write_to_log("[PROTOCOL27] data is correct")
            return True
        else:
            # if it is not one of our values we return false
            return False

    def create_request_msg(self, cmd: str, args: list) -> str:
        """Create a valid protocol message, will be sent by client, with length field"""
        # we add before msg itself its length, so we can tell how much space the message is going to take
        request = ""
        if self.check_cmd(cmd):
            # create string that looks like cmd>args
            request = cmd + ">" + args
            # write to log
            write_to_log("[PROTOCOL - CRT-MSG] request - " + request)
            # return string with header with length 4 and request itself
            return f"{len(request):04d}{request}"
        elif cmd == DISCONNECT_MSG:
            return f"{len(request):04d}{cmd}"
        else:
            request = "Command is not supported by this version of protocol"
            # write to log
            write_to_log("[PROTOCOL27 - CRT-MSG] request is not supported- " + request)

            return f"{len(request):04d}{request}"

    def create_response_msg(self, cmd: str, args: str) -> str:
        # creates response msg according to what command user sent
        """Create a valid protocol message, will be sent by server, with length field"""
        response = "Non-supported cmd"
        # write to log
        write_to_log("[PROTOCOL] creates response msg with -" + cmd)
        # check cmd name and executes a function
        if cmd == "DIR":
            write_to_log("DIRRRR")
            response = self.get_dir_file_list(args)
        elif cmd == "DELETE":
            response = self.delete_file(args)
        elif cmd == "SEND_PHOTO":
            response = self.receive_big_image(args)
        elif cmd == "EXECUTE":
            response = self.execute_program(args)
        elif cmd == "TAKE_SCREENSHOT":
            response = self.take_screenshot(args)
        elif cmd == "COPY":
            response = self.copy_file_wrapper(args)
        elif cmd == "REG":
            response = "got a registration request"
        elif cmd == DISCONNECT_MSG:
            response = DISCONNECT_MSG

        return f"{len(response):04d}{response}"

    def get_dir_file_list(self, args: str) -> str:
        # get all that is in "args/"
        current_dir = args + "/" + "*"
        write_to_log(current_dir)
        dir_list = glob.glob(current_dir)

        res = str(', '.join(dir_list))
        # write to log
        write_to_log("[Protocol] files in the directory: " + res)
        return res

    def delete_file(self, file_path: str) -> str:
        res = ''
        # if there is such path (if the file exists)
        if os.path.exists(file_path):
            # remove file
            os.remove(file_path)
            res = f'File {file_path} was successfully removed'

        else:
            res = f'File {file_path} was not removed'
        # write to log
        write_to_log("[Protocol] " + res)
        return res

    def receive_buffer(self, my_socket: socket) -> (bool, str):
        buf = ""
        # receive msg from client or server
        """get buffer from socket, without the length field. If length field does not include a number, returns False, "Error" """
        str_header = my_socket.recv(self.HEADER_SIZE).decode(self.FORMAT)
        # write to log
        write_to_log(f"[Protocol - GET_MSG] str_header - {str_header}")

        if str_header.isnumeric():
            # get header length
            length = int(str_header)
            # write to log
            write_to_log(f"[Protocol - GET_MSG] length - {length}")
            if length > 0:
                # get message from the socket and decode it
                buf = my_socket.recv(length).decode(FORMAT)
        else:
            return False, 'Error'

        return True, buf

    def parse_buffer(self, request) -> (str, str):
        """
        parse the request and return a tuple of the command and argument
        :param request: the request received from the client
        :return: a tuple with the command and argument
        """
        split_request = request.split(self.COMMAND_SEPARATOR)
        command = split_request[self.COMMAND_INDEX]
        arg = ''
        if len(split_request) == self.ARG_INDEX + 1:
            arg = split_request[self.ARG_INDEX]
        return command, arg

    def parse_request(self, buf: str) -> str:
        # split buf for parts before and after >
        split_request = buf.split('>')
        # get the first part (cmd) before > in buf
        cmd = split_request[0]
        # get the second part (args) after > in buf
        args = split_request[1][0:len(split_request[1])]
        return cmd, args

    def send_big_image(self, my_socket: socket, file_name: str, chunk_size=1024) -> str:
        txt = ''
        try:
            # open file in binary reading mode
            with open(file_name, "rb") as file:
                while True:
                    # read by chunk sized bytes
                    image_data = file.read(chunk_size)
                    # when everything is read
                    if not image_data:
                        break  # Reached th end of the file

                    my_socket.send(image_data)

                txt = f'Send photo {file_name} - done'
        except FileNotFoundError:
            txt = f'Send photo {file_name} - Photo file doesnt exist'

        return txt

    def receive_big_image(self, my_socket: socket, file_name: str, chunk_size=1024) -> str:
        try:
            # open file in binary writing mode
            with open(file_name, "wb") as file:
                while True:
                    # receive bytes in chunk size
                    data = my_socket.recv(chunk_size)
                    # when empty
                    if not data:
                        break  # Reached th end of the file

                    file.write(data)
                    return "file received"
        except FileNotFoundError:
            return "File was not received"

    def execute_program(self, file_path: str) -> str:

        write_to_log(file_path)
        # call the file
        res = subprocess.call(file_path)
        if res == 0:
            response = file_path + " - successfully executed"
        else:
            response = file_path + " - was not executed"
        write_to_log('[PROTOCOL] EXECUTE command for {0} with response {1}'.format(file_path, res))
        return response

    def take_screenshot(self, img_file: str) -> str:
        # take screenshot
        image = pyautogui.screenshot()
        # saves img to img_file
        image.save(img_file)
        write_to_log('[PROTOCOL] screenshot saved to ' + img_file)
        return "screenshot saved to " + img_file

    def copy_file(self, source_path: str, destination_path: str) -> str:
        res = ''
        # if copy file exists
        if os.path.exists(source_path):
            # copy file from source path to destination path
            shutil.copy(source_path, destination_path)
            res = f'File {source_path} was copied successfully '
            write_to_log(f'[PROTOCOL] File was copied')
        else:
            res = f'File {source_path} was not copied'
            write_to_log('[PROTOCOL] File was not copied')
        return res

    def copy_file_wrapper(self, args: str) -> str:
        # parses command into source and destination, calls copy file and returns a string to send to the client
        result = ''
        split_command = args.split(self.ARG_SEPARATOR)
        if len(split_command) == self.NUM_OF_COPY_ARGS:
            src = split_command[self.SOURCE_INDEX]
            dest_dir = split_command[self.DEST_INDEX]
            if self.copy_file(src, dest_dir):
                result = 'Copied File'
        return result
