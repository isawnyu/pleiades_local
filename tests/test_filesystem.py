#
# This file is part of pleiades_local
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test the pleiades_local.filesystem
"""

from pathlib import Path
from pleiades_local.filesystem import (
    PleiadesFilesystem,
    PleiadesFilesystemError,
    PleiadesFilesystemNotIndexedError,
)
from pytest import raises


class TestSimple:
    def test_all(self):
        pfs = PleiadesFilesystem(Path("tests/data/simple/"))
        pfs.verify_index()
        assert len(pfs.index) == 1
        j = pfs.get("295374")
        with raises(PleiadesFilesystemNotIndexedError):
            j = pfs.get("8675309")


class TestComplex:
    def test_all(self):
        pfs = PleiadesFilesystem(Path("tests/data/complex/"))
        pfs.verify_index()
        assert len(pfs.index) == 362
        j = pfs.get("101778129")
        with raises(PleiadesFilesystemNotIndexedError):
            j = pfs.get("8675309")


class TestPreindexed:
    def test_all_valid(self):
        root_path = Path("tests/data/preindexed/")
        pfs = PleiadesFilesystem(root_path, catalog=root_path / "catalog.json")
        pfs.verify_index()
        assert len(pfs.index) == 362
        j = pfs.get("101778129")
        with raises(PleiadesFilesystemNotIndexedError):
            j = pfs.get("8675309")

    def test_all_invalid(self):
        root_path = Path("tests/data/preindexed_invalid/")
        pfs = PleiadesFilesystem(root_path, catalog=root_path / "catalog.json")
        with raises(PleiadesFilesystemError):
            pfs.verify_index()
