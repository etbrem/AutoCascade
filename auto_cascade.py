import re


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
    def __init__(self, title, link, **attributes):
        self.title = title
        self.link = link

        for key, value in attributes.iteritems():
            self.__setattr__(key, value)


def parse_size_string(in_str):
    REGEX_NUMBER = r'(\d+(?:\.\d+)?)'

    multiplier = 1.0
    if not("i" in in_str or ("b" not in in_str and "B" in in_str)):
        multiplier *= 8

    in_str = in_str.lower()
    sizes = {
        "k": 1,
        "m": 2,
        "g": 3,
        "t": 4
    }

    for s, m in sizes.iteritems():
        if s in in_str:
            multiplier *= 1024 ** m

    match = re.search(REGEX_NUMBER, in_str)
    if match:
        multiplier *= float(match.group(1))
    return multiplier


def parse_date_string(date):
    REGEX_UPLOAD_DATE = r'(\d\d)\-(\d\d)\s+(\d{4})'

    month, day, year = -1, -1, -1
    match = re.search(REGEX_UPLOAD_DATE, date)
    if match:
        month, day, year = [int(m) for m in match.groups()]

    return day, month, year