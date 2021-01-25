import config, time

from classes.TemplateManager import TemplateManager
from classes.TemplateTranspiler import TemplateTranspiler


def main():

    templateManager = TemplateManager()
    templates = templateManager.get_templates()

    runtime_start = time.time()

    for template in templates:
        TemplateTranspiler.transpile(template, templates)

    runtime_stop = time.time()

    # Calculate runtime.
    runtime_duration = runtime_stop - runtime_start

    print("Finished transpiling in %s seconds" % str(runtime_duration))
    
    return '0'

main()

    





    