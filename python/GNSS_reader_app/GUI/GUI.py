import PySimpleGUI as sg
from multiprocessing import Queue
import threading

from Threads.GNSS_Reader import GNSSThread
from Threads.PlotThread import PlotThread
import time
from os.path import exists
from os import remove

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
avg_position_file  = "uśrednienia_pomiaru.txt"

class GUI:
    def __init__(
        self,
        gnss_base_config,
        qmaxsize: int = 100,
        ):
        # threads params
        self.msgq = Queue(maxsize = qmaxsize)
        self.msgq2 = Queue(maxsize = qmaxsize)
        self.semaphore = threading.Semaphore(value=1)
        self.stop_program = False
        self.plots = False
        # GUI layaout
        self.layout_column1 = [
            [sg.Text('GNSS-Readout')],
            [sg.Button('Zatrzymaj odczyt'), sg.Button('Zmień parametry portu', enable_events=True)],
        ]

        headings = ["ID", "  lat [deg]  ", "  lon [deg]  ", "  alt [m]  "]

        self.layout_column2 = [
            [sg.Text('Czas [s]'),
             sg.In(size=(20, 1), enable_events=True, key=3),
            sg.Button('Start uśredniania'),sg.Text(' ',key=7),
            sg.Button('Wykresy')],
            [sg.Text("\t\t\t\t\tlat [deg]   lon [deg]    alt[m]")],
            [sg.Text('ID'), sg.In(size=(15, 1), key=5),
             sg.Button("Dodaj do listy"),
             sg.Text(" ",key=4)],
            [sg.Table(values=[],
                      headings=headings,
                      max_col_width=45,
                      key='-TABLE-',
                      row_height=40,
                      tooltip="Contacts Table")],
            [sg.Text('ścieżka pliku wynikowego')],
            [sg.In(size=(50, 1), key=6),
             sg.FileBrowse(file_types=(("Text Files", "*.txt"),)),
             sg.Button("Zapisz"),
             sg.Button('Zamknij')],
            [sg.Multiline(size=(45,5), key='-MULTILINE-')]
        ]

        # ------------------ full layout --------------------
        # self.layout = [
        #     [sg.Column(self.layout_column1),
        #      sg.VSeparator(),
        #      sg.Column(self.layout_column2)
        #      ]
        # ]
        self.layout = self.layout_column2
        # ---------------------------------------------------

        gnss_base_config = self.change_port(gnss_base_config)
        # start pomiaru z serial portu
        if not self.stop_program:
            self.gnss_thread_base = self.start_GNSS_reader(self.msgq,self.msgq2,self.semaphore, gnss_base_config)
            # start wykresów
            self.gnss_thread_plot_base = self.start_GNSS_plots(self.msgq2,self.semaphore,self.plots)

            # print("aktywne wątki", threading.activeCount())
            self.start_mainGUI()

    # ---------------------------------------------------

    def change_port(self, gnss_base_config):
        self.layout2 = []
        self.layout2 = [
            [sg.Text('COM'), sg.In(gnss_base_config['serial_port'],size=(20, 1), enable_events=True, key=1)],
            [sg.Text('Prędkość transmisji'), sg.Spin([gnss_base_config['baudrate'],9600, 19200,38400,
                                                      57600,115200,460800, 4800,], s=(15,2), key=2)],
            [sg.Button("Zatwierdź")]
        ]

        self.running = False  # flag of working serial port

        self.window2 = sg.Window('Final version', layout=self.layout2, finalize=True)
        while True:
            event, values = self.window2.read(timeout=400)
            if event == "Zatwierdź":
                self.port = str(values[1])
                self.baudrate = values[2]
                self.running = True
                gnss_base_config['serial_port'] = self.port
                gnss_base_config['baudrate'] = self.baudrate
                break
            elif event == sg.WIN_CLOSED:
                self.stop_program = True
                break
        self.window2.Close()
        return gnss_base_config


    def get_serial_port_data(self):
        return self.port, self.baudrate


    def start_GNSS_reader(self,  msgq : Queue, msgq2 : Queue, semaphore, config : dict) -> threading.Thread:
        if self.running == True:
            print(f"\nInitializing GNSS thread for {config['device']}")

            gnss_thread = GNSSThread(
                msgq = msgq,
                msgq2 = msgq2,
                semaphore =semaphore,
                start_time=time.time(),
                **config
            )
            print(f"Starting GNSS thread for {config['device']}")
            gnss_thread.start()

            return gnss_thread

    def start_GNSS_plots(self, msgq:Queue,semaphore, stop_program:bool) ->threading.Thread:
        print(f"\nInitializing GNSS plots")
        plot_thread = PlotThread(
            msgq = msgq,
            stop_program = stop_program,
            semaphore = semaphore,
            start_time=time.time(),
        )
        print(f"Starting GNSS plotting thread")
        self.plots = True
        plot_thread.start()
        return plot_thread

    def check_status(self):

        on_off_color = lambda x : '\033[32mON\033[39m' if x else '\033[31mOFF\033[39m'

        print(
        f"GNSS BASE:\t{on_off_color(self.gnss_thread_base.is_alive())}\n\
        ")

    def start_mainGUI(self):
        avg_flag = 0
        avg_done_flag = 0
        save_flag = 0
        counter = 0
        out_tab = []
        position = [[0],[0], [0], [0]]

        self.window = sg.Window('Final version', layout=self.layout, location=(0, 0), finalize=True)
        while True:
            print(self.semaphore._value)
            print("aktywne wątki", threading.activeCount())
            if not self.msgq.empty():
                self.last_msgq = self.msgq.get()
                if avg_flag == 1:
                    if (self.last_msgq['time'] - t0) < N:
                        self.window['-MULTILINE-'].print(round(self.last_msgq['time'] - t0,2))
                        counter += 1
                        position[1][0] += self.last_msgq['lat']
                        position[2][0] += self.last_msgq['lon']
                        position[3][0] += self.last_msgq['height'] / 1000

                    else:
                        self.window['-MULTILINE-'].print(f"uśredniono tyle liczb : {counter}")
                        position[1][0] /= counter
                        position[2][0] /= counter
                        position[3][0] /= counter
                        self.window[4].update(f'  {position[1][0]}  {position[2][0]}  {position[3][0]}')
                        avg_flag = 0
                        avg_done_flag = 1

            event, values = self.window.read(timeout=10)
            # ---------------------------------------------------
            if event == sg.WIN_CLOSED or event == 'Zamknij':
                self.window['-MULTILINE-'].print("koniec")
                self.stop_program = True
                break

            elif event == "Start uśredniania" and values[3]:
                t0 = time.time()
                if exists(avg_position_file):
                    remove(avg_position_file)
                N = int(values[3])  # czas uśredniania
                position = [[0], [0], [0], [0]]
                avg_flag = 1
                counter = 0
                self.window['-MULTILINE-'].print("Rozpoczęto tryb uśredniania")

            elif event == 'Dodaj do listy' and avg_done_flag == 1:
                if values[5] != '':
                    position[0][0] = values[5]
                    out_tab.append(position)
                    self.window['-TABLE-'].update(out_tab)
                    avg_done_flag = 0
                    save_flag = 1
                    self.window['-MULTILINE-'].print("Dodano do listy")

            elif event == 'Zapisz' and save_flag == 1:
                if values[6] != '':
                    path = values[6]
                    f = open(path, 'a')
                    for data in out_tab:
                        string = ",".join(str(j[0]) for j in data) + " "
                        f.writelines(string + '\n')
                    f.close()
                    save_flag = 0
                    self.window['-MULTILINE-'].print("Zapisano")
                else:
                    self.window['-MULTILINE-'].print("Brak ścieżki do pliku!")
            elif event == 'Wykresy':
                if self.semaphore._value == 1:
                    self.gnss_thread_plot_base = self.start_GNSS_plots(self.msgq2,self.semaphore,self.plots)






