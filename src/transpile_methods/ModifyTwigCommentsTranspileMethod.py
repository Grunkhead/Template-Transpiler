from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import file_helper
from helpers import transpile_helper


class ModifyTwigCommentsTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:
    
        Modifies the {% tags within the comments {# ... #}
        This way the transpiler doesn't get confused.
    """

    @staticmethod
    def exclude(template):
        return []

    @staticmethod
    def execute(template, comparison_template):
        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        comments = transpile_helper.get_twig_comments_from_file_content(file_content)

        for comment in comments:
            modifiedComment = comment.replace('{%', '{# (IGNORED BY TRANSPILER)')
            file_content = file_content.replace(comment, modifiedComment)

        with open(absolute_file_path, "w") as f:
            f.write(file_content)