#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author Maxime Hutinet

class ColorText:
    '''
    Class to print pretty colored message.
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def Header(text):
        return ColorText.HEADER + text + ColorText.ENDC

    @staticmethod
    def OkBlue(text):
        return ColorText.OKBLUE + text + ColorText.ENDC

    @staticmethod
    def OkGreen(text):
        return ColorText.OKGREEN + text + ColorText.ENDC

    @staticmethod
    def Warning(text):
        return ColorText.WARNING + text + ColorText.ENDC

    @staticmethod
    def Fail(text):
        return ColorText.FAIL + text + ColorText.ENDC
