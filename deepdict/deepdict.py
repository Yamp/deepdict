# -*- coding: utf-8 -*-

import copy
import json
from collections import defaultdict, Mapping

from typing import Dict


class DeepDict(defaultdict):
    def __init__(self, seq=None, **kwargs):
        defaultdict.__init__(self, DeepDict, **kwargs)
        if seq is not None:
            self.from_dict(seq)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __deepcopy__(self, memo=None, _nil=[]):  # noqa
        return DeepDict(
            copy.deepcopy(
                dict(self),
                memo=memo,  # noqa
                _nil=_nil   # noqa
            )
        )

    def from_dict(self, d: Dict):
        for k, v in d.items():
            self[k] = DeepDict()
            if not self._is_dict(v):
                self[k] = v
            else:
                self[k] = DeepDict(v)

    def merge(self, target: Dict) -> 'DeepDict':
        for k in target:
            if isinstance(target[k], DeepDict):
                if isinstance(self[k], DeepDict):
                    self[k].merge(target[k])
                else:
                    self[k] = DeepDict()
                    self.merge(target[k])
            else:
                self[k] = target[k]

        return self

    def clear_empty(self) -> 'DeepDict':
        for k, v in list(self.items()):
            if isinstance(v, DeepDict):
                v.clear_empty()
                if v:
                    del self[k]

        return self

    def to_dict(self):
        DeepDict._to_dict(self)

    @staticmethod
    def _is_dict(obj):
        return isinstance(obj, (DeepDict, dict, Mapping))

    @staticmethod
    def _is_list(obj):
        return isinstance(obj, (tuple, list))

    @classmethod
    def to_deep(cls, obj):
        if cls._is_dict(obj):
            return DeepDict({
                k: cls.to_deep(v)
                for k, v in obj.items()
            })
        elif cls._is_list(obj):
            return [cls.to_deep(v) for v in obj]
        else:
            return copy.deepcopy(obj)

    @classmethod
    def _to_dict(cls, obj):
        if cls._is_dict(obj):
            return {k: cls._to_dict(v) for k, v in obj.items()}
        elif cls._is_list(obj):
            return [cls._to_dict(v) for v in obj]
        else:
            return copy.deepcopy(obj)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)


if __name__ == '__main__':
    dd = DeepDict()
    dd.a.b.c = 1
    dd.a.b.d = 2

    cdd = copy.deepcopy(dd)
