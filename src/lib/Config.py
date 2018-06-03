import configparser
import os
from uuid import uuid4


class Config:

    # Config file location
    configPath = None

    # Config
    config = configparser.ConfigParser()

    def __init__(self, configPath):
        self.configPath = configPath

    def getConfig(self):
        """
            Will return a user config and set a default if necessary
        """

        # Generate a default config the first time
        if not os.path.isfile(self.configPath):
            self.setDefaultConfigFile()

        # Load existing config
        self.config.read(self.configPath)
        return self.config['MAIN']

    def setDefaultConfigFile(self):
        """
            Set a user default config file
        """

        self.config['MAIN'] = {
            'version': '2.00',
            'keyVersion': '1',  # Will be used to support legacy key versions if the algorithm changes
            'salt': self.generateRandomSalt(),
            'clipboardTTL': '15',
            'hideSecretTTL': '5',
            'autoLockTTL': '900',
            'encryptedDb': True,
        }

        # Save
        self.saveConfig()

    def update(self, name, value):
        """
            Update a config value
        """

        # Set new value
        self.config['MAIN'][name] = str(value)

        print()
        print('The setting `%s` is now set to `%s`.' % (name, value))
        print()

        # Save
        return self.saveConfig()

    def saveConfig(self):
        """
            Save user config to a file
        """

        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)
        os.chmod(self.configPath, 0o600)

        return True

    def generateRandomSalt(self):
        """
            Generate a random salt
            Will be used to generate the vault hash with the user master key
        """

        return str(uuid4())
