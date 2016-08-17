django-choices-sugar
====================

A cleaner approach to declare "choices" in Django.

Standard Django way to define choices for model/form fields is to use iterable consisting of two items tuples:

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

django-choices-sugar introduces more *enum* like approach:

```python
from django.db import models
from django.utils.translation import ugettext_lazy as _

from choices_sugar import Choices


class Ticket(models.Model):

    class StatusChoices(Choices):
        NEW = 0, _('New')
        PENDING = 1, _('Pending')
        ACCEPTED = 2, _('Accepted')
        REJECTED = 3, _('Rejected')

    status = models.SmallIntegerField(
        choices=StatusChoices,
        default=StatusChoices.NEW,
    )
```

Labels can be skipped. As Django requires to have them defined, ``Choices`` class will use attribute name when missing:

```python
    class StatusChoices(Choices):
        YES = 1
        NO = 0
```

The code above is equivalent to ```StatusChoices = ((1, 'YES'), (0, 'NO'))```.


Goals
-----
- tuple compatibility
- preserved items order
- compact, enum like notation


Challenges
----------
In Python 2 there is no elegant way to resolve primitive value attributes order in which they were entered.
Solution which django-choices-sugar implements is by leveraging reflection. However, Python's ``inspect``
module method ``findsource``, which we mainly rely on, is inaccurate when two or more class objects
with the same name exist in the same module (even in different scopes). This is a serious drawback,
as such cases are likely to occur, eg. status choices for two or more models in one module.

**A few workarounds and improvements are in progress...**
