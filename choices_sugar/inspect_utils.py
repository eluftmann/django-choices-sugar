# coding=utf-8

import functools
import inspect
import itertools
from cStringIO import StringIO


def unindent_block(code):
    """
    Unindent Python source code block.

    Superfluous indentation is inferred from the leading whitespaces
    in the first line.

    :param code: source code to unindent
    :type code: str

    :rtype: str

    >>> unindent_block("    class C(object):\\n        A = 10\\n")
    'class C(object):\\n    A = 10\\n'
    >>> unindent_block("class C(object):\\n  A = 10\\n  B = 20\\n")
    'class C(object):\\n  A = 10\\n  B = 20\\n'
    >>> unindent_block("    ")
    ''
    """
    code_stream = StringIO(code)

    first_line = code_stream.readline()
    base_indent = len(first_line) - len(first_line.lstrip())

    # Reduce function is fed with a tuple as a second argument:
    # next line of code with number of characters to strip (indentation)
    return functools.reduce(
        lambda code_acc, (next_line, start): code_acc + next_line[start:],
        itertools.product(code_stream, [base_indent]),
        first_line[base_indent:]
    )


def get_class_source(object, object_attrs=None):
    """Return the text of the source code for a class.

    The source code is returned as a single string. An IOError is raised
    if the source code cannot be retrieved.
    """
    return inspect.getsource(object)
