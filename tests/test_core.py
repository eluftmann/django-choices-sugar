# coding=utf-8

"""
Through all the tests, except for the last one, naming convention
that prevents accidental redeclaration of ``Choices`` subclasses is used.
This is necessary as there is a serious inaccuracy in Python's ``inspect``
module method (``findsource``), which ``Choices`` heavily relies on.

Workaround solution is in progress. For more details see README.md.
"""

import collections
import unittest

from choices_sugar import Choices


class TupleCompatibilityTests(unittest.TestCase):
    """
    Test that ``Choices`` subclasses meet ``tuple`` interface requirements.
    """

    class ValueChoices(Choices):
        A = 1
        B = 2

    class TupleChoices(Choices):
        A = 1, 'A'
        B = 2, 'B'

    def test_instance(self):
        # Strict instance tests sometimes occur, so we want to be sure
        # ``Choices`` subclasses pass them.
        self.assertIsInstance(self.ValueChoices, tuple)
        self.assertIsInstance(self.TupleChoices, tuple)

    def test_items(self):
        self.assertEqual(self.ValueChoices[0], (1, 'A'))
        self.assertEqual(self.ValueChoices[1], (2, 'B'))

        self.assertEqual(self.TupleChoices[0], (1, 'A'))
        self.assertEqual(self.TupleChoices[1], (2, 'B'))

    def test_length(self):
        self.assertEqual(len(self.ValueChoices), 2)
        self.assertEqual(len(self.TupleChoices), 2)

    def test_iterator(self):
        self.assertTrue(hasattr(self.ValueChoices, '__iter__'))
        self.assertIsInstance(self.ValueChoices.__iter__(), collections.Iterator)
        self.assertIsInstance(self.ValueChoices, collections.Iterable)

        self.assertTrue(hasattr(self.TupleChoices, '__iter__'))
        self.assertIsInstance(self.TupleChoices.__iter__(), collections.Iterator)
        self.assertIsInstance(self.TupleChoices, collections.Iterable)

    def test_modification(self):
        def set_value(t):
            t[0][0] = 0

        def set_item(t):
            t[0] = ()

        def set_attribute(t):
            t.new_attribute = 0

        for choices in (self.ValueChoices, self.TupleChoices):
            for method in (set_value, set_item):
                self.assertRaises(TypeError, method, t=choices)

            self.assertRaises(AttributeError, set_attribute, t=choices)


class AttributesTests(unittest.TestCase):
    """
    Test that specified attributes of ``Choices`` subclass are accessible.
    """

    def test_value_choices(self):
        class ValueChoices2(Choices):
            A = 1
            B = 2

        self.assertEqual(ValueChoices2.A, 1)
        self.assertEqual(ValueChoices2.B, 2)

    def test_tuple_choices(self):
        class TupleChoices2(Choices):
            X = 1, 'X'
            Y = 2, 'Y'
            Z = 3

        self.assertEqual(TupleChoices2.X, 1)
        self.assertEqual(TupleChoices2.Y, 2)
        self.assertEqual(TupleChoices2.Z, 3)

    @classmethod
    def _create_choises_with_duplicated_attributes(cls):
        class DuplicatedChoices(Choices):
            A = 1
            A = 2

        return DuplicatedChoices

    @classmethod
    def _create_choises_with_dict_attribute(cls):
        class DictAttributeChoices(Choices):
            __dict__ = {}

        return DictAttributeChoices

    @classmethod
    def _create_choises_with_fields_attribute(cls):
        class FieldsAttributeChoices(Choices):
            _fields = []

        return FieldsAttributeChoices

    def test_duplicates(self):
        self.assertRaises(ValueError, self._create_choises_with_duplicated_attributes)

    def test_illegal_attributes(self):
        self.assertRaises(TypeError, self._create_choises_with_dict_attribute)
        self.assertRaises(TypeError, self._create_choises_with_fields_attribute)


class LabelsTests(unittest.TestCase):
    """
    Test that ``Choices`` subclasses have labels defined.
    """

    def test_custom_labels(self):
        class CustomLabelTupleChoices(Choices):
            A = 1, 'Label A'
            B = 2, 'Label B'

        self.assertSequenceEqual(
            CustomLabelTupleChoices,
            [(1, 'Label A'), (2, 'Label B')]
        )

    def test_auto_labels(self):
        """Test that missing labels are filled with attributes names."""

        class AutoLabelTupleChoices(Choices):
            NONE = 0, 'ALL'
            A = 1
            B = 2

        self.assertSequenceEqual(
            AutoLabelTupleChoices,
            [(0, 'ALL'), (1, 'A'), (2, 'B')]
        )


class OrderingTests(unittest.TestCase):
    """
    Test that ``Choices`` subclass preserves specified ordering.
    """

    def test_ordering(self):
        class OrderChoices(Choices):
            Z = 4
            A = 2
            C = 3
            B = 1
            L = 0

        self.assertSequenceEqual(
            OrderChoices,
            [(4, 'Z'), (2, 'A'), (3, 'C'), (1, 'B'), (0, 'L')]
        )


@unittest.skip("Workaround solution in progress")
class ClassRedefinitionTests(unittest.TestCase):
    """
    Test redefining ``Choices`` subclass.

    This test should pass, but due to an inaccuracy in Python's ``inspect``
    module method (``findsource``) it does not work for now.

    Workaround solution is in progress.
    """

    def test_redefinition(self):
        class RedefinedChoices(Choices):
            A = 10
            B = 20

        class RedefinedChoices(Choices):
            C = 30
            D = 40

        self.assertSequenceEqual(RedefinedChoices, [(30, 'C'), (40, 'D')])
