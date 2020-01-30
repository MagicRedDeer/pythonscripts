import re
import os.path
import types


class PathMapping(dict):
    '''An extension of a python dictionary which enables lookups for paths
    using tokens.
    Misses / or token based lookups cost n where n is the size of the
    dictionary'''
    curdir = '.'

    __tokens__ = {
            '<f>': r'\d+',
            '<udim>': r'\d{4}',
            '\\?+': lambda tt: '\d{%d}' % len(tt),
            '#+': lambda tt: '\d{%d}' % len(tt)
            }

    @classmethod
    def token_re(cls, token_type):
        if not token_type:
            return ''
        for ttype, texp in cls.__tokens__.items():
            if re.match(ttype, token_type, re.I):
                return '(%s)' % (
                        texp(token_type)
                        if isinstance(texp, types.FunctionType)
                        else texp)
        raise ValueError('Unknown Token Type %s' % token_type)

    @classmethod
    def token_type(cls, key):
        dirname, basename = os.path.split(key)
        for token in cls.__tokens__:
            match = re.search(token, basename, re.I)
            if match:
                return match.group()
        return ''

    def key_matches(self, key, frame_no=False):
        matches = []
        key = os.path.normpath(key)
        dirname, basename = os.path.split(key)

        token_type = self.token_type(basename)

        key_pat = basename
        if token_type:
            token_re = self.token_re(token_type)
            key_pat = basename.replace(token_type, token_re)
        else:
            frame_no = False
        dirname = os.path.join(dirname, '').replace('\\', '\\\\')
        key_pat = dirname + key_pat

        for _key in self.keys():
            match = re.match(key_pat, os.path.normpath(_key))
            if match:
                if frame_no:
                    matches.append((
                        match.group(), match.group(1)))
                else:
                    matches.append(match.group())
        return matches

    def replace_with_tokens(self, key, val, match):
        token_type = self.token_type(key)
        if token_type:
            dirname, basename = os.path.split(val)
            basename = re.sub(match[1], token_type, basename)
            val = os.path.normpath(os.path.join(dirname, basename))
        return val

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        super(PathMapping, self).__setitem__(key, value)

    def __getitem__(self, key):
        try:
            return super(PathMapping, self).__getitem__(key)
        except KeyError:
            matches = self.key_matches(key, True)
            if not matches:
                raise
            val = super(PathMapping, self).__getitem__(matches[0][0])
            return self.replace_with_tokens(key, val, matches[0])

    def __contains__(self, key):
        if super(PathMapping, self).__contains__(key):
            return True
        return self.key_matches(key)

    has_key = __contains__

mapping = {
        u'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0001.jpg': u'D:\\temp\\pics\\003\\smart_car_open.0001.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0002.jpg': 'D:\\temp\\pics\\003\\smart_car_open.0002.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0003.jpg': 'D:\\temp\\pics\\003\\smart_car_open.0003.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0004.jpg': 'D:\\temp\\pics\\003\\smart_car_open.0004.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0005.jpg': 'D:\\temp\\pics\\003\\smart_car_open.0005.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\open\\smart_car_open.0006.jpg': 'D:\\temp\\pics\\003\\smart_car_open.0006.jpg',
        u'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0001.jpg': u'D:\\temp\\pics\\003\\smart_car_quiet.0001.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0002.jpg': 'D:\\temp\\pics\\003\\smart_car_quiet.0002.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0003.jpg': 'D:\\temp\\pics\\003\\smart_car_quiet.0003.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0004.jpg': 'D:\\temp\\pics\\003\\smart_car_quiet.0004.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0005.jpg': 'D:\\temp\\pics\\003\\smart_car_quiet.0005.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\quiet\\smart_car_quiet.0006.jpg': 'D:\\temp\\pics\\003\\smart_car_quiet.0006.jpg',
        u'D:\\talha.ahmed\\Pictures\\smart_car\\round\\smart_car_round.0001.jpg': u'D:\\temp\\pics\\003\\smart_car_round.0001.jpg',
        u'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0001.jpg': u'D:/temp\\pics\\003\\smart_car_wide.0001.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0002.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0002.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0003.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0003.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0004.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0004.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0005.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0005.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0006.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0006.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0007.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0007.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0008.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0008.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0009.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0009.jpg',
        'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.0010.jpg': 'D:\\temp\\pics\\003\\smart_car_wide.0010.jpg'
}


path = 'D:\\talha.ahmed\\Pictures\\smart_car/wide/smart_car_wide.<f>.jpg'
path2 = 'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.####.jpg'
path3 = 'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.????.jpg'
path4 = 'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.<udim>.jpg'
path4 = 'D:\\talha.ahmed\\Pictures\\smart_car\\wide\\smart_car_wide.????.jpg'
pathmap = PathMapping(mapping)
print pathmap[path]
print pathmap[path2]
print pathmap[path3]
print pathmap[path4]
print pathmap['hello']
