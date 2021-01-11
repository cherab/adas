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
from adas import run_adas405 as _run_adas405


_cached_adas405_calls = {}

_electron_densities = [10**x * 1E6 for x in np.linspace(7.7, 15.3, num=24)]
_electron_temperatures = [10**x for x in np.linspace(-0.7, 4.2, num=100)]


def run_adas405(uid='adas', year=96, elem='ne'):

    unique_cache_id = (uid, year, elem)

    try:
        fractional_array, total_power_array, plt_array, prb_array, prc_array, stage_resolved_line_radiation = _cached_adas405_calls[unique_cache_id]

    except KeyError:
        ne_list = []
        te_list = []
        for ne in _electron_densities:
            for te in _electron_temperatures:
                ne_list.append(ne * 1E-6)
                te_list.append(te)

        fraction, power = _run_adas405(uid=uid, year=year, elem=elem, te=te_list, dens=ne_list)

        fractional_array = fraction['ion']
        number_species = fractional_array.shape[-1]
        fractional_array = fractional_array.reshape((len(_electron_densities), len(_electron_temperatures), number_species))

        total_power_array = power['total'].reshape((len(_electron_densities), len(_electron_temperatures))) * 1E6
        plt_array = power['plt'].reshape((len(_electron_densities), len(_electron_temperatures))) * 1E6
        prb_array = power['prb'].reshape((len(_electron_densities), len(_electron_temperatures))) * 1E6
        prc_array = power['prc'].reshape((len(_electron_densities), len(_electron_temperatures))) * 1E6
        stage_resolved_line_radiation = power['ion'].reshape((len(_electron_densities), len(_electron_temperatures), number_species)) * 1E6

        _cached_adas405_calls[unique_cache_id] = (fractional_array, total_power_array, plt_array, prb_array, prc_array, stage_resolved_line_radiation)

    return _electron_densities, _electron_temperatures, fractional_array, total_power_array, plt_array, prb_array, prc_array, stage_resolved_line_radiation
