You can do stuff like this:

```
Python 3.11.3 (main, Apr 12 2023, 15:40:43) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from pleiades_local.filesystem import PleiadesFilesystem
>>> from pathlib import Path
>>> root_path = "/Users/paregorios/Documents/files/P/pleiades.datasets/data/json"
>>> root_path = Path(root_path)
>>> root_path.exists()
True
>>> pfs = PleiadesFilesystem(root_path)
>>> len(pfs.index)
39954
>>> j = pfs.get("8675309")
>>> j["title"]
'Hermeskeil Roman Camp'
```