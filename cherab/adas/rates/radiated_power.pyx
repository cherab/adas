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
from libc.math cimport INFINITY, log10

from raysect.core.math.function.float cimport Interpolator2DArray


cdef class TotalRadiatedPower(CoreTotalRadiatedPower):

    def __init__(self, element, electron_density, electron_temperature, radiated_power, extrapolate=False):

        super().__init__(element)

        self.raw_data = {'ne': np.array(electron_density, np.float64),
                         'te': np.array(electron_temperature, np.float64),
                         'rate': np.array(radiated_power, np.float64)}

        # store limits of data
        self.density_range = self.raw_data['ne'].min(), self.raw_data['ne'].max()
        self.temperature_range = self.raw_data['te'].min(), self.raw_data['te'].max()

        # interpolate rate
        # using nearest extrapolation to avoid infinite values at 0 for some rates
        extrapolation_type = 'nearest' if extrapolate else 'none'
        self._rate = Interpolator2DArray(np.log10(self.raw_data['ne']), np.log10(self.raw_data['te']), np.log10(self.raw_data['rate']),
                                         'cubic', extrapolation_type, INFINITY, INFINITY)

    cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:

        # need to handle zeros, also density and temperature can become negative due to cubic interpolation
        if electron_density < 1.e-300:
            electron_density = 1.e-300

        if electron_temperature < 1.e-300:
            electron_temperature = 1.e-300

        # calculate rate and convert from log10 space to linear space
        return 10 ** self._rate.evaluate(log10(electron_density), log10(electron_temperature))
