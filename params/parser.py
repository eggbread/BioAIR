import configparser
import os
from .configurable_node_params import ConfigurableNodeParams
from .situation_decision_params import SituationDecisionParams
from .system_hyper_params import SystemHyperParams


class Parser(object):
    def __init__(self, node_id=None, load_option=False):
        self.__config = configparser.ConfigParser()
        self.__node_id = node_id
        load_file = f'{os.path.dirname(__file__)}/load_file/node_{self.__node_id}.ini' \
            if load_option else f'{os.path.dirname(__file__)}/init_file/node_{self.__node_id}.ini'
        self.__config.read(load_file)
        self.__configurable_node_params = ConfigurableNodeParams(self.__config)
        self.__system_hyper_params = SystemHyperParams(self.__config)
        self.__situation_decision_params = SituationDecisionParams(self.__config)

    def save(self):
        try:
            save_directory = f'{os.path.dirname(__file__)}/load_file'
            if not (os.path.isdir(save_directory)):
                os.makedirs(save_directory)
            with open(os.path.join(save_directory, f'node_{self.__node_id}.ini', ), mode='w', encoding='utf-8') as f:
                self.__configurable_node_params.save(self.__config)
                self.__situation_decision_params.save(self.__config)
                self.__system_hyper_params.save(self.__config)
                self.__config.optionxform = lambda option: option.upper()
                self.__config.write(f)
        except OSError as err:
            print("Failed to save the parameters!", err)

    @property
    def configurable_node_params(self):
        return self.__configurable_node_params

    @property
    def system_hyper_params(self):
        return self.__system_hyper_params

    @property
    def situation_decision_params(self):
        return self.__situation_decision_params
