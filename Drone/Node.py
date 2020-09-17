import threading
import pickle
import os
from Params.SystemHyperParams import SystemHyperParams
from Params.ConfigurableNodeParams import ConfigurableNodeParams
from Params.SituationDecisionParams import SituationDecisionParams
from Modules.Communicator import Communicator
from Modules.Motion import Motion


class Node(object):
    def __init__(self, run_mode=None, node_id=None, load_option=0, write_option=0):
        # 주위 노드들의 정보를 담는다.
        self.__node_status = {}
        # ?
        self.__node_signal = {}
        self.__write = write_option

        # node_n_CNP config 가져오기
        self.__configurable_node_params = ConfigurableNodeParams("node_" + node_id + "_CNP.ini", load_option)
        # node_n_SHP config 가져오기
        self.__system_hyper_params = SystemHyperParams("node_" + node_id + "_SHP.ini", load_option)
        # node_n_SDP config 가져오기
        self.__situation_decision_params = SituationDecisionParams("node_" + node_id + "_SDP.ini", load_option)

        # 가져온 config를 기준으로 Communicator 클래스 생성
        self.__communicator = Communicator(self.__system_hyper_params,
                                           self.__situation_decision_params,
                                           self.__configurable_node_params,
                                           self.__node_status,
                                           self.__node_signal)

        # Generate the Motion Class
        self.__motion = Motion()

        #  Start the Communicator Thread
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
                self.__system_hyper_params.save(f"node_{node_id}_SHP.ini")
                self.__configurable_node_params.save(f"node_{node_id}_CNP.ini")
                self.__situation_decision_params.save(f"node_{node_id}_SDP.ini")
                cmd = f"coresendmsg -a 127.0.0.1 NODE NUMBER={node_id} X_POSITION=9999 Y_POSITION=9999"
                os.popen(cmd)


if __name__ == '__main__':
    node_1 = Node(run_mode="CORE", node_id="1", load_option=0)
    node_1.run()
