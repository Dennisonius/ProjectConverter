# -*- coding: utf-8 -*-

""" Entry point for project conversion
    @file
"""

import os
import argparse
import cmake
import ewpproject
import uvprojxproject


def callRightConversion(my_arg):
    # Check input file parameter
    if os.path.isfile(my_arg.project_file) is False:
        print('Not a valid file path')
        return

    # Check input project type
    ext = "." + my_arg.format
    if my_arg.project_file.endswith(ext) is False:
        print('Wrong format or project file specified')
        return

    if my_arg.format == 'ewp':
        print('Converting iar project file:' + my_arg.project_file)
        print(f'Cmake file is for {my_arg.compiler}')
        project = ewpproject.EWPProject(my_arg.project_file)

        project.parseProject()
        project.displaySummary()

        cmakefile = cmake.CMake(project.getProject(), my_arg.project_file)
        cmakefile.populateCMake(my_arg.compiler)
    elif my_arg.format == 'uvprojx':
        print('Converting keil project file:' + my_arg.project_file)

        project = uvprojxproject.UVPROJXProject(
            my_arg.project_file, my_arg.project_file)
        project.parseProject()
        project.displaySummary()
        cmakefile = cmake.CMake(project.getProject(), my_arg.project_file)
        cmakefile.populateCMake(my_arg.compiler)
    return


if __name__ == '__main__':

    # Parse params and call the right conversion
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=("ewp", "uvprojx"))
    parser.add_argument("project_file", type=str, help="Project file path")
    parser.add_argument("compiler", choices=("iar", "clang"))

    args = parser.parse_args()
    callRightConversion(args)
