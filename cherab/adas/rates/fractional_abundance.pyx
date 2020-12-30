# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
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
from numpy cimport ndarray
from cherab.core.math.interpolators.interpolators2d cimport Interpolate2DCubic
from cherab.core.atomic.rates cimport FractionalAbundance as CoreFractionalAbundance


cdef class FractionalAbundance(CoreFractionalAbundance):

    def __init__(self, element, ionisation, electron_density, electron_temperature, fractional_abundance, name='', extrapolate=False):

        super().__init__(element, ionisation, name)

        self.name = name
        self.element = element
        self.ionisation = ionisation

        self._electron_density = np.array(electron_density)
        self._electron_temperature = np.array(electron_temperature)
        self._fractional_abundance = np.array(fractional_abundance)

        self.density_range = (self._electron_density.min(), self._electron_density.max())
        self.temperature_range = (self._electron_temperature.min(), self._electron_temperature.max())

        self.extrapolate = extrapolate
        self._abundance_func = Interpolate2DCubic(self._electron_density, self._electron_temperature,
                                                  self._fractional_abundance,
                                                  extrapolate=extrapolate, extrapolation_type="quadratic")

    cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:
        return self._abundance_func.evaluate(electron_density, electron_temperature)
