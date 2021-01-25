# Syntax Converter

<b>*Be aware that the README is based on a Mac filesystem!*</b><br>
*This script is included inside the Drupal skeleton of Dept and can be called using a Drush command.*

## Requirements
This script should be executed using <b>Python v3 or higher</b>.

### Config
The config file is named <b>config.py</b> which is located in the <b>src</b> directory.<br>
In this file a bunch of paths are set which are used on runtime.

### Script Arguments
1. *Absolute path to project frontend folder*<br>
```/Users/<user>/<path_to_project>/project-name/src/frontend```
2. *Absolute path to project backend theme folder*<br>
```/Users/<user>/<path_to_project>/project-name/src/backend/web/themes/dtnl_theme```

*Executing the script:* ```<python> <path to main.py> <argument 1> <argument 2>```

### Execution
This script has to be called from <b>main.py</b> located in the <b>src</b> directory.

## Are you going to expand this transpiler or debug it?
*Then you should follow those steps:*
1. Go to <b>src/config.py</b> and set the variable <b>DEBUGGING</b> to True<br>
2. Go to <b>src/config.py</b> and set the variable <b>absolute_output_directory_path</b> to your path<br>
*The <b>absolute_output_directory_path</b> variable will be used to dump al the generated templates.* So pick wisely!<br>
*Create a directory named <b>test_output</b> inside the root of the <b>syntax-converter</b> (syntax-converter/test_output)*<br><br>
3. *Now you are able to run the transpiler by executing the following command:<br>*
```bash
python3 main.py /Users/<user>/<path_to_project>/project-name/src/frontend /Users/<user>/<path_to_project>/project-name/src/backend/web/themes/dtnl_theme
```
4. The files should appear in the <b>absolute_output_directory_path</b> directory.

## Features

### Transpiler Settings (optional)

Before you run the tool, I recommend to create a settings file. Because of its<br> existence you will probably going to make use of it which might come in handy if you think<br> something isn't right. Via the settings file you are able to ignore certain templates.<br>

#### Creating the Settings file
Create a <b>JSON</b> file named <b>transpiler-settings.json</b> inside the root of the <b>frontend components</b> directory.<br> After the file is created copy the <b>JSON</b> under here in the file.


```JSON
{
  "_README": [
    "This file needs to be placed inside the frontend components directory.",
    "Fill in the name of the component by their PARENT directory name.",
    "Please, only use one of the 2 transpile options: dont, only",

    "DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES",
    "Do not transpile components that are listed.",

    "ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES",
    "Only transpile components that are listed.",

    "CUSTOM_NUNJUCK_TO_TWIG_FILTERS",
    "If a filter is not supported by the transpiler, you can add it yourself as key value pairs."
  ],

  "SETTING_ENABLED": {

    "DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES": false,
    "ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES": false,

    "CUSTOM_NUNJUCK_TO_TWIG_FILTERS": false
  },

  "DONT_TRANSPILE_COMPONENT_DIRECTORY_NAMES": [
    "example-component"
  ],
  "ONLY_TRANSPILE_COMPONENT_DIRECTORY_NAMES": [
    "example-component"
  ],

  "CUSTOM_NUNJUCK_TO_TWIG_FILTERS": {
    "exampleNunjuckFilter": "exampleTwigFilter"
  }
}
```

*Be aware of the strict syntax of JSON!*

### Injecting code inside Twig by Commenting inside Frontend (optional)

*It is <b>important</b>, to place the comment at the side where you want to inject it, this does work with <b>{{</b> and <b>{%</b> tags.*

#### Left sided injection
If you want the transpiler to inject code inside Twig from the left side, you can do this by adding a comment inside the frontend template.
```
{% macro contactFooter(data) %}
    
    <div class="c-contact-footer" js-hook-contact-footer>
        <div class="o-grid">
            <div class="contact-footer__logo o-col-12 o-col-6--md">
                <img class="contact-footer__logo--image" src="{{ data.image.src }}" alt="{{ data.image.alt }}">
            </div>
            <div class="contact-footer__text o-col-12 o-col-6--md">
                {# LINJECT: yourInjectedCode #} {% yourInjectedCode data.content.text | safe %}
                {{ data.content.text | raw }}
            </div>
        </div>
    </div>
{% endmacro %}
```

#### Right sided injection
If you want the transpiler to inject code inside Twig from the right side, you can do this by adding a comment inside the frontend template.

```
{% macro contactFooter(data) %}
    
    <div class="c-contact-footer" js-hook-contact-footer>
        <div class="o-grid">
            <div class="contact-footer__logo o-col-12 o-col-6--md">
                <img class="contact-footer__logo--image" src="{{ data.image.src }}" alt="{{ data.image.alt }}">
            </div>
            <div class="contact-footer__text o-col-12 o-col-6--md">
                {% data.content.text | safe yourInjectedCode %} {# RINJECT: yourInjectedCode #} 
                {{ data.content.text | raw }}
            </div>
        </div>
    </div>
{% endmacro %}
```

## Transpiler main flow of Execution

1. *main.py* is called using command with arguments
2. Import config file, check if DEBUGGING mode is on, if not continue else show debug messages
2. Create new instance of class TemplateManager and create default directories (*partials etc..*)
3. Check if <b>transpiler-settings.json</b> settings file exists, then implement settings on the fly.<br> 
    *Do a search all in the source code for 'SETTING IMPLEMENTATION' to find the implementations*
4. Create the parent template objects and for each parent template object create child template objects<br>
    *The template files will be created by the TemplateFactory class, which will take care of the file naming convention* 
5. For each created template, transpile using TemplateTranspiler.transpile(...)
    - Mutate the template file by executing all transpile methods on it<br> 
        *A single transpile method should do 1 type of file mutation. The transpile methods are prioritized!*
    - If transpile method has exclude conditions, skip if they return true else continue
    - Write log comment at the top of the template file, for enduser debug purposes