# Copyright 2016-2021 Euratom
# Copyright 2016-2021 United Kingdom Atomic Energy Authority
# Copyright 2016-2021 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

import numpy as np
from libc.math cimport INFINITY

from raysect.core.math.function.float cimport Interpolator2DArray


cdef class FractionalAbundance(CoreFractionalAbundance):

    def __init__(self, element, ionisation, electron_density, electron_temperature, fractional_abundance, name='', extrapolate=False):

        super().__init__(element, ionisation, name)

        self.raw_data = {'ne': np.array(electron_density, np.float64),
                         'te': np.array(electron_temperature, np.float64),
                         'fractional_abundance': np.array(fractional_abundance, np.float64)}

        # store limits of data
        self.density_range = self.raw_data['ne'].min(), self.raw_data['ne'].max()
        self.temperature_range = self.raw_data['te'].min(), self.raw_data['te'].max()

        # interpolate fractional abundance
        extrapolation_type = 'linear' if extrapolate else 'none'
        self._abundance_func = Interpolator2DArray(self.raw_data['ne'], self.raw_data['te'], self.raw_data['fractional_abundance'],
                                                   'cubic', extrapolation_type, INFINITY, INFINITY)

    cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:

        # prevent negative values (possible if extrapolation enabled)
        return max(0, self._abundance_func.evaluate(electron_density, electron_temperature))