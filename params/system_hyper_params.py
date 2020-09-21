

class SystemHyperParams(object):
    def __init__(self, config=None):
        """
        Init the SystemHyperParams
        :param config: Parser.__config
        """
        self.__wait_time = 0.5
        self.__max_msg_length = 4096
        self.__repulsor = 1
        self.__target_proximity = 20
        self.__target_force = 1
        self.__unknown = -9999
        self.__comms_timeout = 15
        self.__average_sample = 5
        self.__pi = 3.141592

        self.__init(config)

    def save(self, config=None):
        """
        Save the SystemHyperParams
        :param config: Parser.__config
        :return:
        """
        config['SystemHyperParams'] = {
            'waittime': self.__wait_time,
            'maxmsglength': self.__max_msg_length,
            'repulsor': self.__repulsor,
            'targetproximity': self.__target_proximity,
            'targetforce': self.__target_force,
            'unknown': self.__unknown,
            'commstimeout': self.__comms_timeout,
            'averagesample': self.__average_sample,
            'pi': self.__pi,
        }

    def __init(self, config=None):
        """
        Load the SystemHyperParams
        :param config: Parser.__config
        :return:
        """
        if 'waittime' in config['SystemHyperParams']:
            self.__wait_time = float(config['SystemHyperParams']['waittime'])

        if 'maxmsglength' in config['SystemHyperParams']:
            self.__max_msg_length = int(config['SystemHyperParams']['maxmsglength'])

        if 'repulsor' in config['SystemHyperParams']:
            self.__repulsor = int(config['SystemHyperParams']['repulsor'])

        if 'targetproximity' in config['SystemHyperParams']:
            self.__target_proximity = int(config['SystemHyperParams']['targetproximity'])

        if 'targetforce' in config['SystemHyperParams']:
            self.__target_force = int(config['SystemHyperParams']['targetforce'])

        if 'unknown' in config['SystemHyperParams']:
            self.__unknown = int(config['SystemHyperParams']['unknown'])

        if 'commstimeout' in config['SystemHyperParams']:
            self.__comms_timeout = int(config['SystemHyperParams']['commstimeout'])

        if 'averagesample' in config['SystemHyperParams']:
            self.__average_sample = int(config['SystemHyperParams']['averagesample'])

        if 'pi' in config['SystemHyperParams']:
            self.__pi = float(config['SystemHyperParams']['pi'])

    @property
    def wait_time(self):
        return self.__wait_time

    @wait_time.setter
    def wait_time(self, value):
        self.__wait_time = value

    @property
    def max_msg_length(self):
        return self.__max_msg_length

    @max_msg_length.setter
    def max_msg_length(self, value):
        self.__max_msg_length = value

    @property
    def repulsor(self):
        return self.__repulsor

    @repulsor.setter
    def repulsor(self, value):
        self.__repulsor = value

    @property
    def target_proximity(self):
        return self.__target_proximity

    @target_proximity.setter
    def target_proximity(self, value):
        self.__target_proximity = value

    @property
    def target_force(self):
        return self.__target_force

    @target_force.setter
    def target_force(self, value):
        self.__target_force = value

    @property
    def unknown(self):
        return self.__unknown

    @unknown.setter
    def unknown(self, value):
        self.__unknown = value

    @property
    def comms_timeout(self):
        return self.__comms_timeout

    @comms_timeout.setter
    def comms_timeout(self, value):
        self.__comms_timeout = value

    @property
    def average_sample(self):
        return self.__average_sample

    @average_sample.setter
    def average_sample(self, value):
        self.__average_sample = value

    @property
    def pi(self):
        return self.__pi

    @pi.setter
    def pi(self, value):
        self.__pi = value
