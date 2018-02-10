import sys
import yaml


class StationConfig:
    """Configuration parser"""
    def __init__(self, file='config.yaml'):
        with open(file, 'r') as ymlfile:
            try:
                self.configs = yaml.load(ymlfile)
            except yaml.YAMLError as exc:
                sys.exit("Fatal: Config file cannot be parsed as correct YAML")
