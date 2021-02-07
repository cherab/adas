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
import platform
import os
from subprocess import Popen, PIPE
import numpy as np
from cherab.core.atomic import Line
from cherab.core.atomic.elements import hydrogen, deuterium, tritium, helium, boron, beryllium, carbon, calcium
from cherab.core.atomic.elements import krypton, magnesium, sodium, neon, oxygen, silicon


MULTIPLETS = [Line(boron, 1, ('1s2 2p2 1d2.0', '1s2 2s1 2p1 1p1.0')),
              Line(boron, 1, ('1s2 2s1 4f1 1f3.0', '1s2 2s1 3d1 1d2.0')),
              Line(beryllium, 0, ('2s1 2p1 1p1.0', '2s2 1s0.0')),
              Line(beryllium, 0, ('2s1 3d1 3d7.0', '2s1 2p1 3p4.0')),
              Line(beryllium, 0, ('2p2 3p4.0', '2s1 2p1 3p4.0')),
              Line(beryllium, 1, ('4d1 2d4.5', '3p1 2p2.5')),
              Line(beryllium, 1, ('4f1 2f6.5', '3d1 2d4.5')),
              Line(beryllium, 1, ('4s1 2s0.5', '3p1 2p2.5')),
              Line(beryllium, 2, ('1s1 2p1 3p4.0', '1s1 2s1 3s1.0')),
              Line(carbon, 0, ('2s2 2p1 5d1 3d7.0', '2s2 2p2 3p4.0')),
              Line(carbon, 0, ('2s2 2p1 3d1 3d7.0', '2s2 2p2 3p4.0')),
              Line(carbon, 0, ('2s1 2p3 3d7.0', '2s2 2p2 3p4.0')),
              Line(carbon, 0, ('2s2 2p1 3s1 3p4.0', '2s2 2p2 3p4.0')),
              Line(carbon, 0, ('2s2 2p1 3s1 1p1.0', '2s2 2p2 1s0.0')),
              Line(carbon, 0, ('2s2 2p1 7s1 3p0.0', '2p2 2p1 3p1 3s1.0')),
              Line(carbon, 0, ('2s2 2p1 3p1 3p4.0', '2s2 2p1 3s1 3p4.0')),
              Line(carbon, 1, ('2p3 2d4.5', '2s1 2p2 2p2.5')),
              Line(carbon, 1, ('6f 2f', '3d 2d')),
              Line(carbon, 1, ('2s2 4d1 2d4.5', '2s2 3p1 2p2.5')),
              Line(carbon, 1, ('2s2 3p 2p2.5', '2s1 2p2 2s0.5')),
              Line(carbon, 1, ('2s2 5f1 2f6.5', '2s2 3d1 2d4.5')),
              Line(carbon, 1, ('2s2 4f1 2f6.5', '2s2 3d1 2d4.5')),
              Line(carbon, 1, ('2s2 4p1 2p2.5', '2s2 3d1 2d4.5')),
              Line(carbon, 1, ('2s2 3p1 2p2.5', '2s2 3s1 2s0.5')),
              Line(carbon, 2, ('2p2 1d2.0', '2s1 2p1 1p1.0')),
              Line(carbon, 2, ('2p1 3s1 1p1.0', '2s1 3d1 1d2.0')),
              Line(carbon, 2, ('1s2 2s1 5f1 1f', '1s2 2s1 4d1 1d')),
              Line(carbon, 2, ('4p 1p', '5d 1d')),
              Line(carbon, 2, ('2s1 3p1 3p4.0', '2s1 3s1 3s1.0')),
              Line(carbon, 2, ('2s1 3d1 1d2.0', '2s1 3p1 1p1.0')),
              Line(carbon, 3, ('1s2 5f1 2f6.5', '1s2 4d1 2d4.5')),
              Line(carbon, 3, ('1s2 3p1 2p2.5', '1s2 3s1 2s0.5')),
              Line(carbon, 4, ('1s1 2p1 3p4.0', '1s1 2s1 3s1.0')),
              Line(calcium, 0, ('3p6 4s1 4p1 1p', '3p6 4s2 1s')),
              Line(calcium, 0, ('3p6 4s1 4d1 3d', '3p6 4s1 4p1 3p')),
              Line(calcium, 1, ('3p6 4d1 2d', '3p6 4p1 2p')),
              Line(helium, 0, ('1s1 4d1 3d7.0', '1s1 2p1 3p4.0')),
              Line(helium, 0, ('1s1 4s1 3s1.0', '1s1 2p1 3p4.0')),
              Line(helium, 0, ('1s1 3d1 3d7.0', '1s1 2p1 3p4.0')),
              Line(helium, 0, ('1s1 3d1 1d2.0', '1s1 2p1 1p1.0')),
              Line(helium, 0, ('1s1 3s1 3s1.0', '1s1 2p1 3p4.0')),
              Line(helium, 0, ('1s1 3s1 1s0.0', '1s1 2p1 1p1.0')),
              Line(krypton, 0, ('4s2 4p5 2p0.5 5s1 2[0.5]', '4s2 4p6 1s')),
              Line(krypton, 0, ('4s2 4p5 2p1.5 5s1 2[1.5]', '4s2 4p6 1s')),
              Line(krypton, 0, ('4s2 4p5 21.5 5p1 2[0.5]', '4s2 4p5 2p1.5 5s1 2[1.5]')),
              Line(krypton, 0, ('4s2 4p5 21.5 5p1 2[1.5]', '4s2 4p5 2p1.5 5s1 2[1.5]')),
              Line(magnesium, 0, ('2p6 3d1 2d', '2p6 3p1 2p')),
              Line(magnesium, 0, ('2p6 3p1 2p', '2p6 3s1 2s')),
              Line(sodium, 0, ('2p6 4p1 2p', ' 2p6 3s 2s')),
              Line(sodium, 0, ('2p6 6s1 2s', ' 2p6 3p 2p')),
              Line(sodium, 0, ('2p6 3p1 2p', '2p6 3s 2s')),
              Line(neon, 0, ('2s2 2p5 2p0.5 3p 2[0.5]', '2s2 2p5 2p0.5 3s 1[0.5]')),
              Line(neon, 2, ('2s2 2p3 4s1 3p1 5p', '2s2 2p3 4s1 3s1 5s')),
              Line(neon, 2, ('2s2 2p3 2d1 3p1 3f', '2s2 2p3 2d1 3s1 3d')),
              Line(oxygen, 0, ('2s2 2p3 3p1 5p7.0', '2s2 2p3 3s1 5s2.0')),
              Line(silicon, 0, ('3s2 3p1 4s1 3p4.0', '3s2 3p2 3p4.0')),
              Line(silicon, 1, ('3s2 4p1 2p2.5', '3s2 4s1 2s0.5')),
              Line(silicon, 2, ('3s1 4p1 3p4.0', '3s1 4s1 3s1.0')),
              Line(silicon, 2, ('3s1 4p1 1p1.0', '3s1 4s1 1s0.0')),
              Line(silicon, 3, ('4p1 2p2.5', '4s1 2s0.5'))]


HDLIKE = [Line(hydrogen, 0, (j, i)) for i in range(1, 4) for j in range(i + 1, 21)]
HDLIKE += [Line(deuterium, 0, (j, i)) for i in range(1, 4) for j in range(i + 1, 21)]
HDLIKE += [Line(tritium, 0, (j, i)) for i in range(1, 4) for j in range(i + 1, 21)]
HDLIKE += [Line(helium, 1, (j, i)) for i in range(2, 5) for j in range(i + 1, 21)]
HDLIKE += [Line(helium, 1, (j, 5)) for j in range(8, 21)]
HDLIKE += [Line(helium, 1, (j, 6)) for j in range(12, 21)]
HDLIKE += [Line(carbon, 5, (5, 4)), Line(carbon, 5, (6, 5)), Line(carbon, 5, (7, 5)), Line(carbon, 5, (8, 5))]
HDLIKE += [Line(carbon, 5, (j, 6)) for j in range(7, 21)]
HDLIKE += [Line(carbon, 5, (j, i)) for i in range(7, 9) for j in range(i + 1, 21)]
HDLIKE += [Line(carbon, 5, (j, 9)) for j in range(11, 21)]
HDLIKE += [Line(carbon, 5, (j, 10)) for j in range(12, 21)]
HDLIKE += [Line(carbon, 5, (j, 11)) for j in range(14, 21)]
HDLIKE += [Line(neon, 9, (8, 7)), Line(neon, 9, (9, 7))]
HDLIKE += [Line(neon, 9, (j, 8)) for j in range(9, 13)]
HDLIKE += [Line(neon, 9, (j, 9)) for j in range(10, 18)]
HDLIKE += [Line(neon, 9, (j, i)) for i in range(10, 13) for j in range(i + 1, 21)]
HDLIKE += [Line(neon, 9, (j, 13)) for j in range(15, 21)]


B_FIELD_MAX = {line: None for line in MULTIPLETS + HDLIKE}
for isotope in (hydrogen, deuterium, tritium):
    for i in (1, 4):
        B_FIELD_MAX[Line(isotope, 0, (12, i))] = 2.41
        B_FIELD_MAX[Line(isotope, 0, (13, i))] = 1.75
        B_FIELD_MAX[Line(isotope, 0, (14, i))] = 1.30
        B_FIELD_MAX[Line(isotope, 0, (15, i))] = 0.988
        B_FIELD_MAX[Line(isotope, 0, (16, i))] = 0.763
        B_FIELD_MAX[Line(isotope, 0, (17, i))] = 0.599
        B_FIELD_MAX[Line(isotope, 0, (18, i))] = 0.476
        B_FIELD_MAX[Line(isotope, 0, (19, i))] = 0.384
        B_FIELD_MAX[Line(isotope, 0, (20, i))] = 0.312
for i in (2, 7):
    B_FIELD_MAX[Line(helium, 0, (17, i))] = 2.39
    B_FIELD_MAX[Line(helium, 0, (18, i))] = 1.91
    B_FIELD_MAX[Line(helium, 0, (19, i))] = 1.53
    B_FIELD_MAX[Line(helium, 0, (20, i))] = 1.25


ION_INDEX = {hydrogen: 0,
             deuterium: 1,
             tritium: 2,
             helium: 3,
             carbon: 4,
             neon: 5}


def print_adas603_supported_lines():
    print()
    print("The following multiplet lines are supported:")
    for i, line in enumerate(MULTIPLETS):
        print('{}:, {}, {} nm'.format(i + 1, line))
    print()
    print("The following hydrogen and hydrogen-like lines are supported:")
    for i, line in enumerate(HDLIKE):
        if not B_FIELD_MAX[line]:
            print('{}:, {}'.format(i + 1, line))
        else:
            print('{}:, {}, B_FIELD_MAX = {} T'.format(i + 1, line, B_FIELD_MAX[line]))


def run_adas603(line, b_field=None, adas_fort=None):
    r"""
    Runs ADAS603 routines (components603 or hdlikecomponents603) and returns the wavelengths and
    relative intensities of :math:`\pi`-polarised and :math:`\sigma`-polarised compenents of Zeeman
    multiplet for the specified magnetic field strengths.
    Note that it is not required to run the routines for different angles of observation, because
    this angle affects only the ratio between the pi- and sigma-polarized components, which can be
    calculated analytically.

    :param Line line: Spectral line for which the Zeeman structure is calculated.
                      Run cherab.adas.adas6xx.print_adas603_supported_lines() to see the complete
                      list of supported lines.
    :param b_field: The grid of magnetic field strength (list or ndarray). Defaults to
                    np.arange(0, bmax, 0.1), where bmax is B_FIELD_MAX[line] if B_FIELD_MAX is
                    specified for this line or 20 T, if B_FIELD_MAX is not specified.
    :param str adas_fort: Path to ADAS FORTRAN executables.
                          Default path is 'home/adas/bin64' for 64-bit systems or
                          'home/adas/bin' for 32-bit systems.
    :return: A tuple (b_field, wavelengths_pi, components_pi, wavelengths_sigma, components_sigma),
             where b_field is a sorted array of the specified magnetic field strengths,
             wavelengths_pi/sigma are 2D arrays of wavelengths of
             :math:`\pi`-/:math:`\sigma`-polarised components,
             components_pi/sigma are 2D arrays of relative ratios of
             :math:`\pi`-/:math:`\sigma`-polarised components.
    """

    if not b_field:
        bmax = B_FIELD_MAX[line] or 20.
        b_field = np.arange(0, bmax, 0.1)
    else:
        b_field = np.sort(b_field)
        if b_field[0] < 0:
            raise ValueError("Argument b_field must contain non-negative values.")
        if B_FIELD_MAX[line] is not None and b_field[-1] > B_FIELD_MAX[line]:
            raise ValueError("Maximum b_field value for {} is {} T.".format(line, B_FIELD_MAX[line]))

    if line in MULTIPLETS:
        executable = 'components603'
        comm_str_suffix = '{}'.format(MULTIPLETS.index(line))
    elif line in HDLIKE:
        executable = 'hdlikecomponents603'
        comm_str_suffix = '{}\n{}\n{}'.format(line.transition[1], line.transition[0], ION_INDEX[line.element])
    else:
        print_adas603_supported_lines()
        raise ValueError('{} is not supported.'.format(line))

    if adas_fort is None:
        try:
            adas_fort = os.environ['ADASFORT']
        except KeyError:
            if '64' in platform.architecture()[0].lower():
                adas_fort = 'home/adas/bin64'
            else:
                adas_fort = 'home/adas/bin'

    file_path = os.path.join(adas_fort, executable)

    if not os.path.isfile(file_path):
        raise IOError('File {} not found.'.format(file_path))

    wavelengths_pi = []
    wavelengths_sigma = []
    components_pi = []
    components_sigma = []

    for b in b_field:
        process = Popen([file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # the components are calculated for 90 deg angle between the magnetic field vector and the observation direction,
        # at this angle, the ratio between pi- and sigma-polarised components is 1/1.
        comm_str = '{}\n{}\n{}\n{}\n'.format(1, 90., b, comm_str_suffix)
        outs, errors = process.communicate(bytes(comm_str, 'utf-8'))

        if errors:
            raise IOError('Process {} is terminated with error: {}.'.format(file_path, errors.decode('utf-8')))

        wl_pi, comp_pi, wl_sigma, comp_sigma = _adas603_output_to_components(outs.decode('utf-8'))
        wavelengths_pi.append(wl_pi)
        wavelengths_sigma.append(wl_sigma)
        components_pi.append(comp_pi)
        components_sigma.append(comp_sigma)

    return b_field, np.array(wavelengths_pi), np.array(components_pi), np.array(wavelengths_sigma), np.array(components_sigma)


def _adas603_output_to_components(outs):
    lines = outs.splitlines()
    wavelengths_pi = []
    wavelengths_sigma = []
    components_pi = []
    components_sigma = []
    for line in lines:
        if '#' in line:
            columns = line.split('#')
            intensity = float(columns[-1])
            wavelength = 0.1 * float(columns[-2])
            polarisation = int(columns[-3].split('/')[0])
            if polarisation:
                wavelengths_sigma.append(wavelength)
                components_sigma.append(intensity)
            else:
                wavelengths_pi.append(wavelength)
                components_pi.append(intensity)

    wavelengths_pi = np.array(wavelengths_pi)
    wavelengths_sigma = np.array(wavelengths_sigma)
    components_pi = np.array(components_pi)
    components_sigma = np.array(components_sigma)

    # renormalising
    components_pi /= components_pi.sum()
    components_sigma /= components_sigma.sum()

    return wavelengths_pi, components_pi, wavelengths_sigma, components_sigma
