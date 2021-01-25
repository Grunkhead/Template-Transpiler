import config, os, json

from classes.TemplateFactory import TemplateFactory
from classes.TranspileSettings import TranspileSettings
from models.Template import Template
from helpers import file_helper


class TemplateManager:

    parent_templates = []
    child_templates = []

    def __init__(self):
            
        self.make_default_directories()
        
        self.set_parent_templates()
        TemplateFactory.make_template_files(self.parent_templates)

    def get_templates(self):
        return self.parent_templates + self.child_templates

    def skip_current_component(self, component_directory_name):

        if TranspileSettings.settings_file_exists():

            # Setting implementation: DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES
            if TranspileSettings.setting_enabled('DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES'):
                if (True if component_directory_name in TranspileSettings.load_settings_file()['DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES'] else False):
                    return True

            # Setting implementation: ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES
            if TranspileSettings.setting_enabled('ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES'):
                if (False if component_directory_name in TranspileSettings.load_settings_file()['ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES'] else True):
                    return True

        return False

    # Add the parent templates to the parent template array. Also add to 'all' template array.
    def set_parent_templates(self):

        parent_templates = []

        # Iterate over dynamically named frontend component directories.
        for component_directory_name in os.listdir(config.absolute_frontend_components_directory_path):

            if self.skip_current_component(component_directory_name):
                continue

            absolute_component_path = os.path.join(config.absolute_frontend_components_directory_path, component_directory_name)

            for relative_template_directory_path in config.relative_frontend_template_directory_paths:
                absolute_template_directory_path = absolute_component_path + '/' + relative_template_directory_path

                # Verify if template directory exists.
                if not os.path.isdir(absolute_template_directory_path):
                    continue

                # Create final path with template name behind it.
                for parent_template_name in self.get_html_templates_from_directory(absolute_template_directory_path):

                    parent_template_content = file_helper.read_file_content(absolute_template_directory_path + '/' + parent_template_name)
                    parent_template_name = file_helper.remove_file_name_extensions(parent_template_name)

                    parent_template = TemplateFactory.create_template(parent_template_name, parent_template_content)
                    parent_template.child_templates = self.get_child_templates(absolute_template_directory_path, parent_template)

                    parent_templates.append(parent_template)
                    self.parent_templates.append(parent_template)        

    # Add the child template, to the parent template. Also add to 'all' template array.
    def get_child_templates(self, absolute_template_directory_path, parent_template):

        child_templates = []

        child_template_names = self.get_html_templates_from_directory(absolute_template_directory_path + '/' + parent_template.name)

        if child_template_names:
            for child_template_name in child_template_names:

                child_template_content = file_helper.read_file_content(absolute_template_directory_path + '/' + parent_template.name + '/' + child_template_name)
                child_template_name = file_helper.remove_file_name_extensions(child_template_name)
                
                child_template = TemplateFactory.create_template(child_template_name, child_template_content)

                child_template.parent = parent_template

                child_templates.append(child_template)
                self.child_templates.append(child_template)

        return child_templates

    # Only get .html templates from directory.
    def get_html_templates_from_directory(self, directory_path):

        templates = []

        if not os.path.isdir(directory_path):
            return

        for file in os.listdir(directory_path):
            if not file.endswith('.html'):
                continue

            templates.append(file)

        return templates

    # Make default directories that have been given in the config array.
    def make_default_directories(self):

        for absolute_default_directory_path in config.absolute_default_directory_paths:
            if not os.path.isdir(absolute_default_directory_path):
                os.mkdir(absolute_default_directory_path)