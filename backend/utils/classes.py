# -*- coding: utf-8 -*-
'''通用零散的类封装'''


class classproperty(object):
    '''
    from: https://stackoverflow.com/questions/3203286/how-to-create-a-read-only-class-property-in-python#3203659
    '''
    def __init__(self, getter):
        self.getter= getter
    def __get__(self, instance, owner):
        return self.getter(owner)