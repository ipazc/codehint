==============
CodeHint 0.0.1
==============

`CodeHint` is a package for describing a function within the python console during runtime.
It works in the same way as an advanced IDE does when it displays the hint for function, but pretty-printing to
console rather than to a window.

.. image:: https://badge.fury.io/py/codehint.svg
    :target: https://badge.fury.io/py/codehint

An easy example of usage is as follows:

If we have the following function defined somewhere in our code:

.. code:: python

    >>> def hello(a, b:int, c) -> int:
    >>>     """
    >>>     Hello, this is an explanation
    >>>     of what this is going to do
    >>>     :param a: foo
    >>>     :param b: bar example
    >>>     :param c:
    >>>     :return: True if good, False otherwise.
    >>>     """
    >>>     x = a + b * 2*c
    >>>     return x

It can be described in any time later on with codehint:

.. code:: python

    >>> from codehint import hint
    >>> hint(hello)
    ------------------------
    def hello(a, b:int, c) -> int:
    
        Hello, this is an explanation of what this is going to do
    
    === Parameters: 3 ======
     [0] a (type Any) ->   foo
     [1] b (type int) ->   bar example
     [2] c (type Any) ->  
    ========================
     Result (type int) ->  True if good, False otherwise.

`CodeHint` currently can only be used to describe the signature of functions or methods.

Installation
============

It is only supported **Python 3.4.1** onwards:

.. code:: bash

    sudo pip3 install codehint


LICENSE
=======

It is released under the *MIT license*.
