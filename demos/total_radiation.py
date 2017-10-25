
import matplotlib.pyplot as plt
plt.ion()

from cherab.core.atomic import neon
from cherab.adas import ADAS


print("testing total radiation for Neon")

atomic_data = ADAS()

plt.figure()

ne_total_rad = atomic_data.radiated_power_rate(neon, 'total')
ne_total_rad.plot_temperature()

ne_line_rad = atomic_data.radiated_power_rate(neon, 'line')
ne_line_rad.plot_temperature()

ne_continuum_rad = atomic_data.radiated_power_rate(neon, 'continuum')
ne_continuum_rad.plot_temperature()

plt.xlabel("Electron Temperature (eV)")
plt.ylabel("Total emission (W/m^3)")
plt.title("Neon radiation")
plt.legend(loc=3)

