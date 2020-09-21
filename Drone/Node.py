import threading
import os
from Modules.Communicator import Communicator
from Modules.Motion import Motion
from Params.Parser import Parser
from queue import Queue


class Node(object):
    def __init__(self, run_mode=None, node_id=None, load_option=False, write_option=False):
        """
        Load the init files and Make a thread
        :param run_mode: "REAL" mode or "CORE" mode
        :param node_id: The number of node
        :param load_option: True loads the init file from load_file dir, False loads from init_file dir
        :param write_option: True writes the init file in load_file dir, False doesn't write
        """
        self.__write = write_option

        self.__parser = Parser(node_id, load_option)

        self.__bioair_params = {
            'CNP': self.__parser.configurable_node_params,
            'SDP': self.__parser.situation_decision_params,
            'SHP': self.__parser.system_hyper_params
        }

        self.__sender_queue = Queue(maxsize=1)
        self.__receiver_queue = Queue()
        sender_lock = threading.Lock()
        receiver_lock = threading.Lock()

        self.__communicator = \
            Communicator(self.__bioair_params, self.__receiver_queue, self.__sender_queue, receiver_lock, sender_lock)

        self.__motion = Motion(self.__receiver_queue, self.__sender_queue, receiver_lock, sender_lock)
        self.__motion_thread = threading.Thread(target=self.__motion.move_command,
                                                args=(),
                                                daemon=True)

    def run(self):
        try:
            self.__communicator.start()
            self.__motion_thread.start()

            self.__motion_thread.join()
        except OSError as err:
            print("The Error is occured : ", err)
        finally:
            if self.__write:
                node_id = self.__bioair_params.get('CNP').node_id
                self.__parser.save()
                os.popen(f"coresendmsg -a 127.0.0.1 NODE NUMBER={node_id} X_POSITION=9999 Y_POSITION=9999")


if __name__ == '__main__':
    node_1 = Node(run_mode="CORE", node_id="1", load_option=False, write_option=False)
    node_1.run()
