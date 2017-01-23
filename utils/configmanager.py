import sys
from os import path

if sys.version_info[0] < 3:
    # Python 2 uses this module
    from ConfigParser import ConfigParser
else:
    # Python 3 uses this module
    from configParser import ConfigParser


class ConfigManager:
    """
    Manages config file contents
    """

    def __init__(self, filepath):
        """
        Creates ConfigManager instance.
        :param filepath: File path
        """
        if not path.exists(filepath):
            raise OSError("The file %s does not exist." % filepath)
        elif not path.isfile(filepath):
            raise OSError("%s is not a file." % filepath)
        self.filepath = filepath
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(filepath)

    def parse(self):
        # type: () -> dict
        """
        Parses the contents of the config file into a dictionary. Skips empty values.

        TODO: CURO-10855 Move config sections out to models.

        :return: A dictionary with subsections representing each section of the config file.
        """
        info = {}
        for section in self.config.sections():
            cfg_item = {}
            for item in self.config.items(section):
                if item[1]:
                    cfg_item[item[0]] = item[1]
            info[section] = cfg_item
        return info

