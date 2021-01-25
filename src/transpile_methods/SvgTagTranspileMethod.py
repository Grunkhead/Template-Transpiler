import config

from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import file_helper


class SvgTagTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:

        Replaces frontend svg tag with backend source tag.
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
            r"(\{\%\s*svg\s*[\'\"])([a-z-.\/]*)([\'\"]\s*\%\})",
            r'{{ source("' + config.relative_theme_assets_directory_path + r'/svg/\2.svg") }}',
            file_content
        )