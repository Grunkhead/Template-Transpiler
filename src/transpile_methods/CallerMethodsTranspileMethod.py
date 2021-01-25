from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import file_helper
from helpers import transpile_helper


class CallerMethodsTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:
    
        Replaces {{ caller() }} with {{ html_block_<num> }} within a macro for each caller.
    """

    @staticmethod
    def exclude(template):
        return []

    @staticmethod
    def execute(template, comparison_template):
        
        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        for macro_partial in transpile_helper.get_macros_as_strings_from_file_content(file_content):
            file_content = file_content.replace(macro_partial, transpile_helper.replace_caller_methods(macro_partial))

        with open(absolute_file_path, "w") as f:
            f.write(file_content)
