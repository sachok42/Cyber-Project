from CProtocol import *

class CClientBL:

    def __init__(self, host: str, port: int, flag: int = norm_flag):

        self._client_socket = None
        self._host = host
        self._port = port
        self.flag = flag

    def make_artist(self):
        self.flag = art_flag

    def undo_artist(self):
        self.flag = norm_flag


    def connect(self) -> socket:
        try:
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect((self._host, self._port))
            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} connected")
            return self._client_socket
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))
            return None

    def disconnect(self) -> bool:
        try:
            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} closing")
            self.send_data('', DISCONNECT_MSG)
            self._client_socket.close()
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on disconnect: {}".format(e))
            return False
