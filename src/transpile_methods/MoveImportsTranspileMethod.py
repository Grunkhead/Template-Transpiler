from interfaces.TranspileMethodInterface import TranspileMethodInterface

from helpers import transpile_helper
from helpers import file_helper


class MoveImportsTranspileMethod(TranspileMethodInterface):

    """ METHOD DESCRIPTION:

        Moves the import tags within the macro where they are being used.
    """

    @staticmethod
    def exclude(template):
        return [
            template.is_partial()
        ]

    @staticmethod
    def execute(template, comparison_template):
        absolute_file_path = template.get_absolute_template_file_path()
        file_content = file_helper.read_file_content(absolute_file_path)

        macros = transpile_helper.get_macros_as_match_objects_from_file_content(file_content)
        imports = (
            transpile_helper.get_from_import_tags_from_file_content(file_content) 
            + transpile_helper.get_from_import_as_tags_from_file_content(file_content)
            + transpile_helper.get_import_as_tags_from_file_content(file_content))

        # Keep track of changed indexes, so macro and import indexes will be accurate.
        changed_indexes = 0

        # Open file for writing, on write. Replace all file contents with a new string.
        with open(absolute_file_path, "w") as f:

            # Loop over macro matchObjects.
            for macro in macros:

                # Get the full macro match string.
                full_macro = macro.group(0)

                # Get the index of the macro starting tag, and add the changed indexes.
                macro_start_tag_end_index = macro.span(1)[1] + changed_indexes + 1

                # Slice the file content in two parts, so we can add the new lines in between.
                first_file_content_slice = file_content[:macro_start_tag_end_index]
                last_file_content_slice = file_content[macro_start_tag_end_index:]

                for import_line in imports:

                    # Get the full import match string.
                    full_import_line = import_line[0]

                    # Get the variableName from match string.
                    import_line_variable = import_line[1]

                    # Check if the variable of the import is used inside the macro string.
                    if '{{ ' + import_line_variable + '(' in full_macro or "{% call " + import_line_variable in full_macro:

                        # Add the full import string to the string with a new line.
                        first_file_content_slice += full_import_line + '\n'

                        # Add the changed indexes.
                        changed_indexes += len(full_import_line + '\n')

                # Overwrite the file_content variable, so the next iteration can add on top of the string.
                file_content = first_file_content_slice + last_file_content_slice

            # Remove old twig import lines, only remove the first occurrence.
            removed_import_lines = []

            for import_line in imports:
                
                if import_line[0] in removed_import_lines:
                    continue
                
                file_content = file_content.replace(import_line[0] + '\n', '', 1)
                removed_import_lines.append(import_line[0])

            f.write(file_content)