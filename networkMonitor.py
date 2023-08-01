from lib.logger import Logger, Level
from lib.net import NetInfo, NetUnit
import time
import sys, atexit
from datetime import datetime

def kill_handler(signal, frame):
    exit_handler()
    sys.exit(1)

@atexit.register
def exit_handler():
    print('Raspberry-Network-Monitor exited ...')

class NetMonitor:

    def __init__(self, updateDelay) -> None:
        self.logger = Logger('NetMonitor')
        self.lastUploadBytes = 0
        self.lastDownloadBytes = 0
        self.updateDelay = updateDelay
        self.canAddSpace = False

    def logSpace(self):
        self.logger.log(Level.Info, f'\u25E2\u25E4\u25E2\u25E4\u25E2\u25E4\u25E2\u25E4 DateTime is {datetime.now()} \u25E5\u25E3\u25E5\u25E3\u25E5\u25E3\u25E5\u25E3')

    def start(self):
        #Ignoring first read
        uploadSpeed = NetInfo.getUploadSpeed(0.1, self.lastUploadBytes, NetUnit.MB)
        downloadSpeed = NetInfo.getDownloadSpeed(0.1, self.lastDownloadBytes, NetUnit.MB)
        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]

        self.logSpace()

        while True:
            currentHour = int(datetime.now().strftime("%H"))
            if currentHour != 0:
                self.canAddSpace = True
            
            if self.canAddSpace and currentHour == 0:
                self.canAddSpace = False
                self.logSpace()
            
            self.run(self.updateDelay)
            time.sleep(self.updateDelay)
    
    def run(self, deltaTime):
        uploadSpeed = NetInfo.getUploadSpeed(deltaTime, self.lastUploadBytes, NetUnit.MB)
        downloadSpeed = NetInfo.getDownloadSpeed(deltaTime, self.lastDownloadBytes, NetUnit.MB)

        self.lastUploadBytes = uploadSpeed[1]
        self.lastDownloadBytes = downloadSpeed[1]
        uploadSpeed = round(uploadSpeed[0], 4)
        downloadSpeed = round(downloadSpeed[0], 4)

        self.logger.log(Level.Trace, f"Us[{uploadSpeed} MB/s], Ds[{downloadSpeed} MB/s]")


if __name__ == '__main__':
    print('Raspberry-Network-Monitor started ...')

    Logger.logConsoleToLevel = Level.Info
    Logger.logFileToLevel = Level.All
    Logger.fileName = 'output.log'
    
    try:
        NetMonitor(300).start()
    except Exception as e:
        print(str(e))
        sys.exit(2)