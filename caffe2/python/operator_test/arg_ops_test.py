# Copyright (c) 2016-present, Facebook, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hypothesis.strategies as st
import numpy as np

from caffe2.python import core
from hypothesis import given
import caffe2.python.hypothesis_test_util as hu


class TestArgOps(hu.HypothesisTestCase):
    def argmax_ref(self, X, axis, keepdims):
            indices = np.argmax(X, axis=axis)
            if keepdims:
                out_dims = list(X.shape)
                out_dims[axis] = 1
                indices = indices.reshape(tuple(out_dims))
            return [indices]

    @given(X=hu.tensor(dtype=np.float32), axis=st.integers(-1, 5),
            keepdims=st.booleans(), **hu.gcs)
    def test_argmax(self, X, axis, keepdims, gc, dc):
        if axis >= len(X.shape):
            axis %= len(X.shape)
        op = core.CreateOperator(
            "ArgMax", ["X"], ["Indices"], axis=axis, keepdims=keepdims,
            device_option=gc)

        def argmax_ref(X):
            indices = np.argmax(X, axis=axis)
            if keepdims:
                out_dims = list(X.shape)
                out_dims[axis] = 1
                indices = indices.reshape(tuple(out_dims))
            return [indices]

        self.assertReferenceChecks(gc, op, [X], argmax_ref)
        self.assertDeviceChecks(dc, op, [X], [0])

    @given(X=hu.tensor(dtype=np.float32), axis=st.integers(-1, 5),
            keepdims=st.booleans(), **hu.gcs)
    def test_argmin(self, X, axis, keepdims, gc, dc):
        if axis >= len(X.shape):
            axis %= len(X.shape)
        op = core.CreateOperator(
            "ArgMin", ["X"], ["Indices"], axis=axis, keepdims=keepdims,
            device_option=gc)

        def argmin_ref(X):
            indices = np.argmin(X, axis=axis)
            if keepdims:
                out_dims = list(X.shape)
                out_dims[axis] = 1
                indices = indices.reshape(tuple(out_dims))
            return [indices]

        self.assertReferenceChecks(gc, op, [X], argmin_ref)
        self.assertDeviceChecks(dc, op, [X], [0])


if __name__ == "__main__":
    import unittest
    unittest.main()
