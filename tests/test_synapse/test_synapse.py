# Copyright 2012-2024 Blue Brain Project / EPFL

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for the synapse module."""

import numpy as np
from pytest import approx

from bluecellulab.synapse import Synapse


def test_calc_u_scale_factor():
    """Test calculation of u_scale_factor against its old implementation."""
    def hill(extracellular_calcium, y, K_half):
        return y * extracellular_calcium**4 / (
            K_half**4 + extracellular_calcium**4)

    def constrained_hill(K_half):
        y_max = (K_half**4 + 16) / 16
        return lambda x: hill(x, y_max, K_half)

    def f_scale(x, y):
        return constrained_hill(x)(y)

    scale_factor = np.vectorize(f_scale)

    a = 4.62799366
    b = 3.27495564

    assert scale_factor(a, 2) == approx(Synapse.calc_u_scale_factor(a, 2))
    assert scale_factor(a, 2.2) == approx(Synapse.calc_u_scale_factor(a, 2.2))
    assert scale_factor(a, b) == approx(Synapse.calc_u_scale_factor(a, b))
