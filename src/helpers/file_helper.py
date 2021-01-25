import config, codecs, os, re

def remove_file_name_extensions(file_name):
    return file_name[:(file_name.index('.'))]

def read_file_content(file_path):
    return codecs.open(file_path, "r", encoding="utf-8").read()

def write_file_content(file_path, regex_search_pattern, regex_replace_pattern, file_content):
    with open(file_path, "w") as f:
        f.write(re.sub(
            regex_search_pattern,
            regex_replace_pattern,
            file_content)
        )

def make_file(path, content):
    file = open(path, 'w')
    file.write(content)
    file.close()