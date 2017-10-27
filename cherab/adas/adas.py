
# Copyright 2014-2017 United Kingdom Atomic Energy Authority
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

import os

from cherab.core import AtomicData, Element, Isotope
from cherab.adas.adas4xx.adas405 import run_adas405
from cherab.adas.rates.radiated_power import RadiatedPower, StageResolvedLineRadiation
from cherab.adas.rates.fractional_abundance import FractionalAbundance


class ADAS(AtomicData):

    def __init__(self, data_path=None, permit_extrapolation=False):

        super().__init__()
        self._data_path = self._locate_data(data_path)

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

    @property
    def data_path(self):
        return self._data_path

    def _locate_data(self, data_path):

        if data_path is None:

            search_paths = []

            # adas home directory
            try:
                search_paths.append(os.path.join(os.environ["ADASHOME"], "adas"))
            except KeyError:
                search_paths.append("/home/adas/adas")

            for path in search_paths:
                if os.path.isdir(path):
                    data_path = path
                    break
            else:
                raise IOError("Could not find the ADAS data directory.")

        return data_path

    def radiated_power_rate(self, ion, radiation_type):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        name = 'Radiated Power - ({}, {})'.format(ion.symbol, radiation_type)
        electron_densities, electron_temperatures, _, total_power_array, plt_array, prb_array, prc_array, _ = run_adas405(elem=ion.symbol.lower())

        if radiation_type == 'total':
            return RadiatedPower(ion, radiation_type, electron_densities, electron_temperatures, total_power_array,
                                 name=name, extrapolate=self._permit_extrapolation)

        elif radiation_type == 'line':
            return RadiatedPower(ion, radiation_type, electron_densities, electron_temperatures, plt_array,
                                 name=name, extrapolate=self._permit_extrapolation)

        elif radiation_type == 'continuum':
            return RadiatedPower(ion, radiation_type, electron_densities, electron_temperatures, prb_array,
                                 name=name, extrapolate=self._permit_extrapolation)

        elif radiation_type == 'cx':
            return RadiatedPower(ion, radiation_type, electron_densities, electron_temperatures, prc_array,
                                 name=name, extrapolate=self._permit_extrapolation)

        else:
            raise ValueError("RadiatedPower() radiation type must be one of ['total', 'line', 'continuum', 'cx'].")

    def stage_resolved_line_radiation_rate(self, ion, ionisation):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        electron_densities, electron_temperatures, _, _, _, _, _, stage_resolved_line_radiation = run_adas405(elem=ion.symbol.lower())

        name = 'Stage Resolved Line Radiation - ({}, {})'.format(ion.symbol, ionisation)
        return StageResolvedLineRadiation(ion, ionisation, electron_densities, electron_temperatures,
                                          stage_resolved_line_radiation[:, :, ionisation],
                                          name=name, extrapolate=self._permit_extrapolation)

    def fractional_abundance(self, ion, ionisation):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        electron_densities, electron_temperatures, fraction, _, _, _, _, _ = run_adas405(elem=ion.symbol.lower())
        name = ion.symbol + '_' + str(ionisation)
        return FractionalAbundance(ion, ionisation, electron_densities, electron_temperatures, fraction[:, :, ionisation], name=name)


