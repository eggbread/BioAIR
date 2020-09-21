from drone.state import NodeState, TentacleState
import math


class ProfileGenerator(object):
    def __init__(self):
        pass

    def calculate_profile(self, node_params, situation_params, hyper_params, node_status):
        my_state = node_params.node_state

        if my_state is NodeState.Origin or my_state is NodeState.Destination:
            pass
        else:
            pass


    def __generate_ra_profile(self, hyper_params, situation_params, node_params,
                            node_state, node_signal, node_position_x, node_position_y, tentacle_within_pos):
        '''
        인접노드에 대해서 R/A profile 계산
        :return: R/A profile
        '''
        add_x, add_y = 0, 0
        factor = 0

        my_state = node_params.node_state
        my_position_x = node_params.position_x
        my_position_y = node_params.position_y
        my_position_z = node_params.position_z
        high_sq = node_params.high_sq
        low_sq = node_params.low_sq
        REPULSOR = hyper_params.repulsor

        # Close to Node
        if node_signal > high_sq:
            factor = REPULSOR * (node_signal - high_sq) / (1 - high_sq)
        # Far from Node
        elif node_signal < low_sq:
            factor = - low_sq / node_signal
        else:
            factor = 0

        if node_state == NodeState.Destination and factor > 0:
            factor = 0
        # Why Dest pass the if twice?
        elif node_state is NodeState.Origin or node_state is NodeState.Tip or node_state is NodeState.Backbone or node_state is NodeState.Destination or node_state is NodeState.Orphan:
            pass
        elif my_state is NodeState.Tip or my_state is NodeState.Backbone:
            factor = 0
        elif factor > 0 and (node_state is NodeState.Extra or node_state is NodeState.Reinforce):
            factor = 0
        elif factor < 0:
            factor = 0
        # factor * cos()
        add_x = factor * (my_position_x - node_position_x) / math.sqrt(
            (my_position_x - node_position_x) ** 2 + (my_position_y - node_position_y) ** 2)
        add_y = factor * (my_position_y - node_position_y) / math.sqrt(
            (my_position_x - node_position_x) ** 2 + (my_position_y - node_position_y) ** 2)

        return add_x, add_y

    def __generate_destination_profile(self,hyper_params,situation_params,node_params,
                                     my_node_status,my_node_signal):
        '''
        Get field to destination
        :return: destination virtual attraction profile
        '''
        vel_x, vel_y = 0, 0

        dest_position_x = node_params.dest_position_x
        dest_position_y = node_params.dest_position_y
        dest_position_z = node_params.dest_position_z
        my_position_x = node_params.position_x
        my_position_y = node_params.position_y
        my_position_z = node_params.position_z
        TARGETPROXIMITY = hyper_params.targetproximity
        TARGETFORCE = hyper_params.targetforce

        if abs(dest_position_x - my_position_x) < TARGETPROXIMITY:
            # 안전 거리 이내 인 경우 천천히
            vel_x = (dest_position_x - my_position_x) / (TARGETPROXIMITY * 1.0)
        elif (dest_position_x > my_position_x):
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼 
            vel_x = TARGETFORCE
        else:
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼
            vel_x = 0 - TARGETFORCE

        if (abs(dest_position_y - my_position_y) < TARGETPROXIMITY):
            # 안전 거리 이내 인 경우 천천히
            vel_y = (dest_position_y - my_position_y) / (TARGETPROXIMITY * 1.0)
        elif (dest_position_y > my_position_y):
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼 
            vel_y = TARGETFORCE
        else:
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼 
            vel_y = 0 - TARGETFORCE

        ratio = abs(dest_position_y - my_position_y) / (
                abs(dest_position_x - my_position_x) * 1.0)
        if (ratio < 1.0):
            vel_y = vel_y * ratio

        ratio = abs(dest_position_x - my_position_x) / (
                abs(dest_position_y - my_position_y) * 1.0)
        if (ratio < 1.0):
            vel_x = vel_x * ratio

        return vel_x, vel_y

    def generate_origin_profile(self, hyper_params, situation_params, node_params,
                                my_node_status, my_node_signal):
        '''
        Get field to destination
        :return: destination virtual attraction profile
        '''
        vel_x, vel_y = 0, 0

        origin_position_x = node_params.origin_position_x
        origin_position_y = node_params.origin_position_y
        origin_position_z = node_params.origin_position_z
        my_position_x = node_params.position_x
        my_position_y = node_params.position_y
        my_position_z = node_params.position_z
        TARGETPROXIMITY = hyper_params.targetproximity
        TARGETFORCE = hyper_params.targetforce

        if abs(origin_position_x - my_position_x) < TARGETPROXIMITY:
            # 안전 거리 이내 인 경우 천천히
            vel_x = (origin_position_x - my_position_x) / (TARGETPROXIMITY * 1.0)
        elif (origin_position_x > my_position_x):
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼
            vel_x = TARGETFORCE
        else:
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼
            vel_x = 0 - TARGETFORCE

        if (abs(origin_position_y - my_position_y) < TARGETPROXIMITY):
            # 안전 거리 이내 인 경우 천천히
            vel_y = (origin_position_y - my_position_y) / (TARGETPROXIMITY * 1.0)
        elif (origin_position_y > my_position_y):
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼
            vel_y = TARGETFORCE
        else:
            # 안전 거리보다 멀리 떨어진 경우 Force 만큼
            vel_y = 0 - TARGETFORCE

        ratio = abs(origin_position_y - my_position_y) / (
                abs(origin_position_x - my_position_x) * 1.0)
        if (ratio < 1.0):
            vel_y = vel_y * ratio

        ratio = abs(origin_position_x - my_position_x) / (
                abs(origin_position_y - my_position_y) * 1.0)
        if (ratio < 1.0):
            vel_x = vel_x * ratio

        return vel_x, vel_y