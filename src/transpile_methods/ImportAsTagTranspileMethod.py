from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import file_helper


class ImportAsTagTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:
    
        Replace frontend path with relative backend theme path {% import <path> as ... %}
    """

    @staticmethod
    def exclude(template):
        return []

    @staticmethod
    def execute(template, comparison_template):
        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        file_helper.write_file_content(
            absolute_file_path,
            r"(\{\%\s*import\s*\')([a-z-.\/]*" + comparison_template.name + ".html)(\'\s*as\s*[a-zA-Z]*\s*\%\})",
            r'\1' + comparison_template.get_relative_theme_import_path() + r'\3',
            file_content
        )