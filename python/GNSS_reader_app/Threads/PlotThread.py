import threading
from multiprocessing import Queue
import time
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

GRAPH_WIDTH = 500
GRAPH_HEIGHT = 100
GRAPH_H1_L= 51
GRAPH_H1_H = 53

GRAPH_H2_L= 20
GRAPH_H2_H = 22

GRAPH_H3_L= 100
GRAPH_H3_H = 120

GRAPH_H = 200
k = 100

class PlotThread(threading.Thread):
    def __init__(
            self,
            msgq: Queue,
            stop_program:bool,
            semaphore,#:threading.Semaphore(1),
            start_time: float,
            daemon: bool = True,
            **kwargs
    ):
        super(PlotThread, self).__init__(daemon=daemon)
        self.msgq = msgq
        self.start_time = start_time
        self.semaphore = semaphore
        self.stop_program = stop_program
        self.t_max = 5000
        print(f'\tTrying to plot data')
        self.semaphore.acquire()


    def run(self):
        app = QtGui.QApplication([])
        # win = pg.GraphicsWindow(title="Basic plotting examples") # use with one plot
        win = pg.GraphicsLayoutWidget(title="Basic plotting examples") #  use with subplots
        win.resize(1000, 600)
        win.setWindowTitle('Current position from GNSS')
        p1 = win.addPlot(title="Longitude") # adding new subplots
        p2 = win.addPlot(title="Latitude")
        p3 = win.addPlot(title="Altitude")
        curve1 = p1.plot(pen='y')
        curve2 = p2.plot(pen='y')
        curve3 = p3.plot(pen='y')
        curve= [curve1,curve2,curve3]
        x_np = []
        lon_np = []
        lat_np = []
        alt_np = []
        q = self.msgq
        t0 = time.time()


        def updateInProc(curve, q, t0, x, lon, lat, alt):
            if not q.empty():
                item = q.get()

                curve1,curve2,curve3 = curve
                # item = q.get()
                # print(item)

                x.append(item['time']-t0)
                lon.append(item["lon"])
                lat.append(item["lat"])
                alt.append(item["height"]/1000)
                if len(x)/10 >= 100:
                    x.pop(0)  # Remove the first x element.
                    lon.pop(0)  # Remove the first y element
                    lat.pop(0)  # Remove the first y element
                    alt.pop(0)  # Remove the first y element
                curve1.setData(x, lon)
                curve2.setData(x, lat)
                curve3.setData(x, alt)


        timer = QtCore.QTimer()
        timer.setInterval(50)
        timer.timeout.connect(lambda: updateInProc(curve, q, t0, x_np, lon_np, lat_np, alt_np))
        timer.start(5)
        win.show()
        a = QtGui.QApplication.instance().exec_()

        while True:
            if a == 0:
                self.stop_program = True
                self.semaphore.release()
                break
            pass
