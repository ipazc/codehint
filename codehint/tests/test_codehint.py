#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#MIT License
#
#Copyright (c) 2017 Iván de Paz Centeno
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import unittest
from codehint import hint

__author__ = 'Iván de Paz Centeno'


class TestCodehint(unittest.TestCase):
    """
    Unitary tests for the codehint class.
    """

    def test_description_on_simple_funcs(self):
        """
        Description on simple functions without params works as expected
        """
        def simple_func():
            return 2

        truth = """------------------------
def simple_func():

=== Parameters: 0 ======
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(simple_func, do_print=False), truth)

    def test_description_on_simple_funcs_with_params(self):
        """
        Description on simple functions with params works as expected
        """
        def simple_func1(a):
            return 2

        def simple_func2(a, b):
            return 2

        truth_func1 = """------------------------
def simple_func1(a):

=== Parameters: 1 ======
 [0] a (type Any) ->  Not provided
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(simple_func1, do_print=False), truth_func1)

        truth_func2 = """------------------------
def simple_func2(a, b):

=== Parameters: 2 ======
 [0] a (type Any) ->  Not provided
 [1] b (type Any) ->  Not provided
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(simple_func2, do_print=False), truth_func2)

    def test_description_on_funcs_with_doc_params(self):
        """
        Description on functions with documented params works as expected
        """
        def func1(a):
            """
            :param a: Parameter a, to test the retrieval of the docs.
            """

            return 2

        def func2(a, b):
            """
            :param a: Parameter a, to test the retrieval of the docs.
            :param b: Parameter b, to test the retrieval of the docs (again).
            """
            return 2


        truth_func1 = """------------------------
def func1(a):

=== Parameters: 1 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func1, do_print=False), truth_func1)

        truth_func2 = """------------------------
def func2(a, b):

=== Parameters: 2 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
 [1] b (type Any) ->  Parameter b, to test the retrieval of the docs (again).
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func2, do_print=False), truth_func2)

    def test_description_on_funcs_with_doc_params_and_documented_return_and_main(self):
        """
        Description on functions with documented params, main description and return description works as expected
        """
        def func1(a):
            """
            :param a: Parameter a, to test the retrieval of the docs.
            :return: True in case FOO. False otherwise.
            """

            return 2

        def func2(a):
            """
            This is the main description of the func2.
            :param a: Parameter a, to test the retrieval of the docs.
            """
            return 2

        def func3(a):
            """
            This is the main description of the func3.
            :param a: Parameter a, to test the retrieval of the docs.
            :return: True if it is working, false otherwise.
            """
            return 2

        truth_func1 = """------------------------
def func1(a):

=== Parameters: 1 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
========================
 Result (type Any) ->  True in case FOO. False otherwise.
"""
        self.assertEqual(hint(func1, do_print=False), truth_func1)

        truth_func2 = """------------------------
def func2(a):

    This is the main description of the func2.

=== Parameters: 1 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func2, do_print=False), truth_func2)

        truth_func3 = """------------------------
def func3(a):

    This is the main description of the func3.

=== Parameters: 1 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
========================
 Result (type Any) ->  True if it is working, false otherwise.
"""
        self.assertEqual(hint(func3, do_print=False), truth_func3)

    def test_description_on_funcs_with_doc_and_types_params_and_documented(self):
        """
        Description on functions with documented params (with also Types) works as expected.
        """
        def func1(a:int):
            """
            :param a: Parameter a, to test the retrieval of the docs.
            """

            return 2

        def func2(a, b:str):
            """
            This is the main description of the func2.
            :param a: Parameter a, to test the retrieval of the docs.
            :param b: Parameter b, to test the retrieval of the docs.
            """
            return 2

        def func3(a:list, b:str):
            """
            This is the main description of the func3.
            :param b: Parameter b, to test the retrieval of the docs.
            """
            return 2

        def func4(a:list, b:str) -> dict:
            """
            This is the main description of the func4.
            :param b: Parameter b, to test the retrieval of the docs.
            :return: dict result
            """
            return 2

        truth_func1 = """------------------------
def func1(a:int):

=== Parameters: 1 ======
 [0] a (type int) ->  Parameter a, to test the retrieval of the docs.
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func1, do_print=False), truth_func1)

        truth_func2 = """------------------------
def func2(a, b:str):

    This is the main description of the func2.

=== Parameters: 2 ======
 [0] a (type Any) ->  Parameter a, to test the retrieval of the docs.
 [1] b (type str) ->  Parameter b, to test the retrieval of the docs.
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func2, do_print=False), truth_func2)

        truth_func3 = """------------------------
def func3(a:list, b:str):

    This is the main description of the func3.

=== Parameters: 2 ======
 [0] a (type list) ->  Not provided
 [1] b (type str) ->  Parameter b, to test the retrieval of the docs.
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func3, do_print=False), truth_func3)

        truth_func4 = """------------------------
def func4(a:list, b:str) -> dict:

    This is the main description of the func4.

=== Parameters: 2 ======
 [0] a (type list) ->  Not provided
 [1] b (type str) ->  Parameter b, to test the retrieval of the docs.
========================
 Result (type dict) ->  dict result
"""
        self.assertEqual(hint(func4, do_print=False), truth_func4)


    def test_multilines_descriptions(self):
        """
        Multi-line descriptions on functions works as expected.
        """
        def func1():
            """
            this is a multiline
            document for the
            func1. AKA Main description.
            """

            return 2

        def func2(a):
            """
            this is a multiline
            document for the
            func2. AKA Main description.
            :param a: this is a multiline description
            for parameter a. Right?
            """

        def func3(a, b):
            """
            this is a multiline
            document for the
            func3. AKA Main description.
            :param a: this is a multiline description
            for parameter a. Right?
            :param b: this is a multiline description
            for parameter b. Right?
            """
            return 2

        def func4(a, b):
            """
            this is a multiline
            document for the
            func4. AKA Main description.
            :param a: this is a multiline description
            for parameter a. Right?
            :param b: this is a multiline description
            for parameter b. Right?
            :return: this is true in any case,
                false otherwise, since this is in a second line.
            """
            return 2

        truth_func1 = """------------------------
def func1():

    this is a multiline document for the func1. AKA Main description.

=== Parameters: 0 ======
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func1, do_print=False), truth_func1)

        truth_func2 = """------------------------
def func2(a):

    this is a multiline document for the func2. AKA Main description.

=== Parameters: 1 ======
 [0] a (type Any) ->  this is a multiline description for parameter a. Right?
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func2, do_print=False), truth_func2)

        truth_func3 = """------------------------
def func3(a, b):

    this is a multiline document for the func3. AKA Main description.

=== Parameters: 2 ======
 [0] a (type Any) ->  this is a multiline description for parameter a. Right?
 [1] b (type Any) ->  this is a multiline description for parameter b. Right?
========================
 Result (type Any) ->
"""
        self.assertEqual(hint(func3, do_print=False), truth_func3)

        truth_func4 = """------------------------
def func4(a, b):

    this is a multiline document for the func4. AKA Main description.

=== Parameters: 2 ======
 [0] a (type Any) ->  this is a multiline description for parameter a. Right?
 [1] b (type Any) ->  this is a multiline description for parameter b. Right?
========================
 Result (type Any) ->  this is true in any case, false otherwise, since this is in a second line.
"""
        self.assertEqual(hint(func4, do_print=False), truth_func4)

if __name__ == '__main__':
    unittest.main()