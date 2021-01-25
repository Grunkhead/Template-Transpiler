import config, shutil, os

from classes.Message import Message

from datetime import datetime
from helpers import file_helper

from transpile_methods.ModifyTwigCommentsTranspileMethod import ModifyTwigCommentsTranspileMethod
from transpile_methods.FromImportTagTranspileMethod import FromImportTagTranspileMethod
from transpile_methods.FromImportAsTagTranspileMethod import FromImportAsTagTranspileMethod
from transpile_methods.ImportAsTagTranspileMethod import ImportAsTagTranspileMethod
from transpile_methods.IncludeTagTranspileMethod import IncludeTagTranspileMethod
from transpile_methods.ReplaceNunjuckFiltersTranspileMethod import ReplaceNunjuckFiltersTranspileMethod
from transpile_methods.CallerMethodsTranspileMethod import CallerMethodsTranspileMethod
from transpile_methods.MoveImportsTranspileMethod import MoveImportsTranspileMethod
from transpile_methods.SvgTagTranspileMethod import SvgTagTranspileMethod
from transpile_methods.InjectCommentedTwigCodeTranspileMethod import InjectCommentedTwigCodeTranspileMethod


class TemplateTranspiler:

    transpile_methods = [

        # Inject commented twig code.
        InjectCommentedTwigCodeTranspileMethod,

        # First disable tags inside twig comments so the regexes don't fail. 
        ModifyTwigCommentsTranspileMethod,

        # Then transpile the import / include tags.
        FromImportAsTagTranspileMethod,
        FromImportTagTranspileMethod,
        ImportAsTagTranspileMethod,
        IncludeTagTranspileMethod,
        ReplaceNunjuckFiltersTranspileMethod,

        # After transpiling tags, execute other modifications.
        CallerMethodsTranspileMethod,
        MoveImportsTranspileMethod,
        SvgTagTranspileMethod
    ]

    # Executes all of transpile methods on a single template.
    @classmethod
    def transpile(cls, template, comparison_templates):

        Message.success('Transpiling template: %s' % template.name)

        cls.execute_transpile_methods(cls, template, comparison_templates)
        cls.write_template_data_comment(cls, template)

    def execute_transpile_methods(self, template, comparison_templates):

        for comparison_template in template.child_templates + comparison_templates:
            for transpile_method in self.transpile_methods:

                if self.exclude_method(transpile_method, template):
                    continue

                transpile_method.execute(template, comparison_template)

    def exclude_method(transpile_method, template) -> bool:

        for condition in transpile_method.exclude(template):
            if condition:
                return True

        return False

    @classmethod
    def get_transpiler_ignore_file_path(cls):
        return config.absolute_frontend_components_directory_path + '/transpiler_ignore.json'

    @classmethod
    def transpiler_ignore_file_exists(cls):
        return True if os.path.isfile(cls.get_transpiler_ignore_file_path()) else False

    @classmethod
    def create_transpiler_ignore_file(cls):
        try:
            shutil.copyfile(os.getcwd() + '/src/assets/transpiler_ignore.json', config.absolute_frontend_components_directory_path + '/transpiler_ignore.json')
        except:
            print('Could not copy file transpiler_ignore.json to %s', config.absolute_frontend_components_directory_path)

    # Writes the top comment in a transpiled template file.
    def write_template_data_comment(self, template):
        file_content = file_helper.read_file_content(template.get_absolute_template_file_path())

        with open(template.get_absolute_template_file_path(), "w") as f:
            f.write('{#\n\n')
            f.write('THIS TEMPLATE DATA:\n')
            f.write("Finished transpiling at: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
            f.write("uuid: %s \n" % str(template.uuid))

            if template.is_child():
                f.write('\nPARENT TEMPLATE DATA:' + '\n')
                f.write('Parent uuid: %s\n' % str(template.parent.uuid))
                f.write('Parent path: %s\n' % str(template.parent.relative_import_path))

            if template.is_parent() and template.has_childs():
                f.write('\nChild template paths (%s)\n' % str(len(template.child_templates)))
                for child_template in template.child_templates:
                    f.write('=> %s\n' % child_template.relative_import_path)

            f.write("\n#}\n\n")
            f.write(file_content)


