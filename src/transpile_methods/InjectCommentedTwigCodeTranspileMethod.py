import re

from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import file_helper


class InjectCommentedTwigCodeTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:
    
        Injects code from a comment
    """

    transpiler_message = '{# TRANSPILER INJECTED CODE #}'

    left_regex = r"({#\s*LINJECT:\s*(.*?)\s*#}\s*({[{|%]))"
    right_regex = r"(([%|}]})\s*{#\s*RINJECT:\s*(.*?)\s*#})"

    @staticmethod
    def exclude(template):
        return []

    @classmethod
    def execute(self, template, comparison_template):

        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        file_content = self.inject_from_left(self, file_content)
        file_content = self.inject_from_right(self, file_content)

        with open(absolute_file_path, "w") as f:
            f.write(file_content)

    def inject_from_left(self, file_content):

        for a in re.findall(self.left_regex, file_content):

            file_content = file_content.replace(a[0], 
            '%s %s %s' % (self.transpiler_message, a[2], a[1]))
        
        return file_content

    def inject_from_right(self, file_content):

        for a in re.findall(self.right_regex, file_content):

            file_content = file_content.replace(a[0], 
            '%s %s %s' % (a[2], a[1], self.transpiler_message))

        return file_content

    