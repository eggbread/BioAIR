import time
import os

from drone.state import NodeState, TentacleState
from modules.sub.profile_generator import ProfileGenerator
from modules.sub.state_controller import StateController


class Motion(object):
    def __init__(self, bioair_params, receiver_queue, sender_queue, receiver_lock, sender_lock):
        self.node_params = bioair_params.get('CNP')
        self.situation_params = bioair_params.get('SDP')
        self.hyper_params = bioair_params.get('SHP')

        self.profile_generator = ProfileGenerator()
        self.state_controller = StateController()

        self.node_status = {}

        self.sender_queue = sender_queue
        self.receiver_queue = receiver_queue
        self.receiver_lock = receiver_lock
        self.sender_lock = sender_lock

    def __update_node_status(self, adj_node):
        """
        Store the signal and other data from an adjacent node
        :param adj_node: Adjacent Node's data
        :return:
        """
        node_id = adj_node.get('node_id')

        if node_id in self.node_status.keys():
            cnt_signal = self.node_status[node_id]['cnt_signal']
            self.node_status.get(node_id)['node_signal'] += adj_node.get('node_signal')

            if cnt_signal == self.hyper_params.average_sample:
                self.node_status.get(node_id)['node_signal'] /= self.hyper_params.average_sample
                self.node_status.get(node_id)['cnt_signal'] = 0
                self.node_status.get(node_id).update(adj_node)
            else:
                self.node_status[node_id]['cnt_signal'] += 1
        else:
            self.node_status.update({node_id: adj_node})
            self.node_status[node_id]['cnt_signal'] = 1


    def __update_location(self, bioair_params):
        '''
        Base on calculated profile,
        Get the next position
        '''
        node_params = bioair_params.get('CNP')
        situation_params = bioair_params.get('SDP')
        hyper_params = bioair_params.get('SHP')
        expected_x, expected_y, wp_latitude, wp_longtitude = 0, 0, 0, 0
        wait_time = 0

        if situation_params.hold:
            node_params.next_vel_x = 0
            node_params.next_vel_y = 0

        prev_vel_x = node_params.prev_vel_x
        prev_vel_y = node_params.prev_vel_y
        vel_x = node_params.next_vel_x
        vel_y = node_params.next_vel_y
        # print(f'final next_vel_x : {vel_x} , next_vel_y : {vel_y}')
        position_x = node_params.position_x
        position_y = node_params.position_y

        max_groundspeed = 5

        if (((prev_vel_x < 0) and (vel_x >= 0)) or ((prev_vel_x > 0) and (vel_x <= 0)) or (
                (prev_vel_x == 0) and (vel_x != 0)) or ((prev_vel_y < 0) and (vel_y >= 0)) or (
                (prev_vel_y > 0) and (vel_y <= 0)) or ((prev_vel_y == 0) and (vel_y != 0))):
            wait_time = 0
        else:
            wait_time = 1.5 * ((vel_x ** 2) + (vel_y ** 2))

        vel_x = vel_x * max_groundspeed
        vel_y = vel_y * max_groundspeed

        if(vel_x !=0 and vel_y !=0):

            if (vel_x >= max_groundspeed):
                vel_y = (vel_y * max_groundspeed) / vel_x
                vel_x = max_groundspeed
            elif (vel_x <= -max_groundspeed):
                vel_y = (vel_y * (0 - max_groundspeed)) / vel_x
                vel_x = -max_groundspeed

            if (vel_y >= max_groundspeed):
                vel_x = (vel_x * max_groundspeed) / vel_y
                vel_y = max_groundspeed
            elif (vel_y <= -max_groundspeed):
                vel_x = (vel_x * (0 - max_groundspeed)) / vel_y
                vel_y = -max_groundspeed

        expected_x = position_x + vel_x * wait_time
        expected_y = position_y + vel_y * wait_time

        # if run_mode == CORE_MODE:
        self.__update_core_position(hyper_params, situation_params, node_params, position_x, position_y)

        node_params.position_x = position_x + (vel_x * 0.3)
        node_params.position_y = position_y + (vel_y * 0.3)

        # elif run_mode == REAL_MODE:

    def __update_core_position(self, hyper_params, situation_params, node_params, position_x, position_y):
        '''
        Update Node position to next position_x, position_y On the CORE(View)
        :param position_x: next_position_x
        :param position_y: next_position_y
        :return:
        '''
        ip = node_params.ip
        node_id = node_params.node_id
        state = node_params.node_state
        tentacle_state = node_params.tentacle_state
        if(state is NodeState.Origin or state is NodeState.Destination):
            cmd = f'coresendmsg -a {ip} NODE NUMBER={node_id} NAME={node_id}_{state} X_POSITION={int(position_x)} Y_POSITION={int(position_y)}'
        else:
            cmd = f'coresendmsg -a {ip} NODE NUMBER={node_id} NAME={node_id}_{state}_{tentacle_state} X_POSITION={int(position_x)} Y_POSITION={int(position_y)}'
            if node_params.node_id == node_params.virtual_target:
                cmd = f'coresendmsg -a {ip} NODE NUMBER={node_id} NAME={node_id}_{state}_{tentacle_state}_virtual_origin_{node_params.virtual_target} X_POSITION={int(position_x)} Y_POSITION={int(position_y)}'

        # start cmd
        os.popen(cmd)

    def run(self):
        self.profile_generator.calculate_profile(self.node_status, self.situation_params, self.hyper_params, self.node_status)
        self.state_controller.get_next_state()

    def move_command(self):
        '''
        this function is operated by motion_thread
        Command drone to move to next position
        '''
        while True:
            if not self.receiver_queue.empty():
                self.receiver_lock.acquire()
                adj_node = self.receiver_queue.get()
                self.receiver_lock.release()

                self.__update_node_status(adj_node)
            self.run()
            time.sleep(0.3)
