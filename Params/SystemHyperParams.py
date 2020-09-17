import configparser
import os
class SystemHyperParams(object):
    def __init__(self, from_file=None, option=0):
        '''
        :param file: init or save file
        :param option: 0 - init , 1 - load
        '''
        self.__waittime = 0.5
        self.__maxmsglength = 4096
        self.__repulsor = 1
        self.__targetproximity = 20
        self.__targetforce = 1
        self.__unknown = -9999
        self.__commstimeout = 15
        self.__averagesample = 5
        self.__pi = 3.141592

        if option == 0:
            self.__init(f'{os.path.dirname(__file__)}/init_file/{from_file}')
        elif option == 1:
            self.__load(f'../Params/load_file/{from_file}')

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
            shp = f"[SystemHyperParams]\n\
WAITTIME = {self.__waittime}\n\
MAXMSGLENGTH = {self.__maxmsglength}\n\
REPULSOR = {self.__repulsor}\n\
TARGETPROXIMITY = {self.__targetproximity}\n\
TARGETFORCE = {self.__targetforce}\n\
UNKNOWN = {self.__unknown}\n\
COMMSTIMEOUT = {self.__commstimeout}\n\
AVERAGESAMPLE = {self.__averagesample}\n\
PI = {self.__pi}"
            f.write(shp)

    def __load(self, load_file=None):
        '''
        load params
        :param save_file: load할 file name
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
    def waittime(self):
        return self.__waittime

    @waittime.setter
    def waittime(self, value):
        self.__waittime = value

    @property
    def maxmsglenghth(self):
        return self.__maxmsglength

    @maxmsglenghth.setter
    def maxmsglenghth(self, value):
        self.__maxmsglength = value

    @property
    def repulsor(self):
        return self.__repulsor

    @repulsor.setter
    def repulsor(self, value):
        self.__repulsor = value

    @property
    def targetproximity(self):
        return self.__targetproximity

    @targetproximity.setter
    def targetproximity(self, value):
        self.__targetproximity = value

    @property
    def targetforce(self):
        return self.__targetforce

    @targetforce.setter
    def targetforce(self, value):
        self.__targetforce = value

    @property
    def unknown(self):
        return self.__unknown

    @unknown.setter
    def unknown(self, value):
        self.__unknown = value

    @property
    def commstimeout(self):
        return self.__commstimeout

    @commstimeout.setter
    def commstimeout(self, value):
        self.__commstimeout = value

    @property
    def averagesample(self):
        return self.__averagesample

    @averagesample.setter
    def averagesample(self, value):
        self.__averagesample = value

    @property
    def pi(self):
        return self.__pi

    @pi.setter
    def pi(self, value):
        self.__pi = value