import socket

import Util


class Interferometer:
    """
    This interferometer software works through the Brilliant software
    The Brilliant program must be running in order for the calls in this program to work
    """

    def __init__(self, host='127.0.0.1', port = 6385):
        """
        Initialize an interferometer through the Brilliant software
        Note: The Brilliant software must be open in order for the commands to work
        :param host: The IP address of the software
        :param port: The corresponding port to communicate through
        """
        self.host = host
        self.port = port

    def _command(self, message, timeout=0.1):
        """
        Make a command and get a response
        Throws an error is the timeout expires
        :param message: The message to send
        :param timeout: The amount of time to wait for a response
        :return: The response, if available
        """
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

    def clear(self):
        """
        Clears accumulation buffer (spectrum)
        :raise Clear Command Failed: If the command fails
        """
        if self._command("CLEAR") != "OK\r\n":
            raise Exception("Clear Command Failed")

    def save(self, filename):
        """
        Saves current accumulation buffer (spectrum) to the disk.
        File is written to the main folder of the Brilliant
        :param filename: The file name to save the file as
        :raise Save Command Failed: If the command fails
        """
        # TODO: Figure out where this goes
        if self._command("CLEAR::" + filename) != "OK\r\n":
            raise Exception("Save Command Failed")

    def make_scans(self, n):
        """
        Clears spectrum, makes N scans, and returns the accumulation buffer
        WARNING: This can take a long time to make all the scans (max 120 seconds per scan)
        :param n: The number of scans to make
        :return: The current accumulation buffer (spectrum) in a list of ordered pairs [(x1,y1), (x2,y2) ...]
        :raise Scan Failed: If the scan fails
        """
        ret =  self._command("MKSCANS::"+str(n), 120 * n)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Scan Failed")
        else:
            return Util.list_to_pairs(list(map(float, ret[:-2].split("::"))))

    def set_ROI_left(self, start, stop, t):
        """
        Waits until a scan becomes active (max 5 s) and sets new ROI parameters.
        Parameters become valid starting from the next scan.
	    Channel numbers correspond to those appearing in the Channel/X-Scale mode.
	    The channel numbers should be negative and |start| > |stop|
        :param start: The left channel boundary (included)
        :param stop: The right channel boundary (excluded)
        :param t: The scale between the channels and frequency
        :raise Setting Left ROI failed: If the command fails
        """
        ret =  self._command("SETROILEFT::"+str(start)+"::"+str(stop)+"::"+str(t), 6)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Setting Left ROI failed")

    def set_ROI_right(self, start, stop, t):
        """
        Waits until a scan becomes active (max 5 s) and sets new ROI parameters.
        Parameters become valid starting from the next scan.
	    Channel numbers correspond to those appearing in the Channel/X-Scale mode.
	    The channel numbers should be positive and start < stop
        :param start: The left channel boundary (included)
        :param stop: The right channel boundary (excluded)
        :param t: The scale between the channels and frequency
        :raise Setting Right ROI failed: If the command fails
        """
        ret =  self._command("SETROIRIGHT::"+str(start)+"::"+str(stop)+"::"+str(t), 6)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Setting Right ROI failed")

    def PZT(self):
        """
        Returns values of PZTs
        :return: The values of the PZTs in the form [x1, y1, x2, y2, z, dz]
        """
        return list(map(int, self._command("PZT?")[:-2].split("::")))

    def max_count(self):
        """
        Returns maximum count in the region of stabilization for the most recent scan
        :return: The maximum count
        """
        return int(self._command("MAXCOUNT?")[:-2])

    def mode(self):
        """
        Returns the current mode (Measurement/Tandem/Reflection)
        :return: The mode as a string
        """
        return self._command("MODE?")[:-2]

    def ready(self):
        """
        Returns whether the machine is ready for a new command
        :return: True if the machine is ready, False if it is busy
        """
        return self._command("STATE?") == "Ready\r\n"

    def sweeping(self):
        """
        Returns whether sweeping is active
        :return: True if sweeping is active, False otherwise
        """
        return self._command("SWEEPING?") == "T\r\n"

    def ROI_left(self):
        """
        Returns the left ROI
        :return: The left ROI in the form [Start freq, number of channels, freq increase per channel]
        """
        return list(map(float, self._command("ROILEFT?")[:-2].split("::")))

    def ROI_right(self):
        """
        Returns the right ROI
        :return: The right ROI in the form [Start freq, number of channels, freq increase per channel]
        """
        return list(map(float, self._command("ROIRIGHT?")[:-2].split("::")))

    def scan_ms(self):
        """
        Returns duration of scans in ms.
        :return: Duration of scans in ms
        """
        return int(self._command("MSSCAN?")[:-2])

    def data(self):
        """
        Returns the current accumulation buffer (spectrum)
        :return: The accumulation buffer in the format [(x1,y1), (x2,y2), ...]
        """
        return Util.list_to_pairs(list(map(float, self._command("DATA?")[:-2].split("::"))))

    def data_syn(self):
        """
        Waits until the current scan is completed and then returns:
	    scan number, scan duration (ms), gate enable state (1/0),
	    gate enable state for the following scan (1/0), and the accumulation buffer.

        :return: The information in the format [n, d, 1/0, 1/0, x1, y1, x2, y2 ...]
        :raise Timeout Error: If the scan doesn't end within 5 seconds
        """
        ret = self._command("DATASYN?", 6)
        if ret.split("::")[0] == "ERROR":
            print(ret)
            raise Exception("Timeout Error")
        return list(map(float, ret[:-4].split("::")))