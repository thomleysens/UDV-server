#!/usr/bin/env python3
# coding: utf8

import sys

from controller.Controller import Controller
from controller.DocController import DocController
from controller.TourController import TourController

from test.test_functions import *


class GuidedTourTest:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_tours():
        print("\033[01m## Creation of tours ##\033[0m")
        test_operation(GuidedTourTest, "all needed attributes",
                       False,
                       lambda: TourController.create_tour(
                           "First tour",
                           "This is the first guided tour"))

        test_operation(GuidedTourTest, "all needed attributes",
                       False,
                       lambda: TourController.create_tour(
                           "Second tour",
                           "This is the second guided tour"))

        test_operation(GuidedTourTest,
                       "needed + nonexistent attributes",
                       False,
                       lambda: TourController.create_tour(
                           "Third tour",
                           "This is the third guided tour"))

        test_operation(GuidedTourTest, "needed argument missing",
                       True,
                       lambda: TourController.create_tour())

    @staticmethod
    def create_documents():
        print("\n\033[01m## Creation of documents ##\033[0m")
        test_operation(GuidedTourTest, "all needed attributes",
                       False,
                       lambda: DocController.create_document(
                           {"title": "title",
                            "subject": "Subject1",
                            "type": "type",
                            "description": "a description",
                            "link": "1.gif"}))

        test_operation(GuidedTourTest, "all needed attributes",
                       False,
                       lambda: DocController.create_document(
                           {"title": "title2",
                            "subject": "Subject2",
                            "type": "type",
                            "description": "a description",
                            "link": "1.gif"}))

    @staticmethod
    def read_tours():
        print("\n\033[01m## Reading ##\033[0m")

        test_operation(GuidedTourTest, "all tours", False,
                       lambda: TourController.get_tours())

        # @TODO: create method to filter docs
        test_operation(GuidedTourTest, "specific tour", False,
                       lambda: TourController.get_tours())

        test_operation(GuidedTourTest, "tour with existing id", False,
                       lambda: TourController.get_tour_by_id(2))

        test_operation(GuidedTourTest, "tour with non existing id",
                       True,
                       lambda: TourController.get_tour_by_id(-1))

    @staticmethod
    def update_tours():
        print("\n\033[01m## Updating ##\033[0m")
        test_operation(GuidedTourTest, "adding existing document",
                       False,
                       lambda: TourController.add_document(1, 1))

        test_operation(GuidedTourTest, "adding twice existing document",
                       False,
                       lambda: TourController.add_document(1, 1))

        test_operation(GuidedTourTest, "adding twice existing document",
                       True,
                       lambda: TourController.add_document(1))

        test_operation(GuidedTourTest, "adding existing document",
                       False,
                       lambda: TourController.add_document(1, 2))

        test_operation(GuidedTourTest, "adding existing document",
                       False,
                       lambda: TourController.add_document(2, 1))

        test_operation(GuidedTourTest, "adding non existing document",
                       True,
                       lambda: TourController.add_document(1, 3))

        test_operation(GuidedTourTest, "adding non existing document",
                       True,
                       lambda: TourController.add_document(-1, 3))

    @staticmethod
    def delete_tours():
        print("\n\033[01m## Deletion ##\033[0m")
        test_operation(GuidedTourTest, "existing document", False,
                       lambda: TourController.delete_tour(3))
        test_operation(GuidedTourTest, "existing document", True,
                       lambda: TourController.delete_tour(3))


if __name__ == "__main__":
    Controller.recreate_tables()
    GuidedTourTest.create_tours()
    GuidedTourTest.create_documents()
    GuidedTourTest.read_tours()
    GuidedTourTest.update_tours()
    GuidedTourTest.read_tours()
    GuidedTourTest.delete_tours()
    GuidedTourTest.read_tours()

    print("\n\n\033[04mSuccess\033[01m: ",
          GuidedTourTest.nb_tests_succeed, "/",
          GuidedTourTest.nb_tests, sep="")
