from drone.state import NodeState, TentacleState


class ConfigurableNodeParams(object):
    def __init__(self, config=None):
        """
        Init the ConfigurableNodeParams
        :param config: Parser.__config
        """
        self.__ip = "127.0.0.1"
        self.__mac = "00:00:00:aa:00:02"
        self.__port = 10800
        self.__node_id = 1
        self.__tentacle_id = -9999
        self.__node_state = NodeState.Free
        self.__tentacle_state = TentacleState.Forming
        self.__position_x = 137
        self.__position_y = 350
        self.__position_z = 0
        self.__origin_id = 1
        self.__origin_position_x = 30
        self.__origin_position_y = 5
        self.__origin_position_z = 0
        self.__dest_id = 1
        self.__dest_position_x = 870
        self.__dest_position_y = 260
        self.__dest_position_z = 0

        self.__prev_vel_x = 0
        self.__prev_vel_y = 0
        self.__prev_vel_z = 0

        self.__next_vel_x = 0
        self.__next_vel_y = 0
        self.__next_vel_z = 0

        self.__high_sq = 0.3
        self.__low_sq = 0.2
        self.__equilibrium_zone = 0.1
        self.__radio_range = 330

        self.__has_sensor = False

        self.__virtual_target = -1  # -1 : off / 0 : on / node_id : virtual_origin
        self.__virtual_target_position_x = 0
        self.__virtual_target_position_y = 0
        self.__virtual_target_position_z = 0

        self.__init(config)

    def save(self, config=None):
        """
        Save the ConfigurableNodeParams
        :param config: Parser.__config
        :return:
        """

        config['ConfigurableNodeParams'] = {
            'ip': self.__ip,
            'mac': self.__mac,
            'port': self.__port,
            'node_id': self.__node_id,
            'tentacle_id': self.__tentacle_id,
            'node_state': NodeState.node_state_to_str(self.__node_state),
            'tentacle_state': TentacleState.tentacle_state_to_str(self.__tentacle_state),
            'position_x': self.__position_x,
            'position_y': self.__position_y,
            'position_z': self.__position_z,
            'origin_id': self.__origin_id,
            'origin_position_x': self.__origin_position_x,
            'origin_position_y': self.__origin_position_y,
            'origin_position_z': self.__origin_position_z,
            'dest_id': self.__dest_id,
            'dest_position_x': self.__dest_position_x,
            'dest_position_y': self.__dest_position_y,
            'dest_position_z': self.__dest_position_z,
            'prev_vel_x': self.__prev_vel_x,
            'prev_vel_y': self.__prev_vel_y,
            'prev_vel_z': self.__prev_vel_z,
            'next_vel_x': self.__next_vel_x,
            'next_vel_y': self.__next_vel_y,
            'next_vel_z': self.__next_vel_z,
            'high_sq': self.__high_sq,
            'low_sq': self.__low_sq,
            'equilibrium_zone': self.__equilibrium_zone,
            'radio_range': self.__radio_range,
            'has_sensor': str(self.__has_sensor).upper(),
            'virtual_target': self.__virtual_target,
            'virtual_target_position_x': self.__virtual_target_position_x,
            'virtual_target_position_y': self.__virtual_target_position_y,
            'virtual_target_position_z': self.__virtual_target_position_z,
        }

    def __init(self, config=None):
        """
        Load the ConfigurableNodeParams
        :param config: Parser.__config
        :return:
        """
        if 'ip' in config['ConfigurableNodeParams']:
            self.__ip = config['ConfigurableNodeParams']['ip']

        if 'mac' in config['ConfigurableNodeParams']:
            self.__mac = config['ConfigurableNodeParams']['mac']

        if 'port' in config['ConfigurableNodeParams']:
            self.__port = int(config['ConfigurableNodeParams']['port'])

        if 'node_id' in config['ConfigurableNodeParams']:
            self.__node_id = int(config['ConfigurableNodeParams']['node_id'])

        if 'tentacle_id' in config['ConfigurableNodeParams']:
            self.__tentacle_id = int(config['ConfigurableNodeParams']['tentacle_id'])

        if 'node_state' in config['ConfigurableNodeParams']:
            self.__node_state = NodeState.str_to_node_state(config['ConfigurableNodeParams']['node_state'])

        if 'tentacle_state' in config['ConfigurableNodeParams']:
            self.__tentacle_state = \
                TentacleState.str_to_tentacle_state(config['ConfigurableNodeParams']['tentacle_state'])

        if 'position_x' in config['ConfigurableNodeParams']:
            self.__position_x = float(config['ConfigurableNodeParams']['position_x'])

        if 'position_y' in config['ConfigurableNodeParams']:
            self.__position_y = float(config['ConfigurableNodeParams']['position_y'])

        if 'position_z' in config['ConfigurableNodeParams']:
            self.__position_z = float(config['ConfigurableNodeParams']['position_z'])

        if 'origin_id' in config['ConfigurableNodeParams']:
            self.__origin_id = int(config['ConfigurableNodeParams']['origin_id'])

        if 'origin_position_x' in config['ConfigurableNodeParams']:
            self.__origin_position_x = float(config['ConfigurableNodeParams']['origin_position_x'])

        if 'origin_position_y' in config['ConfigurableNodeParams']:
            self.__origin_position_y = float(config['ConfigurableNodeParams']['origin_position_y'])

        if 'origin_position_z' in config['ConfigurableNodeParams']:
            self.__origin_position_z = float(config['ConfigurableNodeParams']['origin_position_z'])

        if 'dest_id' in config['ConfigurableNodeParams']:
            self.__dest_id = int(config['ConfigurableNodeParams']['dest_id'])

        if 'dest_position_x' in config['ConfigurableNodeParams']:
            self.__dest_position_x = int(config['ConfigurableNodeParams']['dest_position_x'])

        if 'dest_position_y' in config['ConfigurableNodeParams']:
            self.__dest_position_y = int(config['ConfigurableNodeParams']['dest_position_y'])

        if 'dest_position_z' in config['ConfigurableNodeParams']:
            self.__dest_position_z = int(config['ConfigurableNodeParams']['dest_position_z'])

        if 'prev_vel_x' in config['ConfigurableNodeParams']:
            self.__prev_vel_x = float(config['ConfigurableNodeParams']['prev_vel_x'])

        if 'prev_vel_y' in config['ConfigurableNodeParams']:
            self.__prev_vel_y = float(config['ConfigurableNodeParams']['prev_vel_y'])

        if 'prev_vel_z' in config['ConfigurableNodeParams']:
            self.__prev_vel_z = float(config['ConfigurableNodeParams']['prev_vel_z'])

        if 'next_vel_x' in config['ConfigurableNodeParams']:
            self.__next_vel_x = float(config['ConfigurableNodeParams']['next_vel_x'])

        if 'next_vel_y' in config['ConfigurableNodeParams']:
            self.__next_vel_y = float(config['ConfigurableNodeParams']['next_vel_y'])

        if 'next_vel_z' in config['ConfigurableNodeParams']:
            self.__next_vel_z = float(config['ConfigurableNodeParams']['next_vel_z'])

        if 'high_sq' in config['ConfigurableNodeParams']:
            self.__high_sq = float(config['ConfigurableNodeParams']['high_sq'])

        if 'low_sq' in config['ConfigurableNodeParams']:
            self.__low_sq = float(config['ConfigurableNodeParams']['low_sq'])

        if 'equilibrium_zone' in config['ConfigurableNodeParams']:
            self.__equilibrium_zone = float(config['ConfigurableNodeParams']['equilibrium_zone'])

        if 'radio_range' in config['ConfigurableNodeParams']:
            self.__radio_range = int(config['ConfigurableNodeParams']['radio_range'])

        if 'has_sensor' in config['ConfigurableNodeParams']:
            has_sensor = config['ConfigurableNodeParams']['has_sensor']
            if has_sensor == "TRUE":
                self.__has_sensor = True
            else:
                self.__has_sensor = False

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, value):
        self.__mac = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def node_id(self):
        return self.__node_id

    @node_id.setter
    def node_id(self, value):
        self.__node_id = value

    @property
    def tentacle_id(self):
        return self.__tentacle_id

    @tentacle_id.setter
    def tentacle_id(self, value):
        self.__tentacle_id = value

    @property
    def node_state(self):
        return self.__node_state

    @node_state.setter
    def node_state(self, value):
        self.__node_state = value

    @property
    def tentacle_state(self):
        return self.__tentacle_state

    @tentacle_state.setter
    def tentacle_state(self, value):
        self.__tentacle_state = value

    @property
    def position_x(self):
        return self.__position_x

    @position_x.setter
    def position_x(self, value):
        self.__position_x = value

    @property
    def position_y(self):
        return self.__position_y

    @position_y.setter
    def position_y(self, value):
        self.__position_y = value

    @property
    def position_z(self):
        return self.__position_z

    @position_z.setter
    def position_z(self, value):
        self.__position_z = value

    @property
    def origin_id(self):
        return self.__origin_id

    @origin_id.setter
    def origin_id(self, value):
        self.__origin_id = value

    @property
    def origin_position_x(self):
        return self.__origin_position_x

    @origin_position_x.setter
    def origin_position_x(self, value):
        self.__origin_position_x = value

    @property
    def origin_position_y(self):
        return self.__origin_position_y

    @origin_position_y.setter
    def origin_position_y(self, value):
        self.__origin_position_y = value

    @property
    def origin_position_z(self):
        return self.__origin_position_z

    @origin_position_z.setter
    def origin_position_z(self, value):
        self.__origin_position_z = value

    @property
    def dest_id(self):
        return self.__dest_id

    @dest_id.setter
    def dest_id(self, value):
        self.__dest_id = value

    @property
    def dest_position_x(self):
        return self.__dest_position_x

    @dest_position_x.setter
    def dest_position_x(self, value):
        self.__dest_position_x = value

    @property
    def dest_position_y(self):
        return self.__dest_position_y

    @dest_position_y.setter
    def dest_position_y(self, value):
        self.__dest_position_y = value

    @property
    def dest_position_z(self):
        return self.__dest_position_z

    @dest_position_z.setter
    def dest_position_z(self, value):
        self.__dest_position_z = value

    @property
    def prev_vel_x(self):
        return self.__prev_vel_x

    @prev_vel_x.setter
    def prev_vel_x(self, value):
        self.__prev_vel_x = value

    @property
    def prev_vel_y(self):
        return self.__prev_vel_y

    @prev_vel_y.setter
    def prev_vel_y(self, value):
        self.__prev_vel_y = value

    @property
    def prev_vel_z(self):
        return self.__prev_vel_z

    @prev_vel_z.setter
    def prev_vel_z(self, value):
        self.__prev_vel_z = value

    @property
    def next_vel_x(self):
        return self.__next_vel_x

    @next_vel_x.setter
    def next_vel_x(self, value):
        self.__next_vel_x = value

    @property
    def next_vel_y(self):
        return self.__next_vel_y

    @next_vel_y.setter
    def next_vel_y(self, value):
        self.__next_vel_y = value

    @property
    def next_vel_z(self):
        return self.__next_vel_z

    @next_vel_z.setter
    def next_vel_z(self, value):
        self.__next_vel_z = value

    @property
    def high_sq(self):
        return self.__high_sq

    @high_sq.setter
    def high_sq(self, value):
        self.__high_sq = value

    @property
    def low_sq(self):
        return self.__low_sq

    @low_sq.setter
    def low_sq(self, value):
        self.__low_sq = value

    @property
    def equilibrium_zone(self):
        return self.__equilibrium_zone

    @equilibrium_zone.setter
    def equilibrium_zone(self, value):
        self.__equilibrium_zone = value

    @property
    def radio_range(self):
        return self.__radio_range

    @radio_range.setter
    def radio_range(self, value):
        self.__radio_range = value

    @property
    def has_sensor(self):
        return self.__has_sensor

    @has_sensor.setter
    def has_sensor(self, value):
        self.__has_sensor = value

    @property
    def virtual_target(self):
        return self.__virtual_target

    @virtual_target.setter
    def virtual_target(self, value):
        self.__virtual_target = value

    @property
    def virtual_target_position_x(self):
        return self.__virtual_target_position_x

    @virtual_target_position_x.setter
    def virtual_target_position_x(self, value):
        self.__virtual_target_position_x = value

    @property
    def virtual_target_position_y(self):
        return self.__virtual_target_position_y

    @virtual_target_position_y.setter
    def virtual_target_position_y(self, value):
        self.__virtual_target_position_y = value

    @property
    def virtual_target_position_z(self):
        return self.__virtual_target_position_z

    @virtual_target_position_z.setter
    def virtual_target_position_z(self, value):
        self.__virtual_target_position_z = value
