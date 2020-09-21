import time
import json
import random
import math
import os
import errno
import threading
from socket import *
from Modules.Sub.StateController import StateController
from Modules.Sub.ProfileGenerator import ProfileGenerator
from Modules.Sub.Message import Message


class Communicator(object):
    def __init__(self, bioair_params, receiver_queue, sender_queue, receiver_lock, sender_lock):
        self.my_node_id = bioair_params.get('CNP').node_id
        self.position_x = bioair_params.get('CNP').position_x
        self.position_y = bioair_params.get('CNP').position_y
        self.position_z = bioair_params.get('CNP').position_z
        self.radio_range = bioair_params.get('CNP').radio_range

        self.sender_queue = sender_queue
        self.receiver_queue = receiver_queue
        self.sender_lock = sender_lock
        self.receiver_lock = receiver_lock

        self.max_msg_length = bioair_params.get('SHP').max_msg_length

        self.node_status = {}

        my_ip = bioair_params.get('CNP').ip
        my_port = bioair_params.get('CNP').port

        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.__sock.setblocking(0)
        self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.__sock.bind((my_ip, my_port))

        self.__state_controller = StateController()
        self.__profile_generator = ProfileGenerator()

    def __message_handling(self):
        while True:
            try:
                data, addr = self.__sock.recvfrom(self.max_msg_length)
                if data:
                    try:
                        self.__message_receiver(data)
                    except Exception as e1:
                        time_str = time.strftime("%Y%m%d-%H%M%S")
                        try:
                            log_directory = f'{os.getcwd()}/logs'
                            if not (os.path.isdir(log_directory)):
                                os.makedirs(os.path.join(log_directory))
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                print("Failed to create directory !")
                                raise

                        with open(f'{os.getcwd()}/logs/node_{self.my_node_id}.err', 'a') as f:
                            log = f'{time_str}\nError in \'message_receiver\' - {e1}\n'
                            f.write(log)
            except Exception as e:
                pass
            finally:
                time.sleep(0.1 + 0.001 * random.random())

    def __message_receiver(self, data):
        """
        Receive the message and update the self.node_status
        :param data:
        :return:
        """
        adj_node = self.__message_parser(data)

        if adj_node.get('node_signal') == -9999:
            return

        if adj_node.get('node_id') != self.my_node_id:
            self.receiver_lock.acquire()
            self.receiver_queue.put(adj_node)
            self.receiver_lock.release()

    def __message_parser(self, data):
        """
        Parse the information from the message packet
        :param data: received data packet
        :return: parsed information
        """
        data = json.loads(data.decode())

        adj_data = {
            'node_mac': data.get('node_mac'),
            'node_id': data.get('node_id'),
            'node_state': data.get('node_state'),
            'node_position_x': data.get('node_position_x'),
            'node_position_y': data.get('node_position_y'),
            'node_position_z': data.get('node_position_z'),

            'tentacle_id': data.get('tentacle_id'),
            'tentacle_state': data.get('tentacle_state'),

            'tentacle_within_pos': data.get('tentacle_within_pos'),

            'extra_on_tentacle': data.get('extra_on_tentacle'),
            'reinforce_on_tentacle': data.get('reinforce_on_tentacle'),

            'real_target_detection': data.get('real_target_detection'),
            'real_target_position_x': data.get('real_target_position_x'),
            'real_target_position_y': data.get('real_target_position_y'),
            'real_target_position_z': data.get('real_target_position_z'),

            'origin_connection': data.get('origin_connection'),
            'dest_connection': data.get('dest_connection'),

            'is_anchored': data.get('is_anchored'),
            'is_reinforced': data.get('is_reinforced'),

            'anchoring': data.get('anchoring'),
            'reinforcing': data.get('reinforcing'),

            'global_count': data.get('global_count'),

            'node_signal': self.__get_signal_quality(data.get('node_mac'),
                                                     data.get('node_position_x'),
                                                     data.get('node_position_y'),
                                                     data.get('node_position_z')),
            'node_last_connection_time': time.time(),
            'has_sensor': data.get('has_sensor'),

            'virtual_target': data.get('virtual_target'),
            'virtual_target_position_x': data.get('virtual_target_position_x'),
            'virtual_target_position_y': data.get('virtual_target_position_y'),
            'virtual_target_position_z': data.get('virtual_target_position_z'),
        }
        return adj_data

    def __get_signal_quality(self, node_mac, node_position_x, node_position_y, node_position_z):
        """
        Get signal quality of a node
        :param node_mac: Adjacent Node's mac address
        :param node_position_x: Adjacent Node's x coordinate
        :param node_position_y: Adjacent Node's y coordinate
        :param node_position_z: Adjacent Node's z coordinate
        :return:
        """
        # CORE - Based on Distance
        rx_signal = math.sqrt(
            (self.position_x - node_position_x) ** 2 + (self.position_y - node_position_y) ** 2 + (
                    self.position_z - node_position_z) ** 2)

        if rx_signal < self.radio_range:
            # rxSignal = 50 - (10 * math.log(rxSignal/4))
            rx_signal = 1 - (rx_signal / self.radio_range)
        else:
            rx_signal = -9999

        # Real - Based on RSSI
        #     check_signal_cmd = f'iw dev {self.__nt_int} station get {node_mac} | grep signal: | grep -oE ([-]{{1}}[0-9]*){{1}}'
        #     result = os.popen(check_signal_cmd).read()
        #
        #     if result == '':
        #         rxSignal = UNKNOWN
        #
        #     else:
        #         rxSignal = int(result.strip().split('\n')[0])
        #         rxSignal = 1.0 + (rxSignal / 101)
        return rx_signal

    def __message_sender(self):
        """
        Send my node_status
        :return:
        """
        while True:
            if not self.sender_queue.empty():
                my_status = self.sender_queue.get()

                self.position_x = my_status.get('position_x')
                self.position_y = my_status.get('position_y')
                self.position_z = my_status.get('position_z')

                connection_info_list = []
                for i in range(1, 10):
                    connection_info_list.append(('127.0.0.1', int('1080' + i)))

                message = Message(my_status)

                for info in connection_info_list:
                    self.__sock.sendto(message.get_json_format().encode(), info)

    def start(self):
        receiver_thread = threading.Thread(target=self.__message_handling,
                                           args=(),
                                           daemon=True)
        sender_thread = threading.Thread(target=self.__message_sender,
                                         args=(),
                                         daemon=True)

        receiver_thread.start()
        sender_thread.start()
