import socket

class ArtNetSender:
    def __init__(self, ip, universe):
        self.ip = ip
        self.universe = universe
        self.sequence = 0
        self.connected = False
        self.packet = bytearray(530)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._build_header()

    def connect(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.connected = True

    def send_dmx(self, dmx_data):
        self.sequence = (self.sequence + 1) % 256
        self.packet[12] = self.sequence
        if not self.connected: return

        self.packet[18:530] = dmx_data[:512]
        self.sock.sendto(self.packet, (self.ip, 6454))

    def close(self):
        self.sock.close()
        self.connected = False

    def _build_header(self):
        self.packet[0:8] = b'Art-Net\x00'
        self.packet[8] = 0x00  # OpCode Low
        self.packet[9] = 0x50  # OpCode High
        self.packet[10] = 0x00  # Protocol Version High
        self.packet[11] = 0x0E  # Protocol Version Low (14)
        self.packet[12] = 0  # Sequence (wird später überschrieben)
        self.packet[13] = 0  # Physical
        self.packet[14] = self.universe & 0xFF  # Universe Low
        self.packet[15] = (self.universe >> 8) & 0xFF  # Universe High
        self.packet[16] = 0x02  # Length High (512 = 0x0200)
        self.packet[17] = 0x00  # Length Low
