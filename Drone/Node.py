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

        self.bioair_params = {
            'CNP': self.__parser.configurable_node_params,
            'SDP': self.__parser.situation_decision_params,
            'SHP': self.__parser.system_hyper_params
        }

        self.__node_status_queue = Queue(maxsize=1)
        lock = threading.Lock()

        self.__communicator = Communicator(self.bioair_params, self.__node_status_queue, lock)
        self.__motion = Motion(self.__node_status_queue, lock)

        self.__comm_thread = threading.Thread(target=self.__communicator.communication,
                                              args=(),
                                              daemon=True)
        self.__motion_thread = threading.Thread(target=self.__motion.move_command,
                                                args=(),
                                                daemon=True)

    def run(self):
        try:
            self.__comm_thread.start()
            self.__motion_thread.start()

            self.__comm_thread.join()
            self.__motion_thread.join()
            pass
        except:
            pass
        finally:
            if self.__write:
                node_id = self.__bioair_params.get('CNP').node_id
                self.__parser.save()
                cmd = f"coresendmsg -a 127.0.0.1 NODE NUMBER={node_id} X_POSITION=9999 Y_POSITION=9999"
                os.popen(cmd)


if __name__ == '__main__':
    node_1 = Node(run_mode="CORE", node_id="1", load_option=False, write_option=False)
    node_1.run()
