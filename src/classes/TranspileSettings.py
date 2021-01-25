import config, os, json

from classes.Message import Message


class TranspileSettings:

    settings_file_path = config.absolute_frontend_components_directory_path + '/'
    settings_file_name = 'transpiler-settings.json'

    @classmethod
    def get_settings_file_path(cls):
        return cls.settings_file_path

    @classmethod
    def get_settings_file_name(cls):
        return cls.settings_file_name

    @classmethod
    def get_settings_file_path_with_name(cls):
        return cls.settings_file_path + cls.settings_file_name

    @classmethod
    def settings_file_exists(cls):
        return bool(os.path.isfile(cls.get_settings_file_path_with_name()))

    @classmethod
    def load_settings_file(cls):

        try:
            with open(cls.get_settings_file_path_with_name()) as json_file:
                return json.load(json_file)
        except:
            return {}

    @classmethod
    def setting_exists(cls, setting):

        # Check if setting file exists.
        if not cls.settings_file_exists():
            return False

        # Check if dictionary with setting switches exists.
        if 'SETTING_ENABLED' not in cls.load_settings_file():
            return False

        # Check if setting switch true / false switch exists.
        if setting not in cls.load_settings_file()['SETTING_ENABLED']:
            return False

        # Check if setting data exists.
        if setting not in cls.load_settings_file():
            return False

        return True

    @classmethod
    def setting_enabled(cls, setting):

        # If setting can not be found, return false.
        if not cls.setting_exists(setting):
            return False

        # Return true / false value of setting switch.
        return cls.load_settings_file()['SETTING_ENABLED'][setting]



