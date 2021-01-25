import re, uuid, config


class Template:

    def __init__(self, name, content):

        self.uuid = uuid.uuid4()
        self.parent = None

        self.name = name
        self.content = content
        self.child_templates = []

        self.relative_import_path = ''

    def contains_macro(self) -> bool:
        return bool(re.search(r"\{\%(\s)+macro(\s?)+(([a-z]|[A-Z])+\((\s?)+data(\s?)+\)(\s?)+)\%\}", self.content))

    def is_parent(self) -> bool:
        return not self.is_child()

    def is_child(self) -> bool:
        return bool(self.parent)

    def has_childs(self) -> bool:
        return bool(self.child_templates)
    
    def is_partial(self) -> bool:
        return not self.contains_macro()

    def set_relative_import_path(self, relative_path):
        self.relative_import_path = relative_path

    # Relative @theme/... import path. 
    # Used for converting frontend to backend import paths.
    def get_relative_theme_import_path(self):
        return config.relative_theme_components_directory_path + '/' + self.relative_import_path

    # Used for accessing the file contents.
    def get_absolute_template_file_path(self):
        return config.absolute_output_directory_path + '/' + self.relative_import_path






