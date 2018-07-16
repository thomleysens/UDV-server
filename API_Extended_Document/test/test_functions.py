#!/usr/bin/env python3
# coding: utf8

from colorama import Fore, Style


def display_error(error=True):
    if error:
        print(f"{Fore.RED}[ error ]", end=" ")
    else:
        print(f"{Fore.GREEN}[success]", end=" ")
    print(f"{Style.RESET_ALL}", end="")


def format_display(old_function):
    def new_function(TestClass, description, expecting_error,
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

            TestClass.nb_tests += 1
            if expecting_error == happened_error:
                TestClass.nb_tests_succeed += 1

    return new_function


@format_display
def test_operation(function_to_test):
    return function_to_test()
