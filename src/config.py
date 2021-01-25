import os, sys, shutil, platform

from classes.Message import Message


DEBUGGING = True

# Argument 1. Is the script itself, thats why I check on above 2.
if not (len(sys.argv) > 2):
    Message.fail('You are missing arguments that are required to run this script')
    Message.warning('Argument 1: Absolute path to frontend folder')
    Message.warning('Argument 2: Absolute path to theme backend folder')
    exit()

absolute_frontend_path = sys.argv[1]
absolute_backend_path = sys.argv[2]

absolute_backend_components_directory_path = absolute_backend_path + '/templates/components'
absolute_frontend_components_directory_path = absolute_frontend_path + '/source/components'

# Set output directory, templates will be created in this directory.
absolute_output_directory_path = absolute_backend_path + '/templates/components'

# Statically type template paths relative from backend components folder.
# These paths are used to tell which directories need to be searched for .html files.
relative_frontend_template_directory_paths = [
    'template'
]

# These directories will be created to store templates in.
absolute_default_directory_paths = [
    absolute_output_directory_path + '/' + 'partials',
]

# Get basename from theme folder. For relative Drupal / Twig reference.
relative_theme_basename_reference = '@' + os.path.basename(absolute_backend_path)

relative_theme_components_directory_path = relative_theme_basename_reference + '/components'
relative_theme_assets_directory_path = relative_theme_basename_reference + '/../assets'


if DEBUGGING:

    # Set output directory, templates will be created in this directory.
    absolute_output_directory_path = '/Users/dave/PhpstormProjects/drupal-custom-commands/src/Scripts/syntax-converter/test_output'

    # These directories will be created to store templates in.
    absolute_default_directory_paths = [
        absolute_output_directory_path + '/' + 'partials',
    ]

    # Check if string is in path, preventing system wipes.
    if 'syntax-converter/test_output' in absolute_output_directory_path and os.path.isdir(absolute_output_directory_path):
        shutil.rmtree(absolute_output_directory_path)

    # Create new test output directory if not exists.
    if not os.path.isdir(absolute_output_directory_path):
        os.mkdir(absolute_output_directory_path)
