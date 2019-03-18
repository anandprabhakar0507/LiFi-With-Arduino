from fsm import Receiver

# Threading Imports
import time
import queue
import threading


class ThreadManager:
        def __init__(self, fsm, in_queue, gui):
                self.__fsm = fsm
                self.__my_queue = in_queue
                self.__gui = gui

                self.__running = 1
                self.__thread1 = threading.Thread(target=self.workerThread1)
                self.__thread1.start()

                self.__first_flag = 1

                self.periodicCall()

        @property
        def fsm(self):
                return self.__fsm

        @property
        def my_queue(self):
                return self.__my_queue

        @property
        def gui(self):
                return self.__gui

        @property
        def running(self):
                return self.__running

        @running.setter
        def running(self, val):
                self.__running = val

        @property
        def thread1(self):
                return self.__thread1

        @property
        def first_flag(self):
                return self.__first_flag

        @first_flag.setter
        def first_flag(self, val):
                self.__first_flag = val

        def periodicCall(self):
                self.gui.threadProcessor()
                if not self.running:
                        # This is the brutal stop of the system. You may want to do
                        # some cleanup before actually shutting it down.
                        import sys
                        sys.exit(1)
                self.gui.window.after(200, self.periodicCall)

        # TODO: Check serial.read() here
        def workerThread1(self):
                while self.running:
                        if self.gui.serialPort.isOpen():
                                bytes_ready = self.gui.serialPort.in_waiting
                        else:
                                bytes_ready = 0
                        if bytes_ready > 0 and isinstance(self.fsm.state, Receiver):
                                if self.first_flag == 1:
                                        self.my_queue.put("meta")
                                        self.first_flag = 0
                                else:
                                        pass
                        else:
                                pass