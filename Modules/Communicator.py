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
    def __init__(self, bioair_params, node_status_queue, lock):
        self.params = bioair_params
        self.queue = node_status_queue
        my_ip = self.params.get('CNP').ip
        my_port = self.params.get('CNP').port
        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.__sock.setblocking(0)
        self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.__sock.bind((my_ip, my_port))

        self.__state_controller = StateController()
        self.__profile_generator = ProfileGenerator()

    def __message_receiver(self, hyper_params, node_params, situation_params,
                           my_node_status, my_node_signal, data):
        '''
        Receive message and Update Node_status
        '''
        my_node_id = node_params.node_id

        node_mac, node_id, node_state, node_position_x, node_position_y, node_position_z, \
        tentacle_id, tentacle_state, tentacle_within_pos, \
        extra_on_tentacle, reinforce_on_tentacle, \
        real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
        origin_connection, dest_connection, \
        is_anchored, is_reinforced, anchoring, reinforcing,\
        global_count, \
        node_signal, has_sensor, \
        virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__message_parser(node_params, data)

        print(self.__message_parser(node_params, data))
        node_last_connection_time = time.time()

        if node_signal == -9999:
            return

        if node_id != my_node_id:
            self.__update_node_status(node_id, node_state, node_position_x, node_position_y, node_position_z, node_signal,
                                      tentacle_id, tentacle_state, tentacle_within_pos,
                                      extra_on_tentacle, reinforce_on_tentacle,
                                      real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z,
                                      origin_connection, dest_connection,
                                      is_anchored, is_reinforced, anchoring, reinforcing,
                                      node_last_connection_time,
                                      global_count,
                                      my_node_status, my_node_signal, has_sensor,
                                      virtual_target, virtual_target_position_x, virtual_target_position_y,
                                      virtual_target_position_z,
                                      situation_params, node_params)

            log = f"-- From : {node_mac} / SQ : {node_signal}\n"
            log += f"node_id : {node_id}, node_state : {NodeState(node_state)}, node_position_x : {node_position_x}, node_position_y : {node_position_y}\n"
            log += f"tentacle_id : {tentacle_id}, tentacle_state : {TentacleState(tentacle_state)}, tentacle_within_pos : {tentacle_within_pos}\n"
            log += f"extra_on_tentalce : {extra_on_tentacle}, reinforce_on_tetnacle : {reinforce_on_tentacle}\n"
            log += f"anchoring : {anchoring}, reinforcing : {reinforcing}, is_anchored : {is_anchored}, is_reinforced : {is_reinforced}\n"
            log += f"origin_connection : {origin_connection}, dest_connection : {dest_connection}, global_count : {global_count}\n"
            log += f"has_sensor : {has_sensor}\n"
            print(log)

            # write data to log.file
            timestr = time.strftime("%Y%m%d-%H%M%S")
            try:
                log_directory = f'{os.getcwd()}/logs'
                if not (os.path.isdir(log_directory)):
                    os.makedirs(os.path.join(log_directory))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory !")
                    raise

            with open(f'{os.getcwd()}/logs/node_{node_params.node_id}.log', 'a') as f:
                f.write(log)

    def __message_parser(self, node_params,
                         data):
        '''
        parse the information from the message packet
        :param data: received data packet
        :return: parsed information
        '''
        data = json.loads(data.decode())

        node_mac = data.get('node_mac')
        node_id = data.get('node_id')
        node_state = data.get('node_state')
        node_position_x = data.get('node_position_x')
        node_position_y = data.get('node_position_y')
        node_position_z = data.get('node_position_z')

        tentacle_id = data.get('tentacle_id')
        tentacle_state = data.get('tentacle_state')

        tentacle_within_pos = data.get('tentacle_within_pos')

        extra_on_tentacle = data.get('extra_on_tentacle')
        reinforce_on_tentacle = data.get('reinforce_on_tentacle')

        real_target_detection = data.get('real_target_detection')
        real_target_position_x = data.get('real_target_position_x')
        real_target_position_y = data.get('real_target_position_y')
        real_target_position_z = data.get('real_target_position_z')

        origin_connection = data.get('origin_connection')
        dest_connection = data.get('dest_connection')

        is_anchored = data.get('is_anchored')
        is_reinforced = data.get('is_reinforced')

        anchoring = data.get('anchoring')
        reinforcing = data.get('reinforcing')

        global_count = data.get('global_count')

        node_signal = self.__get_signal_quality(node_mac,node_position_x,node_position_y,node_position_z,node_params)

        has_sensor = data.get('has_sensor')

        virtual_target = data.get('virtual_target')
        virtual_target_position_x = data.get('virtual_target_position_x')
        virtual_target_position_y = data.get('virtual_target_position_y')
        virtual_target_position_z = data.get('virtual_target_position_z')

        return node_mac, node_id, node_state,node_position_x, node_position_y, node_position_z, \
               tentacle_id, tentacle_state, tentacle_within_pos,\
               extra_on_tentacle,reinforce_on_tentacle, \
               real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z,\
               origin_connection, dest_connection,\
               is_anchored, is_reinforced, anchoring, reinforcing,\
               global_count, \
               node_signal, has_sensor, \
               virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z

    def __message_handling(self,hyper_params,node_params, situation_params,
                           my_node_status,my_node_signal):

        adj_nodes = len(my_node_status)

        for i in range((adj_nodes+1)*5):
            try :
                data, addr = self.__sock.recvfrom(4096)
                if data :
                    try :
                        self.__message_receiver(hyper_params, node_params, situation_params,
                                                my_node_status, my_node_signal, data)
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

                        with open(f'{os.getcwd()}/logs/node_{node_params.node_id}.err', 'a') as f:
                            log = f'{time_str}\nError in \'message_receiver\' - {e1}\n'
                            f.write(log)
                            print(log)
            except Exception as e:
                # print(e)
                pass
            finally:
                time.sleep(0.1 + 0.001 * random.random())

    def __state_update(self,hyper_params,situation_params,node_params,
                     my_node_status,my_node_signal):
        '''
        state control
        '''
        if node_params.virtual_target > 0:
            next_tentacle_state, next_node_state = self.__state_controller.virtual_origin_mode_state_manage(hyper_params,situation_params,node_params,my_node_status)
            node_params.tentacle_state = next_tentacle_state
            node_params.node_state = next_node_state
            return 0

        if(node_params.node_state is NodeState.Origin or node_params.node_state is NodeState.Destination):
            return 0

        if(self.__state_controller.check_orphan_conditions(hyper_params,situation_params,node_params)):
            situation_params.hold_timer = 0
            situation_params.hold = False
            node_params.node_state = NodeState.Orphan
            return 0
        if(self.__state_controller.check_damaged_conditions(hyper_params,situation_params,node_params)):
            node_params.tentacle_state = TentacleState.Damaged
            situation_params.hold = True
            situation_params.hold_timer = time.time()
            print(f"hold_timer : {situation_params.hold_timer}")
            return 0

        next_tentacle_state, next_node_state, = self.__state_controller.get_next_state(hyper_params, situation_params, node_params, my_node_status)
        node_params.tentacle_state = next_tentacle_state
        node_params.node_state = next_node_state
        return 0

    def __message_sender(self,hyper_params,situation_params,node_params,
                       my_node_status,my_node_signal):
        '''
        update 된 내정보 보내기
        :param params:
        :return:
        '''

        connectionInfo1 = ('127.0.0.1', 10801)
        connectionInfo2 = ('127.0.0.1', 10802)
        connectionInfo3 = ('127.0.0.1', 10803)
        connectionInfo4 = ('127.0.0.1', 10804)
        connectionInfo5 = ('127.0.0.1', 10805)
        connectionInfo6 = ('127.0.0.1', 10806)
        connectionInfo7 = ('127.0.0.1', 10807)
        connectionInfo8 = ('127.0.0.1', 10808)
        connectionInfo9 = ('127.0.0.1', 10809)

        node_mac = node_params.mac
        node_id = node_params.node_id
        node_state = node_params.node_state
        node_position_x = node_params.position_x
        node_position_y = node_params.position_y
        node_position_z = node_params.position_z
        tentacle_id = node_params.tentacle_id
        tentacle_state = node_params.tentacle_state
        tentacle_within_pos = situation_params.tentacle_within_pos
        extra_on_tentacle = situation_params.extra_on_tentacle
        reinforce_on_tentacle = situation_params.reinforce_on_tentacle
        real_target_detection = situation_params.real_target_detection
        real_target_position_x = situation_params.real_target_position_x
        real_target_position_y = situation_params.real_target_position_y
        real_target_position_z = situation_params.real_target_position_z
        origin_connection = situation_params.origin_connection
        dest_connection = situation_params.dest_connection
        is_anchored = situation_params.is_anchored
        is_reinforced = situation_params.is_reinforced
        anchoring = situation_params.anchoring
        reinforcing = situation_params.reinforcing
        global_count = situation_params.global_count
        has_sensor = node_params.has_sensor
        virtual_target = node_params.virtual_target
        virtual_target_position_x = node_params.virtual_target_position_x
        virtual_target_position_y = node_params.virtual_target_position_y
        virtual_target_position_z = node_params.virtual_target_position_z

        message = Message(node_mac, node_id, node_state, node_position_x, node_position_y, node_position_z, \
                        tentacle_id, tentacle_state, tentacle_within_pos, \
                        extra_on_tentacle, reinforce_on_tentacle, \
                        real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                        origin_connection, dest_connection, \
                        is_anchored, is_reinforced, anchoring, reinforcing, \
                        global_count , has_sensor, \
                        virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z)


        self.__sock.sendto(message.get_json_format().encode(), connectionInfo1)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo2)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo3)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo4)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo5)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo6)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo7)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo8)
        self.__sock.sendto(message.get_json_format().encode(), connectionInfo9)

    def communication(self):
        '''
        the function operated by comm_thread
        On init,
        1.Receive message and Update node_status
        2.Calculate profiles and Update SDP
        3.State_control/update
        4.move_command
        5.Send a message
        On load,
        on the first 15 second,
        1.Receive message and Update node_status
        2.move_command
        3.Send a message
        after,
        1.Receive message and Update node_status
        2.Calculate profiles and Update SDP
        3.State_control/update
        4.move_command
        5.Send a message
        '''
        load_time = time.time()
        while True:
                self.__message_handling(hyper_params,
                                        node_params,
                                        situation_params,
                                        my_node_status,
                                        my_node_signal)
                self.__calculate_profile_and_update_situation_params(hyper_params,
                                                                     situation_params,
                                                                     node_params,
                                                                     my_node_status,
                                                                     my_node_signal)
                self.__state_update(hyper_params,
                                    situation_params,
                                    node_params,
                                    my_node_status,
                                    my_node_signal)
                time.sleep(0.2)
                self.__message_sender(hyper_params,
                                      situation_params,
                                      node_params,
                                      my_node_status,
                                      my_node_signal)

    def __get_signal_quality(self, node_mac, node_position_x, node_position_y, node_position_z,node_params):
        '''
            Get signal quality of a node
            - CORE_MODE : using distance
            - REAL_MODE : using iw command
        '''
        # if run_mode == CORE_MODE:  # CORE
        my_position_x = node_params.position_x
        my_position_y = node_params.position_y
        my_position_z = node_params.position_z
        radio_range = node_params.radio_range

        rx_signal = math.sqrt(
            (my_position_x - node_position_x) ** 2 + (my_position_y - node_position_y) ** 2 + (my_position_z - node_position_z) ** 2)

        if (rx_signal < radio_range):
            # rxSignal = 50 - (10 * math.log(rxSignal/4))
            rx_signal = 1 - (rx_signal / radio_range)
        else:
            rx_signal = -9999

        # elif self.__run_mode == REAL_MODE:  # Real
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

    def __update_node_status(self,node_id, node_state, node_position_x, node_position_y, node_position_z, node_signal,
                             tentacle_id, tentacle_state, tentacle_within_pos,
                             extra_on_tentacle, reinforce_on_tentacle,
                             real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z,
                             origin_connection, dest_connection,
                             is_anchored, is_reinforced, anchoring, reinforcing,
                             node_last_connection_time,
                             global_count,
                             my_node_status, my_node_signal, has_sensor,
                             virtual_target, virtual_target_position_x, virtual_target_position_y,
                             virtual_target_position_z,
                             situation_params, node_params):
        '''
            Store the signal and other data from an adjacent node
            - Signal quality : 5 times
        '''
        AVERAGESAMPLES = 5 # From cnp

        # add or update nodes statue
        if node_id in my_node_status:
            # update
            my_node_signal[node_id].pop(0)
            my_node_signal[node_id].append(node_signal)

            avg_signal = 0
            sig_count = 0

            for i in my_node_signal[node_id]:
                if i != -9999:
                    avg_signal += i
                    sig_count += 1

            if sig_count == 0:
                avg_signal = -9999
            else:
                avg_signal /= sig_count
                my_node_status[node_id]['node_last_connection_time'] = node_last_connection_time

            my_node_status[node_id]['node_signal'] = avg_signal

        else:
            # add
            my_node_status[node_id] = {}
            my_node_signal[node_id] = [node_signal] * AVERAGESAMPLES # From cnp
            my_node_status[node_id]['node_signal'] = node_signal
            my_node_status[node_id]['node_last_connection_time'] = node_last_connection_time
            # self.__update_adjacency(node_id, True)


        if('node_state' in my_node_status[node_id].keys() and my_node_status[node_id]['node_state'] is NodeState.Free and NodeState(node_state) is NodeState.Tip):
            if(node_params.node_state is NodeState.Tip):
                situation_params.is_new_tip = True

        my_node_status[node_id]['node_state'] = NodeState(node_state)
        my_node_status[node_id]['node_position_x'] = node_position_x
        my_node_status[node_id]['node_position_y'] = node_position_y
        my_node_status[node_id]['tentacle_id'] = tentacle_id
        my_node_status[node_id]['tentacle_state'] = TentacleState(tentacle_state)
        my_node_status[node_id]['tentacle_within_pos'] = tentacle_within_pos
        my_node_status[node_id]['extra_on_tentacle'] = extra_on_tentacle
        my_node_status[node_id]['reinforce_on_tentacle'] = reinforce_on_tentacle
        my_node_status[node_id]['real_target_detection'] = real_target_detection
        my_node_status[node_id]['real_target_position_x'] = real_target_position_x
        my_node_status[node_id]['real_target_position_y'] = real_target_position_y
        my_node_status[node_id]['real_target_position_z'] = real_target_position_z
        my_node_status[node_id]['origin_connection'] = origin_connection
        my_node_status[node_id]['dest_connection'] = dest_connection
        my_node_status[node_id]['is_anchored'] = is_anchored
        my_node_status[node_id]['is_reinforced'] = is_reinforced
        my_node_status[node_id]['anchoring'] = anchoring
        my_node_status[node_id]['reinforcing'] = reinforcing
        my_node_status[node_id]['global_count'] = global_count
        my_node_status[node_id]['has_sensor'] = has_sensor
        my_node_status[node_id]['virtual_target'] = virtual_target
        my_node_status[node_id]['virtual_target_position_x'] = virtual_target_position_x
        my_node_status[node_id]['virtual_target_position_y'] = virtual_target_position_y
        my_node_status[node_id]['virtual_target_position_z'] = virtual_target_position_z

    def __calculate_profile_and_update_situation_params(self, hyper_params, situation_params, node_params,
                                                        my_node_status, my_node_signal):
        # print(my_node_status)
        vel_x, vel_y = 0, 0  # next x,y velocity
        o_x, o_y = 0, 0  # used for chekcing whether current position is good for tentacle
        add_x, add_y = 0, 0  # x,y velocity based nearby nodes
        adj_origin, adj_dest, adj_tip, adj_backbone, adj_free , adj_virtual_origin = 0, 0, 0, 0, 0, 0 # number of nearby nodes type
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
                virtx, virty = self.__profile_generator.generate_origin_profile(hyper_params,situation_params,node_params,
                                                                                my_node_status,my_node_signal)
            else:
                virtx, virty = self.__profile_generator.generate_destination_profile(hyper_params,situation_params,node_params,
                                                                                     my_node_status,my_node_signal)

            if node_params.virtual_target > 0:
                virtx = virtx/2
                virty = virty/2

            vel_x, vel_y = virtx, virty
            print(f'virtx : {virtx}, virty : {virty}')
            next_attractor = self.__get_further_node_on_same_tentacle(hyper_params,situation_params,node_params,
                                                                      my_node_status,globalNodesId)
            print(f'next_attractor : {next_attractor}')
            for node_id in globalNodesId:
                node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
                tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
                real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                origin_connection, dest_connection, \
                is_anchored, is_reinforced, anchoring, reinforcing, \
                global_count, \
                virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(hyper_params, situation_params, node_params, node_id, my_node_status)

                max_tentacle_within_pos = tentacle_within_pos if max_tentacle_within_pos < tentacle_within_pos else max_tentacle_within_pos
                if tentacle_within_pos != -9999:
                    min_tentacle_within_pos = tentacle_within_pos if min_tentacle_within_pos > tentacle_within_pos else min_tentacle_within_pos

                # Release any reinforcement node that does not hear from its anchor
                if node_signal == -9999:
                    continue

                if node_state is not NodeState.Destination and node_state is not NodeState.Origin and node_state is not NodeState.Orphan:
                    if global_count > my_global_count:
                        if(origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if(dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        # damaged 쪽이 global count 더 큰데 tentacle state 받아오면 또 다시 damaged 되버림
                        if node_params.node_state is NodeState.Free and situation_params.reinforcing != -9999:
                            situation_params.reinforcing = -9999

                        elif(tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        situation_params.global_count = global_count

                    if node_params.node_state is NodeState.Orphan and node_params.tentacle_state is TentacleState.Damaged:
                        if(origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if(dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        if(tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        if global_count > my_global_count:
                            situation_params.global_count = global_count

                if node_state is NodeState.Orphan and node_params.node_state is NodeState.Orphan:
                    if global_count > my_global_count:
                        if(origin_connection):
                            situation_params.origin_connection = True
                        else:
                            situation_params.origin_connection = False

                        if(dest_connection):
                            situation_params.dest_connection = True
                        else:
                            situation_params.dest_connection = False

                        if(tentacle_state is not node_params.tentacle_state):
                            situation_params.latest_tentacle_state = tentacle_state
                        situation_params.global_count = global_count


                add_x, add_y = self.__profile_generator.generate_ra_profile(hyper_params, situation_params, node_params,
                                                                            node_state, node_signal, node_position_x, node_position_y, tentacle_within_pos)

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
                        if(anchoring == node_params.node_id):
                            situation_params.is_anchored = node_id

                elif node_state is NodeState.Reinforce:

                    new_adj_nodes.append(node_id)

                    if my_state is NodeState.Extra or my_state is NodeState.Reinforce:
                        vel_x += add_x
                        vel_y += add_y

                    if node_params.node_state is NodeState.Backbone and situation_params.is_reinforced == -9999:
                        if(reinforcing == node_params.node_id):
                            situation_params.is_anchored = -9999
                            situation_params.is_reinforced = node_id

                elif node_state is NodeState.Free:
                    adj_free += 1
                    new_adj_nodes.append(node_id)
                    if my_state is NodeState.Free:
                        vel_x += add_x
                        vel_y += add_y

                if virtual_target > 0 :
                    if global_count > my_global_count :
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
                virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(hyper_params, situation_params, node_params, node_id, my_node_status)

                if node_state is not NodeState.Destination and node_state is not NodeState.Origin and node_state is not NodeState.Orphan:
                    if global_count > my_global_count:
                        situation_params.global_count = global_count


        print(f"adj_origin : {adj_origin}, adj_free : {adj_free} ,adj_tip : {adj_tip}, adj_back : {adj_backbone}, adj_dest : {adj_dest}")

        #first detector
        if(adj_origin == 1 and situation_params.origin_connection == False):
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
                        if my_node_status[adj_backbones[0]]['tentacle_within_pos'] > situation_params.tentacle_within_pos:
                            situation_params.origin_connection = False
                            situation_params.global_count = situation_params.global_count + 1
                        if my_node_status[adj_backbones[0]]['tentacle_within_pos'] < situation_params.tentacle_within_pos:
                            situation_params.dest_connection = False
                            situation_params.global_count = situation_params.global_count + 1

        if node_params.node_state is NodeState.Reinforce:
            if adj_origin == 1 and adj_backbone == 0:
                situation_params.dest_connection = False
            if adj_dest == 1 and adj_backbone == 0:
                situation_params.origin_connection = False

        if node_params.virtual_target > 0 and node_params.node_id == node_params.virtual_target:
                add_x, add_y = self.__profile_generator.generate_virtual_target_profile(hyper_params,situation_params,node_params,
                                                                          my_node_status,my_node_signal)
                vel_x += add_x
                vel_y += add_y

        if node_params.virtual_target == 0:
            if node_params.node_state is not NodeState.Origin and node_params.node_state is not NodeState.Destination:
                add_x, add_y = self.__profile_generator.generate_virtual_target_profile(hyper_params,situation_params,node_params,
                                                                          my_node_status,my_node_signal)
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


        if math.sqrt(vel_x**2 + vel_y**2) < node_params.equilibrium_zone:
            situation_params.equilibrium = situation_params.equilibrium+1
        else:
            situation_params.equilibrium = 0

    def __get_node_status(self, hyper_params,situation_params,node_params,
                          node_id,my_node_status):
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

        return  node_state, node_position_x, node_position_y, tentacle_id, tentacle_within_pos, node_signal, \
                tentacle_state, extra_on_tentacle, reinforce_on_tentacle, \
                real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                origin_connection, dest_connection, \
                is_anchored, is_reinforced, anchoring, reinforcing, \
                global_count, \
                virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z

    def __get_further_node_on_same_tentacle(self, hyper_params, situation_params, node_params,
                                            my_node_status,globalNodesId):
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
            virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z = self.__get_node_status(hyper_params, situation_params, node_params, node_id, my_node_status)

            if node_signal != UNKNOWN:
                # 상대가 tentacle, tip이거나 상대가 backbone일때, 내가 텐타클 id가 더 큰경우 && 상대가 현재 atrractor보다 먼 경우
                if (node_state is NodeState.Tip or
                    (node_state is NodeState.Backbone and my_tentacle_id >= tentacle_id)) and (tentacle_within_pos >= next_attractor):
                    next_attractor = tentacle_within_pos

                elif node_state is NodeState.Backbone and (
                        my_node_state is NodeState.Extra and tentacle_within_pos >= next_attractor):
                    next_attractor = tentacle_within_pos

        return next_attractor

    def __get_adj_backbone_node(self,adj_nodes,my_node_status):
        adj_backbones = [node_id for node_id in adj_nodes if my_node_status[node_id]['node_state'] is NodeState.Backbone]
        return adj_backbones