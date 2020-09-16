import os
import glob
from shutil import copyfile
# from jinja2 import Template

import dieterpy
from dieterpy.config import settings


def find_files_oswalk(root, templates_search_dir, search=None):
    for file in glob.glob(os.path.join(root, templates_search_dir, '**/*.*'), recursive=True):
        exists = False
        section = ''
        basefile = os.path.basename(file)
        inbetween = file[len(root)+1:-len(basefile)-1].split(os.sep)
        newsection = inbetween[:]
        if search is not None:
            if search in inbetween:
                exists = True
                newsection.remove(search)
            if templates_search_dir in inbetween:
                newsection.remove(templates_search_dir)
        if newsection:
            section = os.path.join(*newsection)
        yield (file, root, section, basefile, exists)

def istemplate(file_abspath):
    file_name = os.path.basename(file_abspath)
    is_tpl = file_name.split('-')[-1]
    if is_tpl == 'tpl':
        flag = True
        destination_filename = file_name[:-4]
    else:
        flag = False
        destination_filename = file_name
    return (flag, destination_filename)

# def template2files(template_abspath, destination_file_abspath, options):
#     '''Render module template to files'''
#     with open(template_abspath) as file_:
#         template = Template(file_.read())
#     output_from_parsed_template = template.render(**options)
#     with open(destination_file_abspath, "w") as fh:
#         fh.write(output_from_parsed_template)

def create_project(project_name, template):
    template_check = ['base', 'example1', 'example2', 'example3', 'example4']
    if template in template_check:
        pass
    else:
        raise Exception(f'--template argument "{template}" not in {template_check}')
    settings.PROJECT_NAME = project_name
    cwd = os.getcwd()
    module_abspath = dieterpy.__path__[0]

    for file, root, section, basefile, exists in find_files_oswalk(module_abspath, settings.TEMPLATES_DIR_NAME, template):
        template_abspath = file
        istemplate_flag, destination_filename = istemplate(template_abspath)

        if destination_filename == 'manage.py':
            destination_file_abspath = os.path.join(cwd, settings.PROJECT_NAME, section, destination_filename)
        elif destination_filename in ['data_input.xlsx', 'time_series.xlsx'] or exists:
            destination_file_abspath = os.path.join(cwd, settings.PROJECT_NAME, settings.BASE_DIR_NAME, section, destination_filename)
        else:
            continue
        os.makedirs(os.path.split(destination_file_abspath)[0], exist_ok=True)
        # if not istemplate_flag:
        #     copyfile(template_abspath, destination_file_abspath)
        # else:
        #     template2files(template_abspath, destination_file_abspath, settings.__dict__['variables'].__dict__)
        copyfile(template_abspath, destination_file_abspath)
    return None
