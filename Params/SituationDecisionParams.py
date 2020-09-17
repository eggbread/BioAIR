from Drone.State import TentacleState


class SituationDecisionParams(object):
    def __init__(self, config=None):
        """
        Init the SituationDecisionParams
        :param config: Parser.__config
        """
        self.__tentacle_within_pos = -9999
        self.__hold = False

        self.__incomplete_orphan = 0
        self.__incomplete_reinforce = 0
        self.__incomplete_repair = 0
        self.__incomplete_tentacle = 0

        self.__complete_reinforce = 0

        self.__origin_connection = True
        self.__dest_connection = False

        self.__is_anchored = -9999
        self.__is_reinforced = -9999
        self.__anchoring = -9999
        self.__reinforcing = -9999

        self.__extra_on_tentacle = []
        self.__reinforce_on_tentacle = []

        self.__adj_nodes = []

        self.__real_target_detection = False
        self.__real_target_position_x = -9999
        self.__real_target_position_y = -9999
        self.__real_target_position_z = -9999

        self.__adj_origin = 0
        self.__adj_dest = 0
        self.__adj_tip = 0
        self.__adj_backbone = 0
        self.__adj_free = 0
        self.__adj_virtual_origin = 0

        self.__virtual_origin_trigger = False

        self.__next_attractor = -1
        self.__equilibrium = 0

        self.__global_count = 0

        self.__is_new_tip = False

        self.__latest_tentacle_state = None

        self.__hold_timer = 0

        self.__init(config)

    def save(self, config=None):
        """
        save the SituationDecisionParams
        :param config: Parser.__config
        """

        try:
            save_directory = f'../Params/load_file'
            if not (os.path.isdir(save_directory)):
                os.makedirs(os.path.join(save_directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory !")
                raise

    def __init(self, config=None):
        """
        Load the SituationDecisionParams
        :param config: Parser.__config
        :return:
        '''
        config = configparser.ConfigParser()
        config.read(load_file)
        if 'TENTACLE_WITHIN_POS' in config['SituationDecisionParams']:
            self.__tentacle_within_pos = int(config['SituationDecisionParams']['TENTACLE_WITHIN_POS'])

        if 'HOLD' in config['SituationDecisionParams']:
            hold = config['SituationDecisionParams']['HOLD']
            if hold == "TRUE":
                self.__hold = True
            else:
                self.__hold = False

        if 'INCOMPLETE_ORPHAN' in config['SituationDecisionParams']:
            self.__incomplete_orphan = int(config['SituationDecisionParams']['INCOMPLETE_ORPHAN'])

        if 'INCOMPLETE_REINFORCE' in config['SituationDecisionParams']:
            self.__incomplete_reinforce = int(config['SituationDecisionParams']['INCOMPLETE_REINFORCE'])

        if 'INCOMPLETE_REPAIR' in config['SituationDecisionParams']:
            self.__incomplete_repair = int(config['SituationDecisionParams']['INCOMPLETE_REPAIR'])

        if 'INCOMPLETE_TENTACLE' in config['SituationDecisionParams']:
            self.__incomplete_repair = int(config['SituationDecisionParams']['INCOMPLETE_TENTACLE'])

        if 'COMPLETE_REINFORCE' in config['SituationDecisionParams']:
            self.__complete_reinforce = int(config['SituationDecisionParams']['COMPLETE_REINFORCE'])

        if 'ORIGIN_CONNECTION' in config['SituationDecisionParams']:
            origin_connection = config['SituationDecisionParams']['ORIGIN_CONNECTION']
            if origin_connection == 'TRUE':
                self.__origin_connection = True
            else:
                self.__origin_connection = False

        if 'DEST_CONNECTION' in config['SituationDecisionParams']:
            dest_conncection = config['SituationDecisionParams']['DEST_CONNECTION']
            if dest_conncection == "TRUE":
                self.__dest_connection = True
            else:
                self.__dest_connection = False

        if 'IS_ANCHORED' in config['SituationDecisionParams']:
            is_anchored = int(config['SituationDecisionParams']['IS_ANCHORED'])

        if 'IS_REINFORCED' in config['SituationDecisionParams']:
            is_reinforced = int(config['SituationDecisionParams']['IS_REINFORCED'])

        if 'ANCHORING' in config['SituationDecisionParams']:
            self.__anchoring = int(config['SituationDecisionParams']['ANCHORING'])

        if 'REINFORCING' in config['SituationDecisionParams']:
            self.__reinforcing = int(config['SituationDecisionParams']['REINFORCING'])

        if 'EXTRA_ON_TENTACLE' in config['SituationDecisionParams']:
            string_list = config['SituationDecisionParams']['EXTRA_ON_TENTACLE']
            if string_list == "[]":
                self.__extra_on_tentacle = []
            else:
                self.__extra_on_tentacle = [int(x) for x in list(string_list.strip("[").strip("]").split(","))]

        if 'REINFORCE_ON_TENTACLE' in config['SituationDecisionParams']:
            string_list = config['SituationDecisionParams']['REINFORCE_ON_TENTACLE']
            if string_list == "[]":
                self.__reinforce_on_tentacle = []
            else:
                self.__reinforce_on_tentacle = [int(x) for x in list(string_list.strip("[").strip("]").split(","))]

        if 'ADJ_NODES' in config['SituationDecisionParams']:
            string_list = config['SituationDecisionParams']['ADJ_NODES']
            if string_list == "[]":
                self.__adj_nodes = []
            else:
                self.__adj_nodes = [int(x) for x in list(string_list.strip("[").strip("]").split(","))]

        if 'REAL_TARGET_DETECTION' in config['SituationDecisionParams']:
            real_target_detection = config['SituationDecisionParams']['REAL_TARGET_DETECTION']
            if real_target_detection == "TRUE":
                self.__real_target_detection = True
            else:
                self.__real_target_detection = False
        if 'REAL_TARGET_POSITION_X' in config['SituationDecisionParams']:
            self.__real_target_position_x = int(config['SituationDecisionParams']['REAL_TARGET_POSITION_X'])

        if 'REAL_TARGET_POSITION_Y' in config['SituationDecisionParams']:
            self.__real_target_position_y = int(config['SituationDecisionParams']['REAL_TARGET_POSITION_Y'])

        if 'REAL_TARGET_POSITION_Z' in config['SituationDecisionParams']:
            self.__real_target_position_z = int(config['SituationDecisionParams']['REAL_TARGET_POSITION_Z'])

        if 'ADJ_ORIGIN' in config['SituationDecisionParams']:
            self.__adj_origin = int(config['SituationDecisionParams']['ADJ_ORIGIN'])

        if 'ADJ_DEST' in config['SituationDecisionParams']:
            self.__adj_dest = int(config['SituationDecisionParams']['ADJ_DEST'])

        if 'ADJ_TIP' in config['SituationDecisionParams']:
            self.__adj_tip = int(config['SituationDecisionParams']['ADJ_TIP'])

        if 'ADJ_BACKBONE' in config['SituationDecisionParams']:
            self.__adj_backbone = int(config['SituationDecisionParams']['ADJ_BACKBONE'])

        if 'ADJ_FREE' in config['SituationDecisionParams']:
            self.__adj_free = int(config['SituationDecisionParams']['ADJ_FREE'])

        if 'ADJ_VIRTUAL_ORIGIN' in config['SituationDecisionParams']:
            self.__adj_virtual_origin = int(config['SituationDecisionParams']['ADJ_VIRTUAL_ORIGIN'])

        if 'VIRTUAL_ORIGIN_TRIGGER' in config['SituationDecisionParams']:
            virtual_origin_trigger = config['SituationDecisionParams']['VIRTUAL_ORIGIN_TRIGGER']
            if virtual_origin_trigger == "TRUE":
                self.__virtual_origin_trigger = True
            else:
                self.__virtual_origin_trigger = False

        if 'NEXT_ATTRACTOR' in config['SituationDecisionParams']:
            self.__next_attractor = int(config['SituationDecisionParams']['NEXT_ATTRACTOR'])

        if 'EQUILIBRIUM' in config['SituationDecisionParams']:
            self.__equilibrium = int(config['SituationDecisionParams']['EQUILIBRIUM'])

    @property
    def tentacle_within_pos(self):
        return self.__tentacle_within_pos

    @tentacle_within_pos.setter
    def tentacle_within_pos(self, value):
        self.__tentacle_within_pos = value

    @property
    def hold(self):
        return self.__hold

    @hold.setter
    def hold(self, value):
        self.__hold = value

    @property
    def incomplete_orphan(self):
        return self.__incomplete_orphan

    @incomplete_orphan.setter
    def incomplete_orphan(self, value):
        self.__incomplete_orphan = value

    @property
    def incomplete_reinforce(self):
        return self.__incomplete_reinforce

    @incomplete_reinforce.setter
    def incomplete_reinforce(self, value):
        self.__incomplete_reinforce = value

    @property
    def incomplete_repair(self):
        return self.__incomplete_repair

    @incomplete_repair.setter
    def incomplete_repair(self, value):
        self.__incomplete_repair = value

    @property
    def incomplete_tentacle(self):
        return self.__incomplete_tentacle

    @incomplete_tentacle.setter
    def incomplete_tentacle(self, value):
        self.__incomplete_tentacle = value

    @property
    def origin_connection(self):
        return self.__origin_connection

    @origin_connection.setter
    def origin_connection(self, value):
        self.__origin_connection = value

    @property
    def dest_connection(self):
        return self.__dest_connection

    @dest_connection.setter
    def dest_connection(self, value):
        self.__dest_connection = value

    @property
    def is_anchored(self):
        return self.__is_anchored

    @is_anchored.setter
    def is_anchored(self, value):
        self.__is_anchored = value

    @property
    def is_reinforced(self):
        return self.__is_reinforced

    @is_reinforced.setter
    def is_reinforced(self, value):
        self.__is_reinforced = value

    @property
    def anchoring(self):
        return self.__anchoring

    @anchoring.setter
    def anchoring(self, value):
        self.__anchoring = value

    @property
    def reinforcing(self):
        return self.__reinforcing

    @reinforcing.setter
    def reinforcing(self, value):
        self.__reinforcing = value

    @property
    def extra_on_tentacle(self):
        return self.__extra_on_tentacle

    @extra_on_tentacle.setter
    def extra_on_tentacle(self, value):
        self.__extra_on_tentacle = value

    @property
    def reinforce_on_tentacle(self):
        return self.__reinforce_on_tentacle

    @reinforce_on_tentacle.setter
    def reinforce_on_tentacle(self, value):
        self.__reinforce_on_tentacle = value

    @property
    def adj_nodes(self):
        return self.__adj_nodes

    @adj_nodes.setter
    def adj_nodes(self, value):
        self.__adj_nodes = value

    @property
    def real_target_detection(self):
        return self.__real_target_detection

    @real_target_detection.setter
    def real_target_detection(self, value):
        self.__real_target_detection = value

    @property
    def real_target_position_x(self):
        return self.__real_target_position_x

    @real_target_position_x.setter
    def real_target_position_x(self, value):
        self.__real_target_position_x = value

    @property
    def real_target_position_y(self):
        return self.__real_target_position_y

    @real_target_position_y.setter
    def real_target_position_y(self, value):
        self.__real_target_position_y = value

    @property
    def real_target_position_z(self):
        return self.__real_target_position_z

    @real_target_position_z.setter
    def real_target_position_z(self, value):
        self.__real_target_position_z = value

    @property
    def adj_origin(self):
        return self.__adj_origin

    @adj_origin.setter
    def adj_origin(self, value):
        self.__adj_origin = value

    @property
    def adj_dest(self):
        return self.__adj_dest

    @adj_dest.setter
    def adj_dest(self, value):
        self.__adj_dest = value

    @property
    def adj_tip(self):
        return self.__adj_tip

    @adj_tip.setter
    def adj_tip(self, value):
        self.__adj_tip = value

    @property
    def adj_backbone(self):
        return self.__adj_backbone

    @adj_backbone.setter
    def adj_backbone(self, value):
        self.__adj_backbone = value

    @property
    def adj_free(self):
        return self.__adj_free

    @adj_free.setter
    def adj_free(self, value):
        self.__adj_free = value

    @property
    def next_attractor(self):
        return self.__next_attractor

    @next_attractor.setter
    def next_attractor(self, value):
        self.__next_attractor = value

    @property
    def equilibrium(self):
        return self.__equilibrium

    @equilibrium.setter
    def equilibrium(self, value):
        self.__equilibrium = value

    @property
    def global_count(self):
        return self.__global_count

    @global_count.setter
    def global_count(self, value):
        self.__global_count = value

    @property
    def is_new_tip(self):
        return self.__is_new_tip

    @is_new_tip.setter
    def is_new_tip(self, value):
        self.__is_new_tip = value

    @property
    def complete_reinforce(self):
        return self.__complete_reinforce

    @complete_reinforce.setter
    def complete_reinforce(self, value):
        self.__complete_reinforce = value

    @property
    def latest_tentacle_state(self):
        return self.__latest_tentacle_state

    @latest_tentacle_state.setter
    def latest_tentacle_state(self, value):
        self.__latest_tentacle_state = value

    @property
    def hold_timer(self):
        return self.__hold_timer

    @hold_timer.setter
    def hold_timer(self, value):
        self.__hold_timer = value

    @property
    def adj_virtual_origin(self):
        return self.__adj_virtual_origin

    @adj_virtual_origin.setter
    def adj_virtual_origin(self, value):
        self.__adj_virtual_origin = value

    @property
    def virtual_origin_trigger(self):
        return self.__virtual_origin_trigger

    @virtual_origin_trigger.setter
    def virtual_origin_trigger(self, value):
        self.__virtual_origin_trigger = value
