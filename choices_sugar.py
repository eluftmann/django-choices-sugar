# coding=utf-8

import ast
import functools
import inspect
import itertools
from cStringIO import StringIO

__all__ = ['Choices']


VERSION = (0, 1)

# PEP 440-compliant version number from `VERSION`
__version__ = '.'.join(map(str, VERSION))


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
    # Could be also done using standard list comprehensions / string join.
    return functools.reduce(
        lambda code_acc, (next_line, start): code_acc + next_line[start:],
        itertools.product(code_stream, [base_indent]),
        first_line[base_indent:]
    )


class AssignNodeVisitor(ast.NodeVisitor):
    """
    AssignNode visitor collecting attributes names during AST traversal.
    """

    def __init__(self, illegal_attributes=None):
        """

        :type illegal_attributes: list[str]
        """
        self._illegal_attributes = illegal_attributes or []
        self.visited_attributes = []

    def visit_Assign(self, node):
        """
        Visit Assign node and collect attribute name.

        Additionally 2 validation rules will be applied:
            - check for specified illegal attributes names,
            - check for duplicated attributes names.

        :raises TypeError:
        :raises ValueError:
        """
        assert len(node.targets) == 1

        for target in node.targets:
            if target.id in self._illegal_attributes:
                raise TypeError("illegal attribute name: %r" % target.id)

            if target.id in self.visited_attributes:
                raise ValueError("duplicated attribute name: %r" % target.id)

            self.visited_attributes.append(target.id)


class AttributedTuple(tuple):
    """
    Tuple-compatible type which enables limited fields (attributes) access.

    This class acts as a class template and should be only instantiated
    by ``ChoisesMeta``.
    """

    __slots__ = ()

    def __getattr__(self, name):
        return self[self._fields.index(name)][0]

    def __setattr__(self, key, value):
        raise AttributeError

    def __getnewargs__(self):
        return tuple(self)

    def __getstate__(self):
        pass


class ChoicesMeta(type):
    """
    Metaclass to replaces class object with an ``AttributedTuple`` instance.

    Constructed tuple will have all attributes from the defined class
    accessible while preserving iterable interface.
    """

    def __new__(mcs, name, bases, dct):
        new_object = super(ChoicesMeta, mcs).__new__(mcs, name, bases, dct)

        # Ensure further initialization is only performed
        # for subclasses of `Choises` (excluding `Choises` class itself).
        if not any(isinstance(base, mcs) for base in bases):
            return new_object

        # Build AST from source to get attributes order
        choices_source_code = unindent_block(inspect.getsource(new_object))
        choices_ast = ast.parse(choices_source_code)

        # Prevent overriding tuple's internals
        illegal_attributes = dir(AttributedTuple) + ['__dict__', '_fields']
        node_visitor = AssignNodeVisitor(illegal_attributes=illegal_attributes)
        node_visitor.visit(choices_ast)
        attributes = node_visitor.visited_attributes

        # Ensure every item has a label: use attribute name when missing
        seq = [dct[key] if isinstance(dct[key], tuple) else (dct[key], key)
               for key in attributes]

        TupleClass = type(name + 'TupleClass', (AttributedTuple,),
                          {'_fields': attributes})
        return TupleClass(seq)


class Choices(object):
    __metaclass__ = ChoicesMeta
