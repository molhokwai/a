# coding: utf8
class aConvert():
    def to_int(self, value):
        """Attention: Eventually returns 0 which 'equals' the False ValueError return"""
        try:
            return int(value)
        except ValueError:
            return False
a_convert=aConvert()
