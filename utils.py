class MultiElementDelete(list):
    def __delitem__(self, key):
        if isinstance(key, (list, tuple)):
            for index in sorted(set(key), reverse=True):
                list.__delitem__(self, index)
        else:
            list.__delitem__(self, key)
