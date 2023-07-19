# -*- coding: utf-8 -*-

""" Module for converting EWP project format file
    @file
"""

import os
from lxml import objectify


class EWPProject(object):
    """ Class for converting EWP project format file
    """

    def __init__(self, xmlFile):
        self.project = {}
        self.path, self.xmlFile = os.path.split(xmlFile)
        xmltree = objectify.parse(xmlFile)
        self.root = xmltree.getroot()

    def parseProject(self):
        """ Parses EWP project file for project settings
        """
        self.project['workspace name'] = self.root.configuration.name
        self.project['name'] = os.path.splitext(self.xmlFile)[0]

        self.project['srcs_base'] = os.path.dirname(self.path)
        self.project['srcs_base'] = self.myNormCase(self.project['srcs_base'])
        self.project['srcs'] = []
        self.expandGroups(self.root, self.project['srcs'])

        self.project['chip'] = ''
        self.project['defs'] = []
        self.project['incs'] = []
        self.project['dlib_config'] = ''
        self.project['diag_suppress'] = 'Pe826,Pe068,Pa091,Pe001'
        self.project['diag_error'] = 'Pe2349,Pe223'
        self.project['linker_icf'] = ''
        self.project['linker_symbols'] = []
        for settings in self.root.configuration.iterchildren(tag='settings'):
            for option in settings.data.iterchildren(tag='option'):
                if option.name.text == 'OGChipSelectEditMenu':
                    self.project['chip'] = str(option.state)
                elif option.name.text == 'CCDefines':
                    for a_define in option.iterchildren(tag='state'):
                        self.project['defs'].append(a_define.text)
                elif option.name.text == 'CCIncludePath2':
                    for a_include in option.iterchildren(tag='state'):
                        s = a_include.text
                        s = self.myNormCase(s)
                        self.project['incs'].append(s)
                elif option.name.text == 'RTConfigPath2':
                    s = str(option.state)
                    s = self.myNormCase(s)
                    s = s.replace('$TOOLKIT_DIR$', '')
                    self.project['dlib_config'] = s
                elif option.name.text == 'IlinkIcfFile':
                    s = str(option.state)
                    s = self.myNormCase(s)
                    self.project['linker_icf'] = s
                elif option.name.text == 'IlinkKeepSymbols':
                    for a_symbol in option.iterchildren(tag='state'):
                        self.project['linker_symbols'].append(a_symbol.text)

    def displaySummary(self):
        """ Display summary of parsed project settings
        """
        print('Project Workspace Name:' + self.project['workspace name'])
        print('Project Name:' + self.project['name'])
        print('Project chip:' + self.project['chip'])
        print('Project includes: ' + ' '.join(self.project['incs']))
        print('Project defines: ' + ' '.join(self.project['defs']))
        print('Project srcs: ' + ' '.join(self.project['srcs']))
        print('Project linker icf file:' + self.project['linker_icf'])
        print('Project linker symbols: ' + ' '.join(self.project['linker_symbols']))

    def expandGroups(self, xml, sources):
        """ SearchGroups - project folders
        @param xml XML file element tagged 'group'
        @param sources List containing source files
        """
        for el in xml.iterchildren(tag='file'):
            if hasattr(el, 'excluded'):
                continue
            s = str(el.name)
            s = self.myNormCase(s)
            sources.append(s)

        for el in xml.iterchildren(tag='group'):
            self.expandGroups(el, sources)

    def myNormCase(self, s):
        s = s.replace('\\', '/')
        s = s.replace('$PROJ_DIR$' + '/' + '..', '')
        os.path.normcase(s)
        return s

    def getProject(self):
        """ Return parsed project settings stored as dictionary
        @return Dictionary containing project settings
        """
        return self.project
