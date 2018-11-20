import operator

from six import string_types, iteritems

from .utils import AttrDict

__all__ = ['Range']

class Range(AttrDict):
    OPS = {
        'lt': operator.lt, 'lte': operator.le,
        'gt': operator.gt, 'gte': operator.ge,
    }

    def __init__(self, *args, **kwargs):
        if args and (
            len(args) > 1 or
            kwargs or
            not isinstance(args[0], dict)
        ):
            raise ValueError('Range accepts a single dictionary or a set of keyword arguments.')
        data = args[0] if args else kwargs
        for k in data:
            if k not in self.OPS:
                raise ValueError('Range received an unknown operator %r' % k)
        super(Range, self).__init__(args[0] if args else kwargs)

    def __repr__(self):
        return 'Range(%s)' % ', '.join('%s=%r' % op for op in iteritems(self._d_))

    def __contains__(self, item):
        if isinstance(item, string_types):
            return super(Range, self).__contains__(item)

        for op in self.OPS:
            if op in self._d_ and not self.OPS[op](item, self._d_[op]):
                return False
        return True
