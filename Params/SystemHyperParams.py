

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

        if option == 0:
            self.__init(f'{os.path.dirname(__file__)}/init_file/{from_file}')
        elif option == 1:
            self.__load(f'../Params/load_file/{from_file}')

    def save(self, config=None):
        """
        Save the SystemHyperParams
        :param config: Parser.__config
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

    def __init(self, config=None):
        """
        Load the SystemHyperParams
        :param config: Parser.__config
        :return:
        '''
        config = configparser.ConfigParser()
        config.read(load_file)
        if 'WAITTIME' in config['SystemHyperParams']:
            self.__waittime = float(config['SystemHyperParams']['WAITTIME'])

        if 'MAXMSGLENGTH' in config['SystemHyperParams']:
            self.__maxmsglength = int(config['SystemHyperParams']['MAXMSGLENGTH'])

        if 'REPULSOR' in config['SystemHyperParams']:
            self.__repulsor = int(config['SystemHyperParams']['REPULSOR'])

        if 'TARGETPROXIMITY' in config['SystemHyperParams']:
            self.__targetproximity = int(config['SystemHyperParams']['TARGETPROXIMITY'])

        if 'TARGETFORCE' in config['SystemHyperParams']:
            self.__targetforce = int(config['SystemHyperParams']['TARGETFORCE'])

        if 'UNKNOWN' in config['SystemHyperParams']:
            self.__unknown = int(config['SystemHyperParams']['UNKNOWN'])

        if 'COMMSTIMEOUT' in config['SystemHyperParams']:
            self.__commstimeout = int(config['SystemHyperParams']['COMMSTIMEOUT'])

        if 'AVERAGESAMPLE' in config['SystemHyperParams']:
            self.__averagesample = int(config['SystemHyperParams']['AVERAGESAMPLE'])

        if 'PI' in config['SystemHyperParams']:
            self.__pi = float(config['SystemHyperParams']['PI'])

    def __init(self, init_file=None):
        config = configparser.ConfigParser()
        config.read(init_file)
        print(init_file)
        print(config['SystemHyperParams'])
        if 'WAITTIME' in config['SystemHyperParams']:
            self.__waittime = float(config['SystemHyperParams']['WAITTIME'])

        if 'MAXMSGLENGTH' in config['SystemHyperParams']:
            self.__maxmsglength = int(config['SystemHyperParams']['MAXMSGLENGTH'])

        if 'REPULSOR' in config['SystemHyperParams']:
            self.__repulsor = int(config['SystemHyperParams']['REPULSOR'])

        if 'TARGETPROXIMITY' in config['SystemHyperParams']:
            self.__targetproximity = int(config['SystemHyperParams']['TARGETPROXIMITY'])

        if 'TARGETFORCE' in config['SystemHyperParams']:
            self.__targetforce = int(config['SystemHyperParams']['TARGETFORCE'])

        if 'UNKNOWN' in config['SystemHyperParams']:
            self.__unknown = int(config['SystemHyperParams']['UNKNOWN'])

        if 'COMMSTIMEOUT' in config['SystemHyperParams']:
            self.__commstimeout = int(config['SystemHyperParams']['COMMSTIMEOUT'])

        if 'AVERAGESAMPLE' in config['SystemHyperParams']:
            self.__averagesample = int(config['SystemHyperParams']['AVERAGESAMPLE'])

        if 'PI' in config['SystemHyperParams']:
            self.__pi = float(config['SystemHyperParams']['PI'])

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
