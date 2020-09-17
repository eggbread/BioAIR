import json


class Message(object):
    def __init__(self, node_mac, node_id, node_state, node_position_x, node_position_y, node_position_z,
                 tentacle_id, tentacle_state, tentacle_within_pos,
                 extra_on_tentacle, reinforce_on_tentacle, \
                 real_target_detection, real_target_position_x, real_target_position_y, real_target_position_z, \
                 origin_connection, dest_connection, \
                 is_anchored, is_reinforced, anchoring, reinforcing, \
                 global_count, has_sensor, \
                 virtual_target, virtual_target_position_x, virtual_target_position_y, virtual_target_position_z):
        self.__node_mac = node_mac
        self.__node_id = node_id
        self.__node_state = node_state
        self.__node_position_x = node_position_x
        self.__node_position_y = node_position_y
        self.__node_position_z = node_position_z

        self.__tentacle_id = tentacle_id
        self.__tentacle_state = tentacle_state

        self.__tentacle_within_pos = tentacle_within_pos

        self.__extra_on_tentacle = extra_on_tentacle
        self.__reinforce_on_tentacle = reinforce_on_tentacle

        self.__real_target_detection = real_target_detection
        self.__real_target_position_x = real_target_position_x
        self.__real_target_position_y = real_target_position_y
        self.__real_target_position_z = real_target_position_z

        self.__origin_connection = origin_connection
        self.__dest_connection = dest_connection

        self.__is_anchored = is_anchored
        self.__is_reinforced = is_reinforced

        self.__anchoring = anchoring
        self.__reinforcing = reinforcing

        self.__global_count = global_count
        self.__has_sensor = has_sensor

        self.__virtual_target = virtual_target
        self.__virtual_target_position_x = virtual_target_position_x
        self.__virtual_target_position_y = virtual_target_position_y
        self.__virtual_target_position_z = virtual_target_position_z

    def get_json_format(self):
        '''
        메시지 클래스 인스턴스를 json으로 변환해서 리턴해준다.
        :return: json format message
        '''
        json_message = json.dumps({
            'node_mac': self.__node_mac,
            'node_id': self.__node_id,
            'node_state': self.__node_state.value,
            'node_position_x': self.__node_position_x,
            'node_position_y': self.__node_position_y,
            'node_position_z': self.__node_position_z,

            'tentacle_id': self.__tentacle_id,
            'tentacle_state': self.__tentacle_state.value,

            'tentacle_within_pos': self.__tentacle_within_pos,

            'extra_on_tentacle': self.__extra_on_tentacle,
            'reinforce_on_tentacle': self.__reinforce_on_tentacle,
            'real_target_detection': self.__real_target_detection,
            'real_target_position_x': self.__real_target_position_x,
            'real_target_position_y': self.__real_target_position_y,
            'real_target_position_z': self.__real_target_position_z,

            'origin_connection': self.__origin_connection,
            'dest_connection': self.__dest_connection,

            'is_anchored': self.__is_anchored,
            'is_reinforced': self.__is_reinforced,
            'anchoring': self.__anchoring,
            'reinforcing': self.__reinforcing,

            'global_count': self.__global_count,
            'has_sensor': self.__has_sensor,

            'virtual_target': self.__virtual_target,
            'virtual_target_position_x': self.__virtual_target_position_x,
            'virtual_target_position_y': self.__virtual_target_position_y,
            'virtual_target_position_z': self.__virtual_target_position_z
        })

        return json_message
