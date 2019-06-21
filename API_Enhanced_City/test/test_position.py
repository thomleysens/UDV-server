#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.UserRoleController import UserRoleController


class TestPosition:

    def test_read_positions_1(self):
        Controller.recreate_tables()
        print("all positions")
        expected_response = 4
        assert expected_response == len(UserRoleController.get_roles())


if __name__ == '__main__':
    Controller.recreate_tables()
    TestPosition().test_read_positions_1()

