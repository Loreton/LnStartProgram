
import copy


    # #########################################################################
    # - merge dictionaries
    # - d1 will be modified
    # -     call function using dict(d1) if you wish mantain the original
    # #########################################################################
def _dict_merge(self, d1, d2, path=None, update=True):  # GOOD
    """http://stackoverflow.com/questions/7204805/python-dictionaries-of-dictionaries-merge"
    merges d2 into d1"""
    if path is None: path = []
    for key in d2:
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                self._dict_merge(d1[key], d2[key], path + [str(key)], update=update)
            elif d1[key] == d2[key]:
                pass # same leaf value
            elif isinstance(d1[key], list) and isinstance(d2[key], list):
                for idx, val in enumerate(d2[key]):
                    d1[key][idx] = self._dict_merge(d1[key][idx], d2[key][idx], path + [str(key), str(idx)], update=update)
            elif update:
                d1[key] = d2[key]
            else:
                raise Exception('Conflict at {}'.format('.'.join(path + [str(key)])))
        else:
            d1[key] = d2[key]
    return d1


