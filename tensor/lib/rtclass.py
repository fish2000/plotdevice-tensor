
from __future__ import print_function
# from functools import partial
import sys, objc, warnings

OBJ_COLON = '_'

class ObjCAncestor(type):
    """ Subclass RTClass using the name of an Objective-C class
        to generate a pythonic wrapper (if you like your syntax sweet)
        """
    def __init__(cls, name, bases, attrs):
        # print("%s, (%s) {%s}" % (name, bases, attrs.keys()))
        # creator = partial(cls.__new__, cls)
        if name == 'RTClass':
            # Don't search for something named RTClass
            super(ObjCAncestor, cls).__init__(name, bases, attrs)
            return
        try:
            cls.__rtbase__ = objc.lookUpClass(name)
        except objc.nosuchclass_error:
            warnings.warn("Objective-C class '%s' not found" % name)
            super(ObjCAncestor, cls).__init__(name, bases, attrs)
            return
        super(ObjCAncestor, cls).__init__(name, tuple([cls.__rtbase__] + list(bases) + [object]), attrs)

class RTClass(object):
    __metaclass__ = ObjCAncestor

    def __init__(self, *args, **kwargs):
        """ Allow PyObjC-based RTClass subclasses to initialize pythonically e.g.

            nsarray = NSArray() # or:
            nsarray = NSArray(other_nsarray,
            init='initWithArray')

            rather than having to do the ObjC allocation/initialization dance:

            nsarray = NSArray.alloc().initWithArray_(other_nsarray) # bah
            """
        cls = self.__class__
        if hasattr(cls, '__rtbase__'):
            objc_cls = cls.__rtbase__
            init_method_name = kwargs.pop('init', 'init')
            if hasattr(objc_cls, 'alloc'):
                instance = objc_cls.alloc()
                init_method = getattr(instance, init_method_name)
                self.__rtinstance__ = init_method(*args)
            elif hasattr(objc_cls, 'init'):
                init_method = getattr(objc_cls, init_method_name)
                self.__rtinstance__ = init_method(*args)
        object.__init__(self, *args, **kwargs)

    def __getattr__(self, attr):
        """ For unknown attributes that don't end in underscores,
            look for their underscored counterpart before bailing. """
        if not attr.endswith(OBJ_COLON):
            alt_attr = attr + OBJ_COLON
            if hasattr(self.__rtinstance__, alt_attr):
                return getattr(self.__rtinstance__, alt_attr)
            raise AttributeError('%s (tried with underscore)' % attr)
        if hasattr(self.__rtinstance__, attr):
            return getattr(self.__rtinstance__, attr)
        raise AttributeError(attr)

    def __repr__(self):
        # This may be a bad idea, let's find out
        return "(%s) <<- %s" % (
                                self.__class__.__name__,
                                super(RTClass, self).__repr__())



if __name__ == '__main__':
    try:
        import tensorlib
    except ImportError:
        sys.exit(1)

    class NSImage(RTClass):
        pass

    class PolkaDotFilter(RTClass):
        pass

    polkadotter = PolkaDotFilter()

    print(polkadotter)
    print(polkadotter.__class__)
    print(polkadotter.__class__.__bases__)
    #print(polkadotter.process)
    print(polkadotter)
    
    print(dir(tensorlib))
