lazily.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
~~[![GitLab Build Status](https://gitlab.com/KOLANICH/lazily.py/badges/master/pipeline.svg)](https://gitlab.com/KOLANICH/lazily.py/pipelines/master/latest)~~
[![PyPi Status](https://img.shields.io/pypi/v/lazily.py.svg)](https://pypi.python.org/pypi/lazily.py)
~~![GitLab Coverage](https://gitlab.com/KOLANICH/lazily.py/badges/master/coverage.svg)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/lazily.py.svg)](https://libraries.io/github/KOLANICH/lazily.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

Imports lazily. Supports hooks.

Useful when some long loading packages are optional to use by your app, so you don't want to spend time on loading them every time. The arguments are the same as in [`importlib.import_module`](https://docs.python.org/3/library/importlib.html#importlib.import_module).

Requirements
------------
* [`lazy_object_proxy`](https://github.com/ionelmc/python-lazy-object-proxy) [![PyPi Status](https://img.shields.io/pypi/v/lazy-object-proxy.svg)](https://pypi.python.org/pypi/lazy-object-proxy)
[![Libraries.io Status](https://img.shields.io/librariesio/github/ionelmc/python-lazy-object-proxy.svg)](https://libraries.io/github/ionelmc/python-lazy-object-proxy) It hooks into cpython and can catch more kinds of actual using of the object than any pure python implementation.


```python
import freeLunch # ModuleNotFoundError: No module named 'freeLunch'
```

```python
from lazily import freeLunch

freeLunch.consume() # ModuleNotFoundError: No module named 'freeLunch'
```

There is a hooks mechanics, but it is a bit broken, don't use for now:

```python
import lazily
def bar():
	raise ImportError("There ain't no such thing as a free lunch.")
lazily.hooks["freeLunch"] = bar
freeLunch = lazily.lazily("freeLunch")

freeLunch.consume() # ImportError: There ain't no such thing as a free lunch.
```

Obviously, `*` in `fromlist` is UB, as it relies on `__all__`, so `_bootstrap.py` in CPython impl tries to read it.
