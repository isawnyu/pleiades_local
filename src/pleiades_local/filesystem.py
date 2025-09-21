#
# This file is part of pleiades_local
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Seek and use Pleiades JSON on the filesystem
"""

import json
import os
from pathlib import Path


class PleiadesFilesystemError(Exception):
    def __init__(self, message, pid="", filepath=""):
        self.message = message
        self.pid = pid
        self.filepath = filepath

    def __str__(self):
        return f"{self.message}: pid={self.pid}, filepath={self.filepath}"


class PleiadesFilesystemNotIndexedError(Exception):
    def __init__(self, pid):
        self.message = "No entry for PID in file system index"
        self.pid = pid

    def __str__(self):
        return f"{self.message}: {self.pid}"


class PleiadesFilesystemNoIndexError(Exception):
    pass


class PleiadesFilesystem:
    def __init__(self, root: Path, catalog: Path = None):
        self.index = None
        self.root = root
        if catalog:
            with open(catalog, "r", encoding="utf-8") as fp:
                self.index = json.load(fp)
            del fp
            self.index = {k: Path(v) for k, v in self.index.items()}
        else:
            self.reindex()

    def get(self, pid):
        """Retrieve the JSON for the requested PID"""
        try:
            filepath = self.index[pid]
        except KeyError:
            raise PleiadesFilesystemNotIndexedError(pid)
        else:
            with open(filepath, "r", encoding="utf-8") as fp:
                j = json.load(fp)
            del fp
            return j

    def get_pids(self):
        return list(self.index.keys())

    def reindex(self):
        """Create a new index for the files actually on the filesystem."""
        self.index = dict()
        for entry in self._scantree(self.root):
            if not entry.is_file():
                continue
            parts = entry.name.split(".")
            if len(parts) != 2:
                continue
            stem, suffix = parts
            if suffix != "json":
                continue
            if stem != "catalog":
                try:
                    stem == str(int(stem))
                except (ValueError, TypeError):
                    continue
                try:
                    self.index[stem]
                except KeyError:
                    self.index[stem] = Path(entry)
                else:
                    raise PleiadesFilesystemError(
                        "Multiple JSON files for same PID", stem, entry
                    )

    def verify_index(self):
        """
        Verify that the existing index is valid for the files actually on the filesystem.

        NB: does not detect if there is a file on the filesystem that is not in the index
        """
        if self.index:
            for pid, filepath in self.index.items():
                if filepath.suffix != ".json":
                    raise PleiadesFilesystemError(
                        "File path does not end in '.json'", pid, filepath
                    )
                if not filepath.is_file():
                    raise PleiadesFilesystemError(
                        "File path does not resolve to a file", pid, filepath
                    )
        else:
            raise PleiadesFilesystemNoIndexError(
                "No index is defined for the filesystem."
            )

    def _scantree(self, path):
        """
        Recursively yield DirEntry objects for given directory.
        Code by Sreenath D with Captain Hat:
        https://stackoverflow.com/questions/50948391/whats-the-fastest-way-to-recursively-search-for-files-in-python
        """
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self._scantree(entry.path)
            else:
                yield entry

    def __len__(self):
        return len(self.index)
