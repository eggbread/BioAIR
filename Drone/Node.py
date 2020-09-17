import threading
import os
from Params.SystemHyperParams import SystemHyperParams
from Params.ConfigurableNodeParams import ConfigurableNodeParams
from Params.SituationDecisionParams import SituationDecisionParams
from Modules.Communicator import Communicator
from Modules.Motion import Motion
from Params.Parser import Parser


class Node(object):
    def __init__(self, run_mode=None, node_id=None, load_option=False, write_option=False):
        """
        Load the init files and Make a thread
        :param run_mode: "REAL" mode or "CORE" mode
        :param node_id: The number of node
        :param load_option: True loads the init file from load_file dir, False loads from init_file dir
        :param write_option: True writes the init file in load_file dir, False doesn't write
        """
        self.__node_status = {}
        self.__node_signal = {}
        self.__write = write_option

        self.__parser = Parser(node_id, load_option)
        self.__configurable_node_params = self.__parser.configurable_node_params
        self.__situation_decision_params = self.__parser.situation_decision_params
        self.__system_hyper_params = self.__parser.system_hyper_params

        self.__communicator = Communicator(self.__system_hyper_params,
                                           self.__situation_decision_params,
                                           self.__configurable_node_params,
                                           self.__node_status,
                                           self.__node_signal)

        self.__motion = Motion()

        self.__comm_thread = threading.Thread(target=self.__communicator.communication, daemon=True,
                                              args=[self.__system_hyper_params,
                                                    self.__situation_decision_params,
                                                    self.__configurable_node_params,
                                                    self.__node_status,
                                                    self.__node_signal,load_option])

        # Start the Motion Thread
        self.__motion_thread = threading.Thread(target=self.__motion.move_command, daemon=True,
                                                args=[self.__system_hyper_params,
                                                      self.__situation_decision_params,
                                                      self.__configurable_node_params])

    def run(self):
        try:
            self.__comm_thread.start()
            self.__motion_thread.start()

            self.__comm_thread.join()
            self.__motion_thread.join()
        except:
            pass
        finally:
            if self.__write:
                node_id = self.__configurable_node_params.node_id
                self.__parser.save()
                cmd = f"coresendmsg -a 127.0.0.1 NODE NUMBER={node_id} X_POSITION=9999 Y_POSITION=9999"
                os.popen(cmd)


if __name__ == '__main__':
    node_1 = Node(run_mode="CORE", node_id="1", load_option=0)
    node_1.run()
