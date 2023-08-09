# Copyright 2016-2023 Euratom
# Copyright 2016-2023 United Kingdom Atomic Energy Authority
# Copyright 2016-2023 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
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
import matplotlib.pyplot as plt

from cherab.core.atomic import neon
from cherab.core.math import sample2d_grid
from cherab.atomic import AtomicData
from cherab.adas.install import install_total_power_rate


print("Testing total radiation for Neon.")

# install total radiated power data for neon from ADAS to the atomic data repository
install_total_power_rate(neon)

atomic_data = AtomicData()

electron_density = 1.e19
electron_temperature = np.geomspace(1, 10000, 81)

# Obtaining total radiation using ADAS405 code (equilibrium balance)
total_rad = atomic_data.total_radiated_power(neon)
total_power = sample2d_grid(total_rad, electron_density, electron_temperature).squeeze()

# Obtaining fractional abundance using ADAS405 code
fractional_abundance = np.zeros((neon.atomic_number + 1, electron_temperature.size))
for charge, abundance in enumerate(fractional_abundance):
    fraction = atomic_data.fractional_abundance(neon, charge)
    abundance[:] = sample2d_grid(fraction, electron_density, electron_temperature).squeeze()

# Obtaining line and continuum radiation
line_power = np.zeros((neon.atomic_number, electron_temperature.size))
continuum_power = np.zeros((neon.atomic_number, electron_temperature.size))
for charge in range(neon.atomic_number):
    line_rad = atomic_data.line_radiated_power_rate(neon, charge)
    continuum_rad = atomic_data.continuum_radiated_power_rate(neon, charge + 1)
    line_power[charge] = sample2d_grid(line_rad, electron_density, electron_temperature).squeeze() * fractional_abundance[charge]
    continuum_power[charge] = sample2d_grid(continuum_rad, electron_density, electron_temperature).squeeze() * fractional_abundance[charge + 1]

plt.figure()
plt.plot(electron_temperature, total_power, '-k', label='Total radiation')
plt.plot(electron_temperature, continuum_power.sum(0), ls=':', color='k', label='Recombination + Bremsstr.')
plt.plot(electron_temperature, line_power.sum(0), ls=':', color='0.7', label='Total line radiation')
for charge in range(line_power.shape[0]):
    plt.plot(electron_temperature, line_power[charge], ls='--', label='Ne(+{}) line radiation'.format(charge))
plt.xscale('log')
plt.yscale('log')
plt.ylim(1.e-39, 1.e-31)
plt.xlabel("Electron Temperature (eV)")
plt.ylabel("Power function (W m^3)")
plt.title("Neon radiation")
plt.legend(ncol=2, fontsize=9)
plt.show()
