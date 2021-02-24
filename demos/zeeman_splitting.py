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

# External imports
from numpy import cos, sin, deg2rad
import matplotlib.pyplot as plt
from scipy.constants import electron_mass, atomic_mass
from raysect.optical import World, Vector3D, Point3D, Ray
from raysect.primitive import Sphere
from raysect.optical.material.emitter.inhomogeneous import NumericalIntegrator

# Cherab imports
from cherab.core import Species, Maxwellian, Plasma, Line
from cherab.core.atomic.elements import deuterium, beryllium
from cherab.core.model import ExcitationLine, RecombinationLine, ZeemanMultiplet
from cherab.adas import ADAS
from cherab.tools.plasmas import GaussianVolume

# Uncomment this if local ADAS respository is not populated
# from cherab.adas.repository import populate
# populate()

# tunables
ion_density = 1e19
sigma = 0.25

# setup scenegraph
world = World()

# create atomic data source
adas = ADAS(permit_extrapolation=True)

# PLASMA ----------------------------------------------------------------------
plasma = Plasma(parent=world)
plasma.atomic_data = adas
plasma.geometry = Sphere(sigma * 5.0)
plasma.geometry_transform = None
plasma.integrator = NumericalIntegrator(step=sigma / 5.0)

# define basic distributions
d_density = GaussianVolume(0.5 * ion_density, sigma * 10000)
be1_density = GaussianVolume(0.01 * ion_density, sigma * 10000)
e_density = GaussianVolume(ion_density, sigma * 10000)
temperature = GaussianVolume(39, sigma) + 1
bulk_velocity = Vector3D(0, 0, 0)

deuterium_mass = deuterium.atomic_weight * atomic_mass
beryllium_mass = beryllium.atomic_weight * atomic_mass
d0_distribution = Maxwellian(d_density, temperature * 0.5, bulk_velocity, deuterium_mass)
d1_distribution = Maxwellian(d_density, temperature, bulk_velocity, deuterium_mass)
be1_distribution = Maxwellian(be1_density, temperature, bulk_velocity, beryllium_mass)
be2_distribution = Maxwellian(be1_density * 2, temperature, bulk_velocity, beryllium_mass)
e_distribution = Maxwellian(e_density, temperature, bulk_velocity, electron_mass)

d0_species = Species(deuterium, 0, d0_distribution)
d1_species = Species(deuterium, 1, d1_distribution)
be1_species = Species(beryllium, 1, be1_distribution)
be2_species = Species(beryllium, 2, be2_distribution)

# define magnetic field
b_field = Vector3D(0, 0, 6.0)
plasma.b_field = b_field

# define species
plasma.electron_distribution = e_distribution
plasma.composition = [d0_species, d1_species, be1_species, be2_species]

# setup D-alpha line
deuterium_I_656 = Line(deuterium, 0, (3, 2))  # n = 3->2: 656.1nm

# setup Be II 527 nm line
beryllium_II_527 = Line(beryllium, 1, ("4s1 2s0.5", "3p1 2p2.5"))  # 527 nm

# angles between the ray and the magnetic field direction
angles = (0., 45., 90.)

# add ZeemanMultiplet model of D-alpha line to the plasma
zeeman_structure = adas.zeeman_structure(deuterium_I_656)

plasma.models = [
    ExcitationLine(deuterium_I_656, lineshape=ZeemanMultiplet, lineshape_args=[zeeman_structure]),
    RecombinationLine(deuterium_I_656, lineshape=ZeemanMultiplet, lineshape_args=[zeeman_structure])
]

# Ray-trace the spectrum again
multiplet = []
for angle in angles:
    angle_rad = deg2rad(angle)
    r = Ray(origin=Point3D(0, -5 * sin(angle_rad), -5 * cos(angle_rad)), direction=Vector3D(0, sin(angle_rad), cos(angle_rad)),
            min_wavelength=655.4, max_wavelength=656.8, bins=500)
    multiplet.append(r.trace(world))

plt.figure()
for i, angle in enumerate(angles):
    plt.plot(multiplet[i].wavelengths, multiplet[i].samples, ls=':', label=r'{}$\degree$'.format(angle))
plt.text(0.05, 0.9, 'B = {} T'.format(b_field.length), transform=plt.gca().transAxes)
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Radiance (W/m^2/str/nm)')
plt.title(r'D$\alpha$ spectrum observed at different angles\nbetween ray and magnetic field')

# add ZeemanMultiplet model of Be II 527 nm line to the plasma
zeeman_structure = adas.zeeman_structure(beryllium_II_527)

plasma.models = [
    ExcitationLine(beryllium_II_527, lineshape=ZeemanMultiplet, lineshape_args=[zeeman_structure]),
    RecombinationLine(beryllium_II_527, lineshape=ZeemanMultiplet, lineshape_args=[zeeman_structure])
]

# Ray-trace the spectrum again
multiplet = []
for angle in angles:
    angle_rad = deg2rad(angle)
    r = Ray(origin=Point3D(0, -5 * sin(angle_rad), -5 * cos(angle_rad)), direction=Vector3D(0, sin(angle_rad), cos(angle_rad)),
            min_wavelength=526.7, max_wavelength=527.5, bins=500)
    multiplet.append(r.trace(world))

plt.figure()
for i, angle in enumerate(angles):
    plt.plot(multiplet[i].wavelengths, multiplet[i].samples, ls=':', label=r'{}$\degree$'.format(angle))
plt.text(0.05, 0.9, 'B = {} T'.format(b_field.length), transform=plt.gca().transAxes)
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Radiance (W/m^2/str/nm)')
plt.title('Be II 4s1 2s0.5 -> 3p1 2p2.5 spectrum observed\nat different angles between ray and magnetic field')

plt.show()
