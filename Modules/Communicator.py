import time
import json
import random
import math
import os
import errno
from socket import *
from Modules.Sub.StateController import StateController
from Modules.Sub.ProfileGenerator import ProfileGenerator
from Modules.Sub.Message import Message
from Drone.State import NodeState, TentacleState
import threading


class Communicator(object):
    def __init__(self, bioair_params, receiver_queue, sender_queue, receiver_lock, sender_lock):
        self.node_params = bioair_params.get('CNP')
        self.situation_params = bioair_params.get('SDP')
        self.hyper_params = bioair_params.get('SHP')

        self.sender_queue = sender_queue
        self.receiver_queue = receiver_queue
        self.sender_lock = sender_lock
        self.receiver_lock = receiver_lock

        self.node_signal = {}
        self.node_status = {}

        my_ip = self.node_params.ip
        my_port = self.node_params.port

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
                data, addr = self.__sock.recvfrom(self.hyper_params.max_msg_length)
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

                        with open(f'{os.getcwd()}/logs/node_{self.node_params.node_id}.err', 'a') as f:
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
        my_node_id = self.node_params.node_id

        adj_node = self.__message_parser(data)

        node_last_connection_time = time.time()

        if adj_node.get('node_signal') == -9999:
            return

        if adj_node.get('node_id') != my_node_id:
            self.__update_node_status(adj_node, node_last_connection_time)

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
        my_position_x = self.node_params.position_x
        my_position_y = self.node_params.position_y
        my_position_z = self.node_params.position_z
        radio_range = self.node_params.radio_range

        rx_signal = math.sqrt(
            (my_position_x - node_position_x) ** 2 + (my_position_y - node_position_y) ** 2 + (
                    my_position_z - node_position_z) ** 2)

        if rx_signal < radio_range:
            # rxSignal = 50 - (10 * math.log(rxSignal/4))
            rx_signal = 1 - (rx_signal / radio_range)
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
                connection_info_list = []
                for i in range(1, 10):
                    connection_info_list.append(('127.0.0.1', int('1080' + i)))
                message = Message(my_status)
                for info in connection_info_list:
                    self.__sock.sendto(message.get_json_format().encode(), info)

    def __update_node_status(self, adj_node, node_last_connection_time):
        """
        Store the signal and other data from an adjacent node
        :param adj_node: Adjacent Node's data
        :param node_last_connection_time:
        :return:
        """
        node_id = adj_node.get('node_id')

        if node_id in self.node_status.keys():
            cnt_signal = self.node_status[node_id]['cnt_signal']
            self.node_status.get(node_id)['node_signal'] += adj_node.get('node_signal')

            if cnt_signal == self.hyper_params.average_sample:
                self.node_status.get(node_id)['node_signal'] /= self.hyper_params.average_sample
                self.node_status.get(node_id)['node_last_connection_time'] = node_last_connection_time
                self.node_status.get(node_id)['cnt_signal'] = 0
                self.node_status.get(node_id).update(adj_node)

                self.sender_lock.acquire()
                self.sender_queue.put(node_id)
                self.sender_queue.put(self.node_status.get(node_id))
                self.sender_lock.release()
            else:
                self.node_status[node_id]['cnt_signal'] += 1
        else:
            if not (adj_node.get('node_state') == NodeState.Origin
                    or adj_node.get('node_state') == NodeState.Destination):
                self.node_status.update({node_id: adj_node})
                self.node_status[node_id]['cnt_signal'] = 1
                self.node_status[node_id]['node_last_connection_time'] = node_last_connection_time

    def start(self):
        receiver_thread = threading.Thread(target=self.__message_handling,
                                           args=(),
                                           daemon=True)
        sender_thread = threading.Thread(target=self.__message_sender,
                                         args=(),
                                         daemon=True)

        receiver_thread.start()
        sender_thread.start()

    def __state_update(self, hyper_params, situation_params, node_params,
                       my_node_status, my_node_signal):
        '''
        state control
        '''
        if node_params.virtual_target > 0:
            next_tentacle_state, next_node_state = self.__state_controller.virtual_origin_mode_state_manage(
                hyper_params, situation_params, node_params, my_node_status)
            node_params.tentacle_state = next_tentacle_state
            node_params.node_state = next_node_state
            return 0

        if (node_params.node_state is NodeState.Origin or node_params.node_state is NodeState.Destination):
            return 0

        if (self.__state_controller.check_orphan_conditions(hyper_params, situation_params, node_params)):
            situation_params.hold_timer = 0
            situation_params.hold = False
            node_params.node_state = NodeState.Orphan
            return 0
        if (self.__state_controller.check_damaged_conditions(hyper_params, situation_params, node_params)):
            node_params.tentacle_state = TentacleState.Damaged
            situation_params.hold = True
            situation_params.hold_timer = time.time()
            print(f"hold_timer : {situation_params.hold_timer}")
            return 0

        next_tentacle_state, next_node_state, = self.__state_controller.get_next_state(hyper_params, situation_params,
                                                                                       node_params, my_node_status)
        node_params.tentacle_state = next_tentacle_state
        node_params.node_state = next_node_state
        return 0

    def __calculate_profile_and_update_situation_params(self, hyper_params, situation_params, node_params,
                                                        my_node_status, my_node_signal):
        # print(my_node_status)
        vel_x, vel_y = 0, 0  # next x,y velocity
        o_x, o_y = 0, 0  # used for chekcing whether current position is good for tentacle
        add_x, add_y = 0, 0  # x,y velocity based nearby nodes
        adj_origin, adj_dest, adj_tip, adj_backbone, adj_free, adj_virtual_origin = 0, 0, 0, 0, 0, 0  # number of nearby nodes type
        next_attractor = -1  # position within a tentacle
        adjTipNodes = []
        new_adj_nodes = []
        my_state = node_params.node_state
        my_anchoring = situation_params.anchoring
        my_global_count = situation_params.global_count
        max_tentacle_within_pos = situation_params.tentacle_within_pos
        min_tentacle_within_pos = situation_params.tentacle_within_pos if situation_params.tentacle_within_pos != -9999 else 9999

        globalNodesId = list(my_node_status.keys())

        if not (my_state is NodeState.Origin or my_state is NodeState.Destination):
            if node_params.node_state is NodeState.Orphan:
                virtx, virty = self.__profile_generator.generate_origin_profile(hyper_params, situation_params,
                                                                                node_params,
                                                                                my_node_status, my_node_signal)
            else:
                virtx, virty = self.__profile_generator.generate_destination_profile(hyper_params, situation_params,
                                                                                     node_params,
                                                                                     my_node_status, my_node_signal)

            if node_params.virtual_target > 0:
                virtx = virtx / 2
                virty = virty / 2

            vel_x, vel_y = virtx, virty
            print(f'virtx : {virtx}, virty : {virty}')
            next_attractor = self.__get_further_node_on_same_tentacle(hyper_params, situation_params, node_params,
                                                                      my_node_status, globalNodesId)
            print(f'next_attractor : {next_attractor}')
            for node_id in globalNodesId:
                node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
                tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
                real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                origin_connection, dest_connection, \
                is_anchored, is_reinforced, anchoring, reinforcing, \
                global_count, \
                virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(
                    hyper_params, situation_params, node_params, node_id, my_node_status)

                max_tentacle_within_pos = tentacle_within_pos if max_tentacle_within_pos < tentacle_within_pos else max_tentacle_within_pos
                if tentacle_within_pos != -9999:
                    min_tentacle_within_pos = tentacle_within_pos if min_tentacle_within_pos > tentacle_within_pos else min_tentacle_within_pos

                # Release any reinforcement node that does not hear from its anchor
                if node_signal == -9999:
                    continue

                if node_state is not NodeState.Destination and node_state is not NodeState.Origin and node_state is not NodeState.Orphan:
                    if global_count > my_global_count:
                        if (origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if (dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        # damaged 쪽이 global count 더 큰데 tentacle state 받아오면 또 다시 damaged 되버림
                        if node_params.node_state is NodeState.Free and situation_params.reinforcing != -9999:
                            situation_params.reinforcing = -9999

                        elif (tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        situation_params.global_count = global_count

                    if node_params.node_state is NodeState.Orphan and node_params.tentacle_state is TentacleState.Damaged:
                        if (origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if (dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        if (tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        if global_count > my_global_count:
                            situation_params.global_count = global_count

                if node_state is NodeState.Orphan and node_params.node_state is NodeState.Orphan:
                    if global_count > my_global_count:
                        if (origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if (dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        if (tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        situation_params.global_count = global_count

                add_x, add_y = self.__profile_generator.generate_ra_profile(hyper_params, situation_params, node_params,
                                                                            node_state, node_signal, node_position_x,
                                                                            node_position_y, tentacle_within_pos)

                print(f'add_x : {add_x} add_y : {add_y} from node_id : {node_id}, node_state {NodeState(node_state)}')

                if node_state is NodeState.Destination:
                    # Check tx_node is current destination
                    if (node_id == node_params.dest_id):
                        adjTipNodes.append(node_id)
                        new_adj_nodes.append(node_id)
                        adj_dest += 1
                    if node_params.node_state is not NodeState.Orphan:

                        vel_x += add_x
                        vel_y += add_y
                        vel_x -= virtx
                        vel_y -= virty

                        if my_state is NodeState.Extra:
                            pass

                elif node_state is NodeState.Origin:
                    adj_origin += 1
                    adjTipNodes.append(node_id)
                    new_adj_nodes.append(node_id)
                    if next_attractor < 0 or situation_params.tentacle_within_pos == 0:
                        if node_params.virtual_target == -1 or node_params.virtual_target == 0:
                            vel_x += add_x
                            vel_y += add_y

                    if my_state is NodeState.Tip or my_state is NodeState.Backbone:
                        o_x += add_x
                        o_y += add_y

                    # When Orphan node found Origin node
                    elif my_state is NodeState.Orphan:
                        pass
                    # The extranode has returned from a full tour, so repeat patrol
                    # Extra mode ??
                    if my_state is NodeState.Extra and node_id == node_params.dest_id:
                        pass

                elif node_state is NodeState.Tip:
                    adj_tip += 1
                    adjTipNodes.append(node_id)
                    new_adj_nodes.append(node_id)

                    if my_state != NodeState.Tip and my_state != NodeState.Backbone:
                        vel_x += add_x
                        vel_y += add_y

                        # if my_state is NodeState.Free and adj_origin == 1 and adj_tip == 1 and adj_backbone == 0 and adj_free == 0 and adj_dest == 0:
                        #     # 자기가 reinforcing 하던 backbone이 터졌는데 그게 첫번째 백본이였던 경우 free 노드가 두번째 백본이였던 팁노드 한테 힘을 너무 많이 받아서 예외 걸어놓음
                        #     vel_x -= add_x
                        #     vel_y -= add_y

                elif node_state is NodeState.Backbone:

                    new_adj_nodes.append(node_id)

                    if node_params.node_state is NodeState.Extra and situation_params.anchoring == -9999:
                        if is_anchored == hyper_params.unknown and is_reinforced == hyper_params.unknown:
                            situation_params.anchoring = node_id

                    if node_params.tentacle_id >= tentacle_id:
                        adj_backbone += 1

                    condi = (
                            my_state is NodeState.Tip or my_state is NodeState.Backbone)

                    if condi and situation_params.tentacle_within_pos > tentacle_within_pos:
                        o_x += add_x
                        o_y += add_y

                    if (condi and situation_params.tentacle_within_pos == tentacle_within_pos + 1) or (
                            my_state != NodeState.Backbone and tentacle_id <= node_params.tentacle_id and tentacle_within_pos == next_attractor) or my_state is NodeState.Reinforce:
                        if situation_params.adj_dest != 1:
                            vel_x += add_x
                            vel_y += add_y

                elif node_state is NodeState.Extra:

                    new_adj_nodes.append(node_id)

                    if my_state is NodeState.Extra or my_state is NodeState.Reinforce:
                        vel_x += add_x
                        vel_y += add_y
                    if node_params.node_state is NodeState.Backbone and situation_params.is_anchored == -9999:
                        if (anchoring == node_params.node_id):
                            situation_params.is_anchored = node_id

                elif node_state is NodeState.Reinforce:

                    new_adj_nodes.append(node_id)

                    if my_state is NodeState.Extra or my_state is NodeState.Reinforce:
                        vel_x += add_x
                        vel_y += add_y

                    if node_params.node_state is NodeState.Backbone and situation_params.is_reinforced == -9999:
                        if (reinforcing == node_params.node_id):
                            situation_params.is_anchored = -9999
                            situation_params.is_reinforced = node_id

                elif node_state is NodeState.Free:
                    adj_free += 1
                    new_adj_nodes.append(node_id)
                    if my_state is NodeState.Free:
                        vel_x += add_x
                        vel_y += add_y

                if virtual_target > 0:
                    if global_count > my_global_count:
                        node_params.virtual_target = virtual_target
                        node_params.virtual_target_position_x = node_position_x
                        node_params.virtual_target_position_y = node_position_y
                        situation_params.global_count = global_count

                if node_id == node_params.virtual_target:
                    adj_virtual_origin += 1
        else:
            for node_id in globalNodesId:
                node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
                tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
                real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                origin_connection, dest_connection, \
                is_anchored, is_reinforced, anchoring, reinforcing, \
                global_count, \
                virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(
                    hyper_params, situation_params, node_params, node_id, my_node_status)

                if node_state is not NodeState.Destination and node_state is not NodeState.Origin and node_state is not NodeState.Orphan:
                    if global_count > my_global_count:
                        situation_params.global_count = global_count

        print(
            f"adj_origin : {adj_origin}, adj_free : {adj_free} ,adj_tip : {adj_tip}, adj_back : {adj_backbone}, adj_dest : {adj_dest}")

        # first detector
        if (adj_origin == 1 and situation_params.origin_connection == False):
            situation_params.origin_connection = True
            situation_params.global_count = situation_params.global_count + 1

        if (adj_dest == 1 and situation_params.dest_connection == False):
            situation_params.dest_connection = True
            situation_params.global_count = situation_params.global_count + 1

        if (adj_dest == 0 and situation_params.adj_dest == 1):
            situation_params.dest_connection = False
            situation_params.global_count = situation_params.global_count + 1

        if node_params.node_state is NodeState.Extra and situation_params.anchoring != hyper_params.unknown:
            if my_node_status[situation_params.anchoring]['node_signal'] > 0.55:
                situation_params.complete_reinforce = situation_params.complete_reinforce + 1

            print(f"situation_params.complete_reinforce : {situation_params.complete_reinforce}")

        if node_params.node_state is NodeState.Backbone:
            if node_params.tentacle_state is not TentacleState.Damaged:
                # condition 9
                backbone_condition = ((adj_origin and adj_tip) or (adj_origin and adj_backbone)) \
                                     or (adj_backbone == 2) \
                                     or (adj_backbone and adj_tip) \
                                     or ((adj_dest and adj_tip) or (adj_dest and adj_backbone)) \
                                     or (adj_dest and adj_origin)

                if backbone_condition == False:
                    adj_backbones = self.__get_adj_backbone_node(new_adj_nodes, my_node_status)
                    if len(adj_backbones) == 0:
                        if adj_origin:
                            situation_params.dest_connection = False
                            situation_params.global_count = situation_params.global_count + 1
                        if adj_dest:
                            situation_params.origin_connection = False
                            situation_params.global_count = situation_params.global_count + 1
                    else:
                        if my_node_status[adj_backbones[0]][
                            'tentacle_within_pos'] > situation_params.tentacle_within_pos:
                            situation_params.origin_connection = False
                            situation_params.global_count = situation_params.global_count + 1
                        if my_node_status[adj_backbones[0]][
                            'tentacle_within_pos'] < situation_params.tentacle_within_pos:
                            situation_params.dest_connection = False
                            situation_params.global_count = situation_params.global_count + 1

        if node_params.node_state is NodeState.Reinforce:
            if adj_origin == 1 and adj_backbone == 0:
                situation_params.dest_connection = False
            if adj_dest == 1 and adj_backbone == 0:
                situation_params.origin_connection = False

        if node_params.virtual_target > 0 and node_params.node_id == node_params.virtual_target:
            add_x, add_y = self.__profile_generator.generate_virtual_target_profile(hyper_params, situation_params,
                                                                                    node_params,
                                                                                    my_node_status, my_node_signal)
            vel_x += add_x
            vel_y += add_y

        if node_params.virtual_target == 0:
            if node_params.node_state is not NodeState.Origin and node_params.node_state is not NodeState.Destination:
                add_x, add_y = self.__profile_generator.generate_virtual_target_profile(hyper_params, situation_params,
                                                                                        node_params,
                                                                                        my_node_status, my_node_signal)
                vel_x += add_x
                vel_y += add_y

        if situation_params.adj_virtual_origin == 1 and adj_virtual_origin == 0:
            situation_params.virtual_origin_trigger = True

        situation_params.adj_nodes = new_adj_nodes
        situation_params.adj_origin = adj_origin
        situation_params.adj_dest = adj_dest
        situation_params.adj_tip = adj_tip
        situation_params.adj_backbone = adj_backbone
        situation_params.adj_free = adj_free
        situation_params.adj_virtual_origin = adj_virtual_origin
        situation_params.next_attractor = next_attractor
        node_params.prev_vel_x = node_params.next_vel_x
        node_params.prev_vel_y = node_params.next_vel_y
        node_params.next_vel_x = vel_x
        node_params.next_vel_y = vel_y
        print(f'node_next_vel_x : {node_params.next_vel_x}', f'node_next_vel_y : {node_params.next_vel_y}')

        if math.sqrt(vel_x ** 2 + vel_y ** 2) < node_params.equilibrium_zone:
            situation_params.equilibrium = situation_params.equilibrium + 1
        else:
            situation_params.equilibrium = 0

    def __get_node_status(self, hyper_params, situation_params, node_params,
                          node_id, my_node_status):
        '''
        :return: the information needed for Bioair algorithm
        '''
        node_status = my_node_status[node_id]
        node_state = node_status['node_state']
        node_position_x = node_status['node_position_x']
        node_position_y = node_status['node_position_y']
        tentacle_id = node_status['tentacle_id']
        tentacle_within_pos = node_status['tentacle_within_pos']
        node_last_connection_time = node_status['node_last_connection_time']

        tentacle_state = node_status['tentacle_state']
        extra_on_tentacle = node_status['extra_on_tentacle']
        reinforce_on_tentacle = node_status['reinforce_on_tentacle']
        real_target_detection = node_status['real_target_detection']
        real_target_position_x = node_status['real_target_position_x']
        real_target_position_y = node_status['real_target_position_y']
        real_target_position_z = node_status['real_target_position_z']
        origin_connection = node_status['origin_connection']
        dest_connection = node_status['dest_connection']
        is_anchored = node_status['is_anchored']
        is_reinforced = node_status['is_reinforced']
        anchoring = node_status['anchoring']
        reinforcing = node_status['reinforcing']
        global_count = node_status['global_count']

        virtual_target = node_status['virtual_target']
        virtual_target_position_x = node_status['virtual_target_position_x']
        virtual_target_position_y = node_status['virtual_target_position_y']
        virtual_target_position_z = node_status['virtual_target_position_z']

        COMMSTIMEOUT = hyper_params.commstimeout
        UNKNOWN = hyper_params.unknown

        if time.time() - node_last_connection_time < COMMSTIMEOUT:
            node_signal = node_status['node_signal']
        else:
            node_signal = UNKNOWN

        return node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
               tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
               real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
               origin_connection, dest_connection, \
               is_anchored, is_reinforced, anchoring, reinforcing, \
               global_count, \
               virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z

    def __get_further_node_on_same_tentacle(self, hyper_params, situation_params, node_params,
                                            my_node_status, globalNodesId):
        '''
            Get furthest node on same tentacle to arrive Tip position
        '''
        next_attractor = -1
        UNKNOWN = hyper_params.unknown
        my_node_state = node_params.node_state
        my_tentacle_id = node_params.tentacle_id

        for node_id in globalNodesId:
            node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
            tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
            real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
            origin_connection, dest_connection, \
            is_anchored, is_reinforced, anchoring, reinforcing, \
            global_count, \
            virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(
                hyper_params, situation_params, node_params, node_id, my_node_status)

            if node_signal != UNKNOWN:
                # 상대가 tentacle, tip이거나 상대가 backbone일때, 내가 텐타클 id가 더 큰경우 && 상대가 현재 atrractor보다 먼 경우
                if (node_state is NodeState.Tip or
                    (node_state is NodeState.Backbone and my_tentacle_id >= tentacle_id)) and (
                        tentacle_within_pos >= next_attractor):
                    next_attractor = tentacle_within_pos

                elif node_state is NodeState.Backbone and (
                        my_node_state is NodeState.Extra and tentacle_within_pos >= next_attractor):
                    next_attractor = tentacle_within_pos

        return next_attractor

    def __get_adj_backbone_node(self, adj_nodes, my_node_status):
        adj_backbones = [node_id for node_id in adj_nodes if
                         my_node_status[node_id]['node_state'] is NodeState.Backbone]
        return adj_backbones
