#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.PositionController import PositionController

from test.test_functions import *


class PositionTest:
    nb_tests = 0
    nb_tests_succeed = 0

    @staticmethod
    def read_positions():
        print('\n\033[01m## Reading ##\033[0m')

        make_test(lambda: PositionController.get_positions())(
            PositionTest, 'all positions', False)


if __name__ == '__main__':
    Controller.recreate_tables()
    PositionTest.read_positions()
    print('\n\n\033[04mSuccess\033[01m: ',
          PositionTest.nb_tests_succeed, '/',
          PositionTest.nb_tests, sep='')
