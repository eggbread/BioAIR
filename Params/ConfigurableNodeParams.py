import configparser
import os
from Drone.State import NodeState,TentacleState
class ConfigurableNodeParams(object):
    def __init__(self, from_file=None, option=0):
        '''
        :param file: init or save file
        :param option: 0 - init , 1 - load
        '''
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

        self.__virtual_target = -1  #  -1 : off / 0 : on / node_id : virtual_origin
        self.__virtual_target_position_x = 0
        self.__virtual_target_position_y = 0
        self.__virtual_target_position_z = 0

        if option == 0:
            
            self.__init(f'{os.path.dirname(__file__)}/init_file/{from_file}')
        elif option == 1:
            self.__load(f'{os.path.dirname(__file__)}/load_file/{from_file}')

    def save(self, save_file=None):
        '''
        save params
        :param save_file: save할 file name
        :return:
        '''

        try:
            save_directory = f'../Params/load_file'
            if not (os.path.isdir(save_directory)):
                os.makedirs(os.path.join(save_directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory !")
                raise

        with open(f'../Params/load_file/{save_file}', mode="w", encoding="utf-8") as f:
            cnp = f"[ConfigurableNodeParams]\n\
IP = {self.__ip}\n\
MAC = {self.__mac}\n\
PORT = {self.__port}\n\
NODE_ID = {self.__node_id}\n\
TENTACLE_ID = {self.__tentacle_id}\n\
NODE_STATE = {self.__node_state_to_str(self.__node_state)}\n\
TENTACLE_STATE = {self.__tentacle_state_to_str(self.__tentacle_state)}\n\
POSITION_X = {self.__position_x}\n\
POSITION_Y = {self.__position_y}\n\
POSITION_Z = {self.__position_z}\n\
ORIGIN_ID = {self.__origin_id}\n\
ORIGIN_POSITION_X = {self.__origin_position_x}\n\
ORIGIN_POSITION_Y = {self.__origin_position_y}\n\
ORIGIN_POSITION_Z = {self.__origin_position_z}\n\
DEST_ID = {self.__dest_id}\n\
DEST_POSITION_X = {self.__dest_position_x}\n\
DEST_POSITION_Y = {self.__dest_position_y}\n\
DEST_POSITION_Z = {self.__dest_position_z}\n\
PREV_VEL_X = {self.__prev_vel_x}\n\
PREV_VEL_Y = {self.__prev_vel_y}\n\
PREV_VEL_Z = {self.__prev_vel_z}\n\
NEXT_VEL_X = {self.__next_vel_x}\n\
NEXT_VEL_Y = {self.__next_vel_y}\n\
NEXT_VEL_Z = {self.__next_vel_z}\n\
HIGH_SQ = {self.__high_sq}\n\
LOW_SQ = {self.__low_sq}\n\
EQUILIBRIUM_ZONE = {self.__equilibrium_zone}\n\
RADIO_RANGE = {self.__radio_range}\n\
HAS_SENSOR = {str(self.__has_sensor).upper()}\n\
VIRTUAL_TARGET = {self.__virtual_target}\n\
VIRTUAL_TARGET_POSITION_X = {self.__virtual_target_position_x}\n\
VIRTUAL_TARGET_POSITION_Y = {self.__virtual_target_position_y}\n\
VIRTUAL_TARGET_POSITION_Z = {self.__virtual_target_position_z}\n"
            f.write(cnp)

    def __load(self, load_file=None):
        '''
        load params
        :param save_file: load할 file name
        :return:
        '''
        config = configparser.ConfigParser()
        config.read(load_file)
        if 'IP' in config['ConfigurableNodeParams']:
            self.__ip = config['ConfigurableNodeParams']['IP']

        if 'MAC' in config['ConfigurableNodeParams']:
            self.__mac = config['ConfigurableNodeParams']['MAC']

        if 'PORT' in config['ConfigurableNodeParams']:
            self.__port = int(config['ConfigurableNodeParams']['PORT'])

        if 'NODE_ID' in config['ConfigurableNodeParams']:
            self.__node_id = int(config['ConfigurableNodeParams']['NODE_ID'])

        if 'TENTACLE_ID' in config['ConfigurableNodeParams']:
            self.__tentacle_id = int(config['ConfigurableNodeParams']['TENTACLE_ID'])

        if 'NODE_STATE' in config['ConfigurableNodeParams']:
            self.__node_state = self.__str_to_node_state(config['ConfigurableNodeParams']['NODE_STATE'])

        if 'TENTACLE_STATE' in config['ConfigurableNodeParams']:
            self.__tentacle_state = self.__str_to_tentacle_state(config['ConfigurableNodeParams']['TENTACLE_STATE'])

        if 'POSITION_X' in config['ConfigurableNodeParams']:
            self.__position_x = float(config['ConfigurableNodeParams']['POSITION_X'])

        if 'POSITION_Y' in config['ConfigurableNodeParams']:
            self.__position_y = float(config['ConfigurableNodeParams']['POSITION_Y'])

        if 'POSITION_Z' in config['ConfigurableNodeParams']:
            self.__position_z = float(config['ConfigurableNodeParams']['POSITION_Z'])

        if 'ORIGIN_ID' in config['ConfigurableNodeParams']:
            self.__origin_id = int(config['ConfigurableNodeParams']['ORIGIN_ID'])

        if 'DEST_POSITION_X' in config['ConfigurableNodeParams']:
            self.__origin_position_x = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_X'])

        if 'DEST_POSITION_Y' in config['ConfigurableNodeParams']:
            self.__origin_position_y = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_Y'])

        if 'DEST_POSITION_Z' in config['ConfigurableNodeParams']:
            self.__origin_position_z = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_Z'])

        if 'DEST_ID' in config['ConfigurableNodeParams']:
            self.__dest_id = int(config['ConfigurableNodeParams']['DEST_ID'])

        if 'DEST_POSITION_X' in config['ConfigurableNodeParams']:
            self.__dest_position_x = int(config['ConfigurableNodeParams']['DEST_POSITION_X'])

        if 'DEST_POSITION_Y' in config['ConfigurableNodeParams']:
            self.__dest_position_y = int(config['ConfigurableNodeParams']['DEST_POSITION_Y'])

        if 'DEST_POSITION_Z' in config['ConfigurableNodeParams']:
            self.__dest_position_z = int(config['ConfigurableNodeParams']['DEST_POSITION_Z'])

        if 'PREV_VEL_X' in config['ConfigurableNodeParams']:
            self.__prev_vel_x = float(config['ConfigurableNodeParams']['PREV_VEL_X'])

        if 'PREV_VEL_Y' in config['ConfigurableNodeParams']:
            self.__prev_vel_y = float(config['ConfigurableNodeParams']['PREV_VEL_Y'])

        if 'PREV_VEL_Z' in config['ConfigurableNodeParams']:
            self.__prev_vel_z = float(config['ConfigurableNodeParams']['PREV_VEL_Z'])

        if 'NEXT_VEL_X' in config['ConfigurableNodeParams']:
            self.__next_vel_x = float(config['ConfigurableNodeParams']['NEXT_VEL_X'])

        if 'NEXT_VEL_Y' in config['ConfigurableNodeParams']:
            self.__next_vel_y = float(config['ConfigurableNodeParams']['NEXT_VEL_Y'])

        if 'NEXT_VEL_Z' in config['ConfigurableNodeParams']:
            self.__next_vel_z = float(config['ConfigurableNodeParams']['NEXT_VEL_Z'])

        if 'HIGH_SQ' in config['ConfigurableNodeParams']:
            self.__high_sq = float(config['ConfigurableNodeParams']['HIGH_SQ'])

        if 'LOW_SQ' in config['ConfigurableNodeParams']:
            self.__low_sq = float(config['ConfigurableNodeParams']['LOW_SQ'])

        if 'EQUILIBRIUM_ZONE' in config['ConfigurableNodeParams']:
            self.__equilibrium_zone = float(config['ConfigurableNodeParams']['EQUILIBRIUM_ZONE'])

        if 'RADIO_RANGE' in config['ConfigurableNodeParams']:
            self.__radio_range= int(config['ConfigurableNodeParams']['RADIO_RANGE'])

        if 'HAS_SENSOR' in config['ConfigurableNodeParams']:
            has_sensor = config['ConfigurableNodeParams']['HAS_SENSOR']
            if has_sensor == "TRUE":
                self.__has_sensor = True
            else:
                self.__has_sensor = False

        if 'VIRTUAL_TARGET' in config['ConfigurableNodeParams']:
            self.__virtual_target = int(config['ConfigurableNodeParams']['VIRTUAL_TARGET'])

        if 'VIRTUAL_TARGET_POSITION_X' in config['ConfigurableNodeParams']:
            self.__virtual_target_position_x = int(config['ConfigurableNodeParams']['VIRTUAL_TARGET_POSITION_X'])

        if 'VIRTUAL_TARGET_POSITION_Y' in config['ConfigurableNodeParams']:
            self.__virtual_target_position_y = int(config['ConfigurableNodeParams']['VIRTUAL_TARGET_POSITION_Y'])

        if 'VIRTUAL_TARGET_POSITION_Z' in config['ConfigurableNodeParams']:
            self.__virtual_target_position_z = int(config['ConfigurableNodeParams']['VIRTUAL_TARGET_POSITION_Z'])

    def __init(self, init_file=None):
        config = configparser.ConfigParser()
        config.read(init_file)
        if 'IP' in config['ConfigurableNodeParams']:
            self.__ip = config['ConfigurableNodeParams']['IP']

        if 'MAC' in config['ConfigurableNodeParams']:
            self.__mac = config['ConfigurableNodeParams']['MAC']

        if 'PORT' in config['ConfigurableNodeParams']:
            self.__port = int(config['ConfigurableNodeParams']['PORT'])

        if 'NODE_ID' in config['ConfigurableNodeParams']:
            self.__node_id = int(config['ConfigurableNodeParams']['NODE_ID'])

        if 'TENTACLE_ID' in config['ConfigurableNodeParams']:
            self.__tentacle_id = int(config['ConfigurableNodeParams']['TENTACLE_ID'])

        if 'NODE_STATE' in config['ConfigurableNodeParams']:
            self.__node_state = self.__str_to_node_state(config['ConfigurableNodeParams']['NODE_STATE'])

        if 'TENTACLE_STATE' in config['ConfigurableNodeParams']:
            self.__tentacle_state = self.__str_to_tentacle_state(config['ConfigurableNodeParams']['TENTACLE_STATE'])

        if 'POSITION_X' in config['ConfigurableNodeParams']:
            self.__position_x = int(config['ConfigurableNodeParams']['POSITION_X'])

        if 'POSITION_Y' in config['ConfigurableNodeParams']:
            self.__position_y = int(config['ConfigurableNodeParams']['POSITION_Y'])

        if 'POSITION_Z' in config['ConfigurableNodeParams']:
            self.__position_z = int(config['ConfigurableNodeParams']['POSITION_Z'])

        if 'ORIGIN_ID' in config['ConfigurableNodeParams']:
            self.__origin_id = int(config['ConfigurableNodeParams']['ORIGIN_ID'])

        if 'DEST_POSITION_X' in config['ConfigurableNodeParams']:
            self.__origin_position_x = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_X'])

        if 'DEST_POSITION_Y' in config['ConfigurableNodeParams']:
            self.__origin_position_y = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_Y'])

        if 'DEST_POSITION_Z' in config['ConfigurableNodeParams']:
            self.__origin_position_z = int(config['ConfigurableNodeParams']['ORIGIN_POSITION_Z'])

        if 'DEST_ID' in config['ConfigurableNodeParams']:
            self.__dest_id = int(config['ConfigurableNodeParams']['DEST_ID'])

        if 'DEST_POSITION_X' in config['ConfigurableNodeParams']:
            self.__dest_position_x = int(config['ConfigurableNodeParams']['DEST_POSITION_X'])

        if 'DEST_POSITION_Y' in config['ConfigurableNodeParams']:
            self.__dest_position_y = int(config['ConfigurableNodeParams']['DEST_POSITION_Y'])

        if 'DEST_POSITION_Z' in config['ConfigurableNodeParams']:
            self.__dest_position_z = int(config['ConfigurableNodeParams']['DEST_POSITION_Z'])

        if 'PREV_VEL_X' in config['ConfigurableNodeParams']:
            self.__prev_vel_x = float(config['ConfigurableNodeParams']['PREV_VEL_X'])

        if 'PREV_VEL_Y' in config['ConfigurableNodeParams']:
            self.__prev_vel_y = float(config['ConfigurableNodeParams']['PREV_VEL_Y'])

        if 'PREV_VEL_Z' in config['ConfigurableNodeParams']:
            self.__prev_vel_z = float(config['ConfigurableNodeParams']['PREV_VEL_Z'])

        if 'NEXT_VEL_X' in config['ConfigurableNodeParams']:
            self.__next_vel_x = float(config['ConfigurableNodeParams']['NEXT_VEL_X'])

        if 'NEXT_VEL_Y' in config['ConfigurableNodeParams']:
            self.__next_vel_y = float(config['ConfigurableNodeParams']['NEXT_VEL_Y'])

        if 'NEXT_VEL_Z' in config['ConfigurableNodeParams']:
            self.__next_vel_z = float(config['ConfigurableNodeParams']['NEXT_VEL_Z'])

        if 'HIGH_SQ' in config['ConfigurableNodeParams']:
            self.__high_sq = float(config['ConfigurableNodeParams']['HIGH_SQ'])

        if 'LOW_SQ' in config['ConfigurableNodeParams']:
            self.__low_sq = float(config['ConfigurableNodeParams']['LOW_SQ'])

        if 'EQUILIBRIUM_ZONE' in config['ConfigurableNodeParams']:
            self.__equilibrium_zone = float(config['ConfigurableNodeParams']['EQUILIBRIUM_ZONE'])

        if 'RADIO_RANGE' in config['ConfigurableNodeParams']:
            self.__radio_range= int(config['ConfigurableNodeParams']['RADIO_RANGE'])

        if 'HAS_SENSOR' in config['ConfigurableNodeParams']:
            has_sensor = config['ConfigurableNodeParams']['HAS_SENSOR']
            if has_sensor == "TRUE":
                self.__has_sensor = True
            else:
                self.__has_sensor = False

    def __str_to_node_state(self,str):
        if (str == "FREE"):
            return NodeState.Free
        if (str == "TIP"):
            return NodeState.Tip
        if (str == "BACKBONE"):
            return NodeState.Backbone
        if (str == "EXTRA"):
            return NodeState.Extra
        if (str == "REINFORCE"):
            return NodeState.Reinforce
        if (str == "ORPHAN"):
            return NodeState.Orphan
        if (str == "ORIGIN"):
            return NodeState.Origin
        if (str == "DEST"):
            return NodeState.Destination
        if (str == "TARGET"):
            return NodeState.Target

    def __node_state_to_str(self,node_state):

        if node_state is NodeState.Free:
            return "FREE"
        if node_state is NodeState.Tip:
            return "TIP"
        if node_state is NodeState.Backbone:
            return "BACKBONE"
        if node_state is NodeState.Extra:
            return "EXTRA"
        if node_state is NodeState.Reinforce:
            return "REINFORCE"
        if node_state is NodeState.Orphan:
            return "ORPHAN"
        if node_state is NodeState.Origin:
            return "ORIGIN"
        if node_state is NodeState.Destination:
            return "DEST"

    def __str_to_tentacle_state(self,str):
        if (str == "FORMING"):
            return TentacleState.Forming
        if (str == "COMPLETE"):
            return TentacleState.Complete
        if (str == "DAMAGED"):
            return TentacleState.Damaged
        if (str == "REINFORCING"):
            return TentacleState.Reinforcing
        if (str == "NEXT_DEST"):
            return TentacleState.Next_Destination

    def __tentacle_state_to_str(self,tentacle_state):
        if tentacle_state is TentacleState.Forming:
            return "FORMING"
        if tentacle_state is TentacleState.Complete:
            return "COMPLETE"
        if tentacle_state is TentacleState.Damaged:
            return "DAMAGED"
        if tentacle_state is TentacleState.Reinforcing:
            return "REINFORCING"
        if tentacle_state is TentacleState.Next_Destination:
            return "NEXT_DEST"
        if tentacle_state is None:
            return "None"

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