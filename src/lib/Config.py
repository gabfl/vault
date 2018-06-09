import configparser
import os
from uuid import uuid4


class Config:

    # Config file location
    config_path = None

    # Config
    config = configparser.ConfigParser()

    def __init__(self, config_path):
        self.config_path = config_path

    def get_config(self):
        """
            Will return a user config and set a default if necessary
        """

        # Generate a default config the first time
        if not os.path.isfile(self.config_path):
            self.set_default_config_file()

        # Load existing config
        self.config.read(self.config_path)
        return self.config['MAIN']

    def set_default_config_file(self):
        """
            Set a user default config file
        """

        self.config['MAIN'] = {
            'version': '2.00',
            'keyVersion': '1',  # Will be used to support legacy key versions if the algorithm changes
            'salt': self.generate_random_salt(),
            'clipboardTTL': '15',
            'hideSecretTTL': '5',
            'autoLockTTL': '900',
            'encryptedDb': True,
        }

        # Save
        self.save_config()

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
        return self.save_config()

    def save_config(self):
        """
            Save user config to a file
        """

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        os.chmod(self.config_path, 0o600)

        return True

    def generate_random_salt(self):
        """
            Generate a random salt
            Will be used to generate the vault hash with the user master key
        """

        return str(uuid4())

    def __getattr__(self, name):
        """
            Allows calls to configuration values:
            config = Config()
            print(config.salt) # Will print the salt
        """

        try:
            return self.get_config()[name]
        except KeyError:  # For values that don't exist in the config file
            return None
