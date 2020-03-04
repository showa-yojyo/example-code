"""
Overriding descriptor (a.k.a. data descriptor or enforced descriptor):

# BEGIN DESCR_KINDS_DEMO1

    >>> obj = Managed()  # <1>
    >>> obj.over  # <2>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over  # <3>
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7  # <4>
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over  # <5>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> obj.__dict__['over'] = 8  # <6>
    >>> vars(obj)  # <7>
    {'over': 8}
    >>> obj.over  # <8>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

# END DESCR_KINDS_DEMO1

Overriding descriptor without ``__get__``:

(these tests are reproduced below without +ELLIPSIS directives for inclusion in the book;
look for DESCR_KINDS_DEMO2)

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Managed.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get
    9

Non-overriding descriptor (a.k.a. non-data descriptor or shadowable descriptor):

# BEGIN DESCR_KINDS_DEMO3

    >>> obj = Managed()
    >>> obj.non_over  # <1>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7  # <2>
    >>> obj.non_over  # <3>
    7
    >>> Managed.non_over  # <4>
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    >>> del obj.non_over  # <5>
    >>> obj.non_over  # <6>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)

# END DESCR_KINDS_DEMO3

No descriptor type survives being overwritten on the class itself:

# BEGIN DESCR_KINDS_DEMO4

    >>> obj = Managed()  # <1>
    >>> Managed.over = 1  # <2>
    >>> Managed.over_no_get = 2
    >>> Managed.non_over = 3
    >>> obj.over, obj.over_no_get, obj.non_over  # <3>
    (1, 2, 3)

# END DESCR_KINDS_DEMO4

Methods are non-overriding descriptors:

    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> Managed.spam  # doctest: +ELLIPSIS
    <function Managed.spam at 0x...>
    >>> obj.spam()
    -> Managed.spam(<Managed object>)
    >>> Managed.spam()
    Traceback (most recent call last):
      ...
    TypeError: spam() missing 1 required positional argument: 'self'
    >>> Managed.spam(obj)
    -> Managed.spam(<Managed object>)
    >>> Managed.spam.__get__(obj)  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> obj.spam.__func__ is Managed.spam
    True
    >>> obj.spam = 7
    >>> obj.spam
    7


"""

"""
NOTE: These tests are here because I can't add callouts after +ELLIPSIS
directives and if doctest runs them without +ELLIPSIS I get test failures.

# BEGIN DESCR_KINDS_DEMO2

    >>> obj.over_no_get  # <1>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> Managed.over_no_get  # <2>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.over_no_get = 7  # <3>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <4>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.__dict__['over_no_get'] = 9  # <5>
    >>> obj.over_no_get  # <6>
    9
    >>> obj.over_no_get = 7  # <7>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <8>
    9

# END DESCR_KINDS_DEMO2

Methods are non-overriding descriptors:

# BEGIN DESCR_KINDS_DEMO5

    >>> obj = Managed()
    >>> obj.spam  # <1>
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x74c80c>>
    >>> Managed.spam  # <2>
    <function Managed.spam at 0x734734>
    >>> obj.spam = 7  # <3>
    >>> obj.spam
    7

# END DESCR_KINDS_DEMO5

"""

# BEGIN DESCR_KINDS

### auxiliary functions for display only ###

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


### essential classes for this example ###

class Overriding:  # <1>
    """a.k.a. data descriptor or enforced descriptor

    >>> import inspect
    >>> inspect.isdatadescriptor(Overriding())
    True
    >>> inspect.isgetsetdescriptor(Overriding())
    False
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # <2>

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # <3>
    """an overriding descriptor without ``__get__``

    >>> import inspect
    >>> inspect.isdatadescriptor(OverridingNoGet())
    False
    >>> inspect.isgetsetdescriptor(OverridingNoGet())
    False
    """

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # <4>
    """a.k.a. non-data or shadowable descriptor

    >>> import inspect
    >>> inspect.isdatadescriptor(NonOverriding())
    False
    >>> inspect.isgetsetdescriptor(NonOverriding())
    False
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:  # <5>
    """
    >>> import inspect
    >>> m = Managed()
    >>> inspect.isdatadescriptor(m.over)
    False
    >>> inspect.isdatadescriptor(m.over_no_get)
    False
    >>> inspect.isdatadescriptor(m.non_over)
    False
    >>> inspect.isdatadescriptor(Managed.over)
    False
    >>> inspect.isdatadescriptor(Managed.over_no_get)
    False
    >>> inspect.isdatadescriptor(Managed.non_over)
    False
    """

    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # <6>
        print('-> Managed.spam({})'.format(display(self)))

# END DESCR_KINDS

class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.

    >>> class MyClass(object):
    ...     x = RevealAccess(10, 'var "x"')
    ...     y = 5
    ...     def __init__(self):
    ...         self.z = RevealAccess(100, 'var "z"')
    ...
    >>> m = MyClass()
    >>> m.x
    Retrieving var "x"
    10
    >>> MyClass.x
    Retrieving var "x"
    10
    >>> m.x = 20
    Updating var "x"
    >>> m.x
    Retrieving var "x"
    20
    >>> MyClass.x
    Retrieving var "x"
    20
    >>> m.y
    5
    >>> m.z = 200
    >>> m.z
    200
    >>> n = MyClass()
    >>> n.x
    Retrieving var "x"
    20
    >>> type(m).__name__
    'MyClass'
    >>> isinstance(type(m).__dict__['x'], RevealAccess)
    True
    >>> type(m).__dict__['x'].__get__(m, type(m))
    Retrieving var "x"
    20
    >>> type(m).__dict__['x'].__get__(None, type(m))
    Retrieving var "x"
    20
    >>> m.__dict__['z']
    200
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

"""

"""
