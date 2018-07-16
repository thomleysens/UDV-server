#!/usr/bin/env python3
# coding: utf8

from colorama import Fore
from colorama import Style

from controller.Controller import Controller


class Test:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_documents():
        print("\033[01m## Creation ##\033[0m")
        test_operation("all needed attributes",
                       False,
                       lambda: Controller.create_document(
                           {"title": "title",
                            "subject": "Subject1",
                            "type": "type",
                            "description": "a description",
                            "link": "1.gif"}))

        test_operation("all needed attributes",
                       False,
                       lambda: Controller.create_document(
                           {"title": "title",
                            "subject": "Subject2",
                            "type": "type",
                            "description": "a description",
                            "link": "2.gif",
                            "refDate": "2019-02-05"}))

        test_operation("needed + nonexistent attributes",
                       False,
                       lambda: Controller.create_document(
                           {"title": "another title",
                            "subject": "Subject3",
                            "type": "type",
                            "non_attr": "non_value",
                            "refDate": "2018-12-03",
                            "description": "an other description",
                            "link": "3.png"}))

        test_operation("needed argument missing",
                       True,
                       lambda: Controller.create_document(
                           {"title": "another title"}))

    @staticmethod
    def read_documents():
        print("\n\033[01m## Reading ##\033[0m")

        test_operation("all documents", False,
                       lambda: Controller.get_documents({}))

        test_operation("specific documents", False,
                       lambda: Controller.get_documents(
                           {"keyword": "description",
                            'refDateStart': '2018-12-03'}))

        test_operation("document with existing id", False,
                       lambda: Controller.get_document_by_id(1))

        test_operation("document with non existing id", True,
                       lambda: Controller.get_document_by_id(-1))

    @staticmethod
    def update_documents():
        print("\n\033[01m## Updating ##\033[0m")
        test_operation("existing document", False,
                       lambda: Controller.update_document(1, {
                           'positionX': 12,
                           'description': "description of a document"
                       }))

        test_operation("existing document", False,
                       lambda: Controller.update_document(1, {
                           'positionX': 12,
                           'description': "another description"
                       }))

        test_operation("existing document", True,
                       lambda: Controller.update_document(-1, {
                           'positionX': 12,
                           'description': "description of a document"
                       }))

    @staticmethod
    def delete_documents():
        print("\n\033[01m## Deletion ##\033[0m")
        test_operation("existing document", False,
                       lambda: Controller.delete_documents(2))
        test_operation("existing document", True,
                       lambda: Controller.delete_documents(2))


def display_error(error=True):
    if error:
        print(f"{Fore.RED}[ error ]", end=" ")
    else:
        print(f"{Fore.GREEN}[success]", end=" ")
    print(f"{Style.RESET_ALL}", end="")


def format_display(old_function):
    def new_function(description, expecting_error,
                     function_to_test):
        happened_error = False
        function_result = ""
        exception = ""
        try:
            function_result = old_function(function_to_test)
        except Exception as e:
            exception = e
            happened_error = True
        finally:
            display_error(expecting_error != happened_error)
            display_error(expecting_error)
            display_error(happened_error)
            print("{:<32}".format(description + ":"), end="")
            print(f"{Fore.RED}", str(exception).replace("\n", ""),
                  end="")
            print(f"{Fore.BLUE}", function_result, sep="")
            print(f"{Style.RESET_ALL}", sep="", end="")

            Test.nb_tests += 1
            if expecting_error == happened_error:
                Test.nb_tests_succeed += 1

    return new_function


@format_display
def test_operation(function_to_test):
    return function_to_test()


if __name__ == "__main__":
    Controller.recreate_tables()
    Test.create_documents()
    Test.read_documents()
    Test.update_documents()
    Test.read_documents()
    Test.delete_documents()
    Test.read_documents()
    print("\n\n\033[04mSuccess\033[01m: ", Test.nb_tests_succeed, "/",
          Test.nb_tests, sep="")
