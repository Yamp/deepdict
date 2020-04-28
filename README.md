# deepdict
Infinite recursive dotted dict


```python
from deepdict.deepdict import DeepDict
d = DeepDict()
d.x.y.z = 1
d.x.y.bar = 'foo'
>>> DeepDict(<class 'deepdict.deepdict.DeepDict'>,
         {'x': DeepDict(<class 'deepdict.deepdict.DeepDict'>,
                        {'y': DeepDict(<class 'deepdict.deepdict.DeepDict'>,
                                       {'bar': 'foo',
                                        'z': 1})})})
```
