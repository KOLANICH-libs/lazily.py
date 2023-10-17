lazily.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
~~[![GitLab Build Status](https://gitlab.com/KOLANICH/lazily.py/badges/master/pipeline.svg)](https://gitlab.com/KOLANICH/lazily.py/pipelines/master/latest)~~
[![PyPi Status](https://img.shields.io/pypi/v/lazily.py.svg)](https://pypi.python.org/pypi/lazily.py)
~~![GitLab Coverage](https://gitlab.com/KOLANICH/lazily.py/badges/master/coverage.svg)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/lazily.py.svg)](https://libraries.io/github/KOLANICH/lazily.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KOLANICH-libs/lazily.py (the namespace has changed to `KFmts`, which groups packages related to parsing or serialization), grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

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
