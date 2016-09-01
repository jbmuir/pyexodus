#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright:
    Lion Krischer (lionkrischer@gmail.com), 2016
:license:
    MIT License
"""
import os

import h5netcdf
import numpy as np

from pyexodus import exodus


def test_initialization(tmpdir):
    """
    Tests initialization.

    Test data has been generated by using the official exodus Python API.
    """
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename,
               mode="w",
               title="Example",
               array_type="numpy",
               numDims=3,
               numNodes=5,
               numElems=6,
               numBlocks=1,
               numNodeSets=0,
               numSideSets=1)
    e.close()

    # Just manually test everything.
    with h5netcdf.File(filename, mode="r") as f:
        assert dict(f.attrs) == {
            'api_version': np.array([6.30000019], dtype=np.float32),
            'file_size': np.array([1], dtype=np.int32),
            'floating_point_word_size': np.array([8], dtype=np.int32),
            'int64_status': np.array([0], dtype=np.int32),
            'maximum_name_length': np.array([32], dtype=np.int32),
            'title': 'Example',
            'version': np.array([6.30000019], dtype=np.float32)}

        assert dict(f.dimensions) == {
            'four': 4,
            'len_line': 81,
            'len_name': 33,
            'len_string': 33,
            'num_dim': 3,
            'num_el_blk': 1,
            'num_elem': 6,
            'num_nodes': 5,
            'num_side_sets': 1,
            # XXX: This is different from the original file!
            'time_step': 1}

        assert list(f.groups) == []

        # Testing the variables is a bit more effort.

        # Generate with
        # v = f.variables
        # {k: {"dimensions": v[k].dimensions,
        #      "shape": v[k].shape,
        #      "dtype": v[k].dtype,
        #      "attrs": dict(v[k].attrs),
        #      "data": v[k][:]} for k in f.variables.keys()} == \

        expected = {
            'coor_names': {
                'attrs': {},
                'data': np.array([
                    ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                     '', '', '', '', '']], dtype='|S1'),
                'dimensions': ('num_dim', 'len_name'),
                'dtype': np.dtype('S1'),
                'shape': (3, 33)},
            'coordx': {'attrs': {},
                       'data': np.array([0., 0., 0., 0., 0.]),
                       'dimensions': ('num_nodes',),
                       'dtype': np.dtype('float64'),
                       'shape': (5,)},
            'coordy': {'attrs': {},
                       'data': np.array([0., 0., 0., 0., 0.]),
                       'dimensions': ('num_nodes',),
                       'dtype': np.dtype('float64'),
                       'shape': (5,)},
            'coordz': {'attrs': {},
                       'data': np.array([0., 0., 0., 0., 0.]),
                       'dimensions': ('num_nodes',),
                       'dtype': np.dtype('float64'),
                       'shape': (5,)},
            'eb_names': {'attrs': {},
                         'data': np.array([
                             ['', '', '', '', '', '', '', '', '', '', '',
                              '', '', '', '', '', '', '', '', '', '', '',
                              '', '', '', '', '', '', '', '', '', '', '']],
                             dtype='|S1'),
                         'dimensions': ('num_el_blk', 'len_name'),
                         'dtype': np.dtype('S1'),
                         'shape': (1, 33)},
            'eb_prop1': {'attrs': {'name': 'ID'},
                         'data': np.array([-1], dtype=np.int32),
                         'dimensions': ('num_el_blk',),
                         'dtype': np.dtype('int32'),
                         'shape': (1,)},
            'eb_status': {'attrs': {},
                          'data': np.array([0], dtype=np.int32),
                          'dimensions': ('num_el_blk',),
                          'dtype': np.dtype('int32'),
                          'shape': (1,)},
            'ss_names': {'attrs': {},
                         'data': np.array([
                             ['', '', '', '', '', '', '', '', '', '', '',
                              '', '', '', '', '', '', '', '', '', '', '',
                              '', '', '', '', '', '', '', '', '', '', '']],
                             dtype='|S1'),
                         'dimensions': ('num_side_sets', 'len_name'),
                         'dtype': np.dtype('S1'),
                         'shape': (1, 33)},
            'ss_prop1': {'attrs': {'name': 'ID'},
                         'data': np.array([-1], dtype=np.int32),
                         'dimensions': ('num_side_sets',),
                         'dtype': np.dtype('int32'),
                         'shape': (1,)},
            'ss_status': {'attrs': {},
                          'data': np.array([0], dtype=np.int32),
                          'dimensions': ('num_side_sets',),
                          'dtype': np.dtype('int32'),
                          'shape': (1,)},
            'time_whole': {'attrs': {},
                           # XXX: Empty array in original file.
                           'data': np.array([0.], dtype=np.float64),
                           'dimensions': ('time_step',),
                           'dtype': np.dtype('float64'),
                           # XXX: Shape = (0,) in original file.
                           'shape': (1,)}}

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_info_records(tmpdir):
    """
    Does currently not do anything.
    """
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename,
               mode="w",
               title="Example",
               array_type="numpy",
               numDims=3,
               numNodes=5,
               numElems=6,
               numBlocks=1,
               numNodeSets=0,
               numSideSets=1)
    e.put_info_records(strings=[])
    e.close()


def test_put_coords(tmpdir):
    """
    Tests the put_coords() method.
    """
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename,
               mode="w",
               title="Example",
               array_type="numpy",
               numDims=3,
               numNodes=5,
               numElems=6,
               numBlocks=1,
               numNodeSets=0,
               numSideSets=1)
    e.put_info_records(strings=[])

    # Use different dtypes on purpose to test the type conversions.
    e.put_coords(
        xCoords=np.arange(5, dtype=np.float32),
        yCoords=np.arange(5, dtype=np.int32) * 2,
        zCoords=np.arange(5, dtype=np.int64) * 3
    )

    e.close()

    expected = {
        'coordx': {'attrs': {},
                   'data': np.array([0., 1., 2., 3., 4.]),
                   'dimensions': ('num_nodes',),
                   'dtype': np.dtype('float64'),
                   'shape': (5,)},
        'coordy': {'attrs': {},
                   'data': np.array([0., 2., 4., 6., 8.]),
                   'dimensions': ('num_nodes',),
                   'dtype': np.dtype('float64'),
                   'shape': (5,)},
        'coordz': {'attrs': {},
                   'data': np.array([0., 3., 6., 9., 12.]),
                   'dimensions': ('num_nodes',),
                   'dtype': np.dtype('float64'),
                   'shape': (5,)}
    }

    with h5netcdf.File(filename, mode="r") as f:
        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_elem_blk_info(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename,
               mode="w",
               title="Example",
               array_type="numpy",
               numDims=3,
               numNodes=5,
               numElems=6,
               numBlocks=1,
               numNodeSets=0,
               numSideSets=1)
    e.put_info_records(strings=[])

    # Use different dtypes on purpose to test the type conversions.
    e.put_coords(
        xCoords=np.arange(5, dtype=np.float32),
        yCoords=np.arange(5, dtype=np.int32) * 2,
        zCoords=np.arange(5, dtype=np.int64) * 3
    )

    e.put_elem_blk_info(1, "HEX", 6, 3, 0)

    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        # Two new dimensions.
        assert f.dimensions["num_el_in_blk1"] == 6
        assert f.dimensions["num_nod_per_el1"] == 3

        # One new variable.
        expected = {
            "connect1": {"attrs": {"elem_type": "HEX"},
                         "data": np.zeros((6, 3), dtype=np.int32),
                         "dimensions": ("num_el_in_blk1",
                                        "num_nod_per_el1"),
                         "dtype": np.int32,
                         "shape": (6, 3)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_elem_connectivity(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename,
               mode="w",
               title="Example",
               array_type="numpy",
               numDims=3,
               numNodes=5,
               numElems=6,
               numBlocks=1,
               numNodeSets=0,
               numSideSets=1)
    e.put_info_records(strings=[])

    # Use different dtypes on purpose to test the type conversions.
    e.put_coords(
        xCoords=np.arange(5, dtype=np.float32),
        yCoords=np.arange(5, dtype=np.int32) * 2,
        zCoords=np.arange(5, dtype=np.int64) * 3
    )

    e.put_elem_blk_info(1, "HEX", 6, 3, 0)
    e.put_elem_connectivity(1, np.arange(6 * 3) + 7)

    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        # connect1 should now be filled.
        expected = {
            "connect1": {"attrs": {"elem_type": "HEX"},
                         "data": (np.arange(6 * 3) + 7).reshape((6, 3)),
                         "dimensions": ("num_el_in_blk1",
                                        "num_nod_per_el1"),
                         "dtype": np.int32,
                         "shape": (6, 3)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_time(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.put_time(1, 1.1)

    with h5netcdf.File(filename, mode="r") as f:
        np.testing.assert_allclose(f.variables["time_whole"], [1.1])


def test_set_global_variable_number(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_global_variable_number(3)

    with h5netcdf.File(filename, mode="r") as f:
        _d = np.empty((3, 33), dtype="|S1")
        _d.fill("")

        expected = {
            "name_glo_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_glo_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (3, 33)},
            "vals_glo_var": {
                "attrs": {},
                "data": np.zeros((1, 3)),
                "dimensions": ("time_step", "num_glo_var"),
                "dtype": np.float64,
                "shape": (1, 3)}
            }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_global_variable_name(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_global_variable_number(3)
    e.put_global_variable_name(name="hello", index=2)

    _d = np.empty((3, 33), dtype="|S1")
    _d.fill("")
    _d[1][:5] = list("hello")

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "name_glo_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_glo_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (3, 33)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_get_global_variable_names(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")
    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_global_variable_number(3)
    e.put_global_variable_name(name="hello", index=2)
    assert e.get_global_variable_names() == ['', 'hello', '']


def test_put_global_variable_value(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_global_variable_number(3)
    e.put_global_variable_name(name="hello", index=2)

    e.put_global_variable_value("hello", 1, 1.1)

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "vals_glo_var": {
                "attrs": {},
                "data": [[0, 1.1, 0]],
                "dimensions": ("time_step", "num_glo_var"),
                "dtype": np.float64,
                "shape": (1, 3)}
            }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_set_element_variables(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_element_variable_number(5)
    e.close()

    _d = np.empty((5, 33), dtype="|S1")
    _d.fill("")

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "name_elem_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_elem_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (5, 33)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_element_variable_name(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_element_variable_number(5)
    e.put_element_variable_name("random", 3)
    e.close()

    _d = np.empty((5, 33), dtype="|S1")
    _d.fill("")
    _d[2][:6] = list("random")

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "name_elem_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_elem_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (5, 33)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_get_element_variable_names(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_element_variable_number(5)
    e.put_element_variable_name("random", 3)

    assert e.get_element_variable_names() == ["", "", "random", "", ""]


def test_put_element_variable_values(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_element_variable_number(5)
    e.put_element_variable_name("random", 3)
    # requires an actual element block.
    e.put_elem_blk_info(1, "HEX", 6, 3, 0)
    e.put_element_variable_values(1, "random", 1, np.arange(6))

    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "vals_elem_var3eb1": {
                "attrs": {},
                "data": np.arange(6, dtype=np.float64).reshape(1, 6),
                "dimensions": ("time_step", "num_el_in_blk1"),
                "dtype": np.float64,
                "shape": (1, 6)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_set_node_variable_number(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_node_variable_number(2)

    _d = np.empty((2, 33), dtype="|S1")
    _d.fill("")

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "name_nod_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_nod_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (2, 33)},
            "vals_nod_var1": {
                "attrs": {},
                "data": np.zeros((1, 5)),
                "dimensions": ("time_step", "num_nodes"),
                "dtype": np.float64,
                "shape": (1, 5)},
            "vals_nod_var1": {
                "attrs": {},
                "data": np.zeros((1, 5)),
                "dimensions": ("time_step", "num_nodes"),
                "dtype": np.float64,
                "shape": (1, 5)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_node_variable_name(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_node_variable_number(2)
    e.put_node_variable_name("good friend", 1)

    _d = np.empty((2, 33), dtype="|S1")
    _d.fill("")
    _d[0][:11] = list("good friend")

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "name_nod_var": {
                "attrs": {},
                "data": _d,
                "dimensions": ("num_nod_var", "len_name"),
                "dtype": np.dtype("|S1"),
                "shape": (2, 33)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_node_variable_values(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_node_variable_number(2)
    e.put_node_variable_name("good friend", 1)
    e.put_node_variable_values("good friend", 1, np.arange(5))

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "vals_nod_var1": {
                "attrs": {},
                "data": np.arange(5).reshape((1, 5)),
                "dimensions": ("time_step", "num_nodes"),
                "dtype": np.float64,
                "shape": (1, 5)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_get_node_variable_names(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.set_node_variable_number(2)
    e.put_node_variable_name("good friend", 1)

    assert e.get_node_variable_names() == ["good friend", ""]


def test_put_side_set_params(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.put_side_set_params(4, 5, 0)
    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "elem_ss1": {
                "attrs": {},
                "data": np.zeros(5),
                "dimensions": ("num_side_ss1",),
                "dtype": np.int32,
                "shape": (5,)},
            "side_ss1": {
                "attrs": {},
                "data": np.zeros(5),
                "dimensions": ("num_side_ss1",),
                "dtype": np.int32,
                "shape": (5,)},
            'ss_prop1': {'attrs': {'name': 'ID'},
                         'data': np.array([4], dtype=np.int32),
                         'dimensions': ('num_side_sets',),
                         'dtype': np.dtype('int32'),
                         'shape': (1,)},
            'ss_status': {'attrs': {},
                          'data': np.array([1], dtype=np.int32),
                          'dimensions': ('num_side_sets',),
                          'dtype': np.dtype('int32'),
                          'shape': (1,)},
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_side_set(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.put_side_set_params(4, 5, 0)
    e.put_side_set(4, np.ones(5, dtype=np.int32) * 2,
                   np.ones(5, dtype=np.int32) * 3)
    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            "elem_ss1": {
                "attrs": {},
                "data": [2, 2, 2, 2, 2],
                "dimensions": ("num_side_ss1",),
                "dtype": np.int32,
                "shape": (5,)},
            "side_ss1": {
                "attrs": {},
                "data": [3, 3, 3, 3, 3],
                "dimensions": ("num_side_ss1",),
                "dtype": np.int32,
                "shape": (5,)}
        }

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key


def test_put_side_set_name(tmpdir):
    filename = os.path.join(tmpdir.strpath, "example.e")

    e = exodus(filename, mode="w", title="Example", array_type="numpy",
               numDims=3, numNodes=5, numElems=6, numBlocks=1,
               numNodeSets=0, numSideSets=1)
    e.put_side_set_params(4, 5, 0)
    e.put_side_set(4, np.ones(5, dtype=np.int32) * 2,
                   np.ones(5, dtype=np.int32) * 3)
    e.put_side_set_name(4, "edge of the world")
    e.close()

    with h5netcdf.File(filename, mode="r") as f:
        expected = {
            'ss_names': {'attrs': {},
                         'data': np.array([
                             ['e', 'd', 'g', 'e', ' ', 'o', 'f', ' ',
                              't', 'h', 'e', ' ', 'w', 'o', 'r', 'l', 'd',
                              '', '', '', '', '', '', '', '', '', '', '',
                              '', '', '', '', '']],
                             dtype='|S1'),
                         'dimensions': ('num_side_sets', 'len_name'),
                         'dtype': np.dtype('S1'),
                         'shape': (1, 33)}}

        for key in sorted(expected.keys()):
            a = f.variables[key]
            e = expected[key]

            assert dict(a.attrs) == e["attrs"], key
            np.testing.assert_equal(a[:], e["data"], err_msg=key)
            assert a.dimensions == e["dimensions"], key
            assert a.dtype == e["dtype"], key
            assert a.shape == e["shape"], key
