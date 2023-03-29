import threading
from multiprocessing import Queue
from threading import Thread
from Threads.GNSS_Reader import GNSSThread
from Threads.PlotThread import PlotThread#, GUIThread
import time
from GUI.GUI import GUI

class ThreadManager:
    def __init__(
        self,
        gnss_base_config,
        qmaxsize: int = 100,
        ):

        self.msgq = Queue(maxsize = qmaxsize)

        self.gnss_thread_base = self.start_GNSS_reader(self.msgq, gnss_base_config)
        self.gnss_thread_plot_base = self.start_GNSS_plots(self.msgq)
        # self.gnss_thread_gui = self.start_GUI(self.msgq2)

    def check_status(self):

        on_off_color = lambda x : '\033[32mON\033[39m' if x else '\033[31mOFF\033[39m'

        print(
        f"GNSS BASE:\t{on_off_color(self.gnss_thread_base.is_alive())}\n\
        ")

    def start_GNSS_reader(self,  msgq : Queue, config : dict) -> threading.Thread:
        print(f"\nInitializing GNSS thread for {config['device']}")

        gnss_thread = GNSSThread(
            msgq = msgq,
            start_time=time.time(),
            **config
        )
        print(f"Starting GNSS thread for {config['device']}")
        gnss_thread.start()
        return gnss_thread


    def start_GNSS_plots(self, msgq:Queue) ->threading.Thread:
        print(f"\nInitializing GNSS plots")
        plot_thread = PlotThread(
            msgq = msgq,
            start_time=time.time()
        )
        print(f"Starting GNSS plotting thread")
        plot_thread.start()
        return plot_thread


    # def start_GUI(self, msgq2:Queue) ->threading.Thread:
    #     print(f"\nInitializing GUI")
    #     gui_thread = GUIThread(
    #         msgq2 = msgq2,
    #         start_time=time.time()
    #     )
    #     print(f"Starting GUI thread")
    #     gui_thread.start()
    #     return gui_thread
