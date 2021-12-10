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

import matplotlib.pyplot as plt

from cherab.core.atomic import neon
from cherab.adas import ADAS


print("testing fraction abundance for Neon")

atomic_data = ADAS()

plt.figure()
ne0_frac = atomic_data.fractional_abundance(neon, 0)
ne0_frac.plot_temperature()
ne1_frac = atomic_data.fractional_abundance(neon, 1)
ne1_frac.plot_temperature()
ne2_frac = atomic_data.fractional_abundance(neon, 2)
ne2_frac.plot_temperature()
ne3_frac = atomic_data.fractional_abundance(neon, 3)
ne3_frac.plot_temperature()
ne4_frac = atomic_data.fractional_abundance(neon, 4)
ne4_frac.plot_temperature()
ne5_frac = atomic_data.fractional_abundance(neon, 5)
ne5_frac.plot_temperature()
ne6_frac = atomic_data.fractional_abundance(neon, 6)
ne6_frac.plot_temperature()
ne7_frac = atomic_data.fractional_abundance(neon, 7)
ne7_frac.plot_temperature()
ne8_frac = atomic_data.fractional_abundance(neon, 8)
ne8_frac.plot_temperature()
ne9_frac = atomic_data.fractional_abundance(neon, 9)
ne9_frac.plot_temperature()
ne10_frac = atomic_data.fractional_abundance(neon, 10)
ne10_frac.plot_temperature()
plt.legend()
plt.title("Fractional abundance of Neon in coronal equilibrium")
plt.xlabel("Electron Temperature (eV)")
plt.ylabel("Fractional Abundance")
plt.show()
