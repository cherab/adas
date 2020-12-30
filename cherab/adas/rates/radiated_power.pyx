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


cdef class TotalRadiatedPower(CoreTotalRadiatedPower):


    def __init__(self, element, electron_density, electron_temperature, radiated_power, extrapolate=False):

        super().__init__(element)

        self._electron_density = np.array(electron_density, dtype=np.float64)
        self._electron_temperature = np.array(electron_temperature, dtype=np.float64)
        self._radiated_power = np.array(radiated_power, dtype=np.float64)

        self.density_range = (self._electron_density.min(), self._electron_density.max())
        self.temperature_range = (self._electron_temperature.min(), self._electron_temperature.max())

        self.extrapolate = extrapolate
        self._power_func = Interpolate2DCubic(self._electron_density, self._electron_temperature, self._radiated_power,
                                              extrapolate=extrapolate, extrapolation_type="quadratic")

    cdef double evaluate(self, double electron_density, double electron_temperature) except? -1e999:
        return self._power_func.evaluate(electron_density, electron_temperature)
