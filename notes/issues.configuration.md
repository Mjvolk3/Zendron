---
id: jyi08t2esd13ch2vabp3rzs
title: Configuration
desc: ''
updated: 1682505276601
created: 1682505188648
---
- ChatGPT: "Can use the `importlib.resources` module to access the included files:
Since you are using Python 3.10, you should use the `importlib.resources` module (instead of the pkg_resources module) to access the files included with your package. Here's an example of how you can access the `conf/__init__.py` file:"

```python
from importlib.resources import files

default_template_path = files('zendron').joinpath('conf', 'default_template.yaml')
```
