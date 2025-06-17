import socket

class Interferometer:
    def __init__(self, host='127.0.0.1', port = 6385):
        self.host = host
        self.port = port

    def _command(self, message, timeout=0.1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((self.host, self.port))
                s.sendall((message + "\r\n").encode())
                data = s.recv(1024)
                return data.decode()
            except socket.timeout:
                print("Timeout when running a command")
                raise Exception("Timeout")

    def _list_to_pairs(self, base_list):
        return list(zip(base_list[::2], base_list[1::2]))

    def clear(self):
        if self._command("CLEAR") != "OK\r\n":
            raise Exception("Clear Command Failed")

    #Dunno where it goes...
    def save(self, filename):
        if self._command("CLEAR::" + filename) != "OK\r\n":
            raise Exception("Save Command Failed")

    def make_scans(self, n):
        ret =  self._command("MKSCANS::"+str(n), 120 * n)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Scan Failed")
        else:
            return self._list_to_pairs(list(map(float, ret[:-2].split("::"))))

    def set_ROI_left(self, start, stop, t):
        ret =  self._command("SETROILEFT::"+str(start)+"::"+str(stop)+"::"+str(t), 6)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Setting Left ROI failed")

    def set_ROI_right(self, start, stop, t):
        ret =  self._command("SETROIRIGHT::"+str(start)+"::"+str(stop)+"::"+str(t), 6)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Setting Right ROI failed")

    def PZT(self):
        return list(map(int, self._command("PZT?")[:-2].split("::")))

    def max_count(self):
        return int(self._command("MAXCOUNT?")[:-2])

    def mode(self):
        return self._command("MODE?")[:-2]

    def ready(self):
        return self._command("STATE?") == "Ready\r\n"

    def sweeping(self):
        return self._command("SWEEPING?") == "T\r\n"

    def ROI_left(self):
        return list(map(float, self._command("ROILEFT?")[:-2].split("::")))

    def ROI_right(self):
        return list(map(float, self._command("ROIRIGHT?")[:-2].split("::")))

    def scan_ms(self):
        return int(self._command("MSSCAN?")[:-2])

    def data(self):
        return self._list_to_pairs(list(map(float, self._command("DATA?")[:-2].split("::"))))

    def data_syn(self):
        return list(map(float, self._command("DATASYN?", 60)[:-4].split("::")))
interferometer = Interferometer()
print(interferometer.ready())
print(interferometer.mode())
print(interferometer.sweeping())
print(interferometer.ROI_left())
print(interferometer.ROI_right())
print(interferometer.scan_ms())
print(interferometer.max_count())
print(interferometer.PZT())
interferometer.clear()
interferometer.save("test")
print(interferometer.data())
print(interferometer.set_ROI_left(-150, -60, 0.167))
print(interferometer.ROI_left())
print(interferometer.data_syn())
print(interferometer.make_scans(4))