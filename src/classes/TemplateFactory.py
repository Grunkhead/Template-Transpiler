
import config, os

from models.Template import Template

from helpers import file_helper

class TemplateFactory():

    @staticmethod
    def create_template(name, content):
        return Template(name, content)

    @classmethod
    def make_template_files(cls, parent_templates):

        for parent_template in parent_templates:
            cls.make_template(parent_template)

            for child_template in parent_template.child_templates:
                cls.make_template(child_template, parent_template.name)

    # Make template files, prefix name and set their relative import path.
    @classmethod
    def make_template(cls, template, parent_template_name = ''):

        if parent_template_name == 'form-elements' and template.is_child():

            absolute_form_elements_directory_path = config.absolute_output_directory_path + '/' + 'form-elements'

            if not os.path.isdir(absolute_form_elements_directory_path):
                os.mkdir(absolute_form_elements_directory_path)

            target_directory = absolute_form_elements_directory_path
            prefixed_template_name = 'element--' + template.name
            template.set_relative_import_path('form-elements' + '/' + prefixed_template_name + '.html.twig')

        elif template.has_childs():

            if template.contains_macro():
                target_directory = config.absolute_output_directory_path + '/' + parent_template_name
                prefixed_template_name = 'macro--' + template.name
                template.set_relative_import_path(prefixed_template_name + '.html.twig')

            else:
                target_directory = config.absolute_output_directory_path + '/' + 'partials'
                prefixed_template_name = 'partial--' + template.name
                template.set_relative_import_path('partials' + '/' + prefixed_template_name + '.html.twig')

        elif template.contains_macro() and template.is_child():

            absolute_parent_directory_path = config.absolute_output_directory_path + '/' + parent_template_name

            if not os.path.isdir(absolute_parent_directory_path):
                os.mkdir(absolute_parent_directory_path)

            target_directory = absolute_parent_directory_path
            prefixed_template_name = 'macro--' + template.name
            template.set_relative_import_path(parent_template_name + '/' + prefixed_template_name + '.html.twig')

        elif template.contains_macro():
            target_directory = config.absolute_output_directory_path
            prefixed_template_name = 'macro--' + template.name
            template.set_relative_import_path(prefixed_template_name + '.html.twig')

        else:
            target_directory = config.absolute_output_directory_path + '/' + 'partials'
            prefixed_template_name = 'partial--' + template.name
            template.set_relative_import_path('partials' + '/' + prefixed_template_name + '.html.twig')

        file_helper.make_file(
            target_directory + '/' + prefixed_template_name + '.html.twig',
            template.content
        )