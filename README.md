django-choices-sugar
====================

![MIT license](https://img.shields.io/github/license/eluftmann/django-choices-sugar.svg)

A cleaner approach to declare `choices` for models in Django.

Standard way to define choices for model/form fields in Django is to use iterable consisting of (value, label) tuples:

```python
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Ticket(models.Model):
    STATUS_NEW = 0
    STATUS_PENDING = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3
    STATUS_CHOICES = (
        (STATUS_NEW, _('New')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_REJECTED, _('Rejected')),
    )

    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
```

**django-choices-sugar** introduces more *enum* like approach:

```python
from django.db import models
from django.utils.translation import ugettext_lazy as _

from choices_sugar import Choices


class Ticket(models.Model):

    class Status(Choices):
        NEW = 0, _('New')
        PENDING = 1, _('Pending')
        ACCEPTED = 2, _('Accepted')
        REJECTED = 3, _('Rejected')

    status = models.SmallIntegerField(
        choices=Status,
        default=Status.NEW,
    )
```

You can make it even more compact by skipping labels. As Django requires to have them defined, ``Choices`` class will use attribute name when missing:

```python
    class Status(Choices):
        YES = 1
        NO = 0
```

The code above is equivalent to ```StatusChoices = ((1, 'YES'), (0, 'NO'))```.


Goals
-----

- [x] tuple compatibility*
- [x] preserved items order
- [x] compact, enum like notation

Full compatibility with `tuple` may seem unnecessary and it adds some implementation overhead.
However, this may be useful when a 3rd-party library checks field `choices` for strict `tuple` compatibility with `isinstance(choices, tuple)`.
We came across such a case.


Roadmap
-------

- Python 3 support (thanks to PEP 520 it will reduce the codebase and improve reliability - see 'Challenges')


Challenges
----------

In Python 2 there is no elegant way to resolve primitive value attributes order in which they were entered.
Solution which django-choices-sugar implements is by leveraging reflection. However, Python's ``inspect``
module method ``findsource``, which we mainly rely on, is inaccurate when two or more class objects
with the same name exist in the same module (even in different scopes). This is a serious drawback,
as such cases are likely to occur, eg. `Status` choices class for two or more models in one module.

**Workaround with improved ``get_class_source`` method (with scope and attributes checking) is in progress...**
