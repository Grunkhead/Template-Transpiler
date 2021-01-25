import re

from interfaces.TranspileMethodInterface import TranspileMethodInterface
from classes.TranspileSettings import TranspileSettings

from helpers import file_helper
from helpers import transpile_helper


class ReplaceNunjuckFiltersTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:
    
        Replaces Nunjuck filter functions with Twig filter functions.
    """

    regex = r"(({{\s*[a-zA-Z.]*\s*\|)\s*(.*?)\s*(}}))"

    settings = [
        'CUSTOM_NUNJUCK_TO_TWIG_FILTERS'
    ]

    filters = {
        'safe': 'raw'
    }

    @staticmethod
    def exclude(template):
        return []

    @classmethod
    def execute(self, template, comparison_template):
        
        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        # Setting implementation: CUSTOM_NUNJUCK_TO_TWIG_FILTERS
        if TranspileSettings.setting_enabled(self.settings[0]) and TranspileSettings.load_settings_file()['SETTING_ENABLED'][self.settings[0]]:
            self.filters = self.merge_developer_custom_filters(self)

        for a in re.findall(self.regex, file_content):

            converted_filters = []

            # Split regex group 2 with the filters and strip the whitespace for each filter.
            for f in map(lambda f: f.strip(), a[2].split('|')):

                converted_filters.append(
                    self.filters.get(f) if f in self.filters else f
                )

            # Replace old filter string with the converted.
            file_content = file_content.replace(a[0], f"{a[1]} {' | '.join(converted_filters)} {a[3]}")

        with open(absolute_file_path, "w") as f:
            f.write(file_content)

    def merge_developer_custom_filters(self):
        return {**self.filters, **TranspileSettings.load_settings_file()[self.settings[0]]}

