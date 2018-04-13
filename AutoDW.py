

class MyAbstractClass(object):
    def __new__(cls, *args, **kwargs):
        for needed_function in getattr(cls, 'abstract_methods', []):
            if getattr(cls, needed_function, None) is None:
                raise Exception("Function %s needs to be implemented!" % needed_function)
        return super(MyAbstractClass, cls).__new__(cls)


class CustomObject(MyAbstractClass):
    def __getattribute__(self, key):
        if key.startswith("has_"):
            try:
                return super(CustomObject, self).__getattribute__(key[len("has_"):])
            except:
                return None
        else:
            return super(CustomObject, self).__getattribute__(key)


class Magnet(CustomObject):
    def __init__(self, title, magnet, **kargs):
        self.title = title
        self.magnet = magnet

        for key, value in kargs.iteritems():
            self.__setattr__(key, value)


# def create_item_from_item_dict(item_dict):
#     title = item_dict['item_title']
#     magnet = item_dict['item_magnet']

#     kargs = dict([(key[len("item_"):], val) for key, val in item_dict.copy().iteritems() if str(key).startswith("item_")])
#     del kargs['title']
#     del kargs['magnet']

#     return Magnet(title, magnet, **kargs)
