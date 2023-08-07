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


import os

from cherab.atomic import repository
from cherab.adas.parse import *
from cherab.adas.adas6xx.adas603 import SUPPORTED_LINES as ADAS603_SUPPORTED_LINES
from cherab.adas.adas6xx import run_adas603
from cherab.adas.adas4xx import run_adas405
from cherab.core.utility import RecursiveDict, PerCm3ToPerM3, Cm3ToM3


def install_files(configuration, repository_path=None, adas_home=None):
    """
    Wrapper function that installs rates of atomic processes defined
    in ADAS files to the repository.
    """

    for adf in configuration:
        if adf.lower() == 'adf11scd':
            for args in configuration[adf]:
                install_adf11scd(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf11acd':
            for args in configuration[adf]:
                install_adf11acd(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf11ccd':
            for args in configuration[adf]:
                install_adf11ccd(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf11plt':
            for args in configuration[adf]:
                install_adf11plt(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf11prb':
            for args in configuration[adf]:
                install_adf11prb(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf11prc':
            for args in configuration[adf]:
                install_adf11prc(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf12':
            for args in configuration[adf]:
                install_adf12(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf15':
            for args in configuration[adf]:
                install_adf15(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf21':
            for args in configuration[adf]:
                install_adf21(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf22bmp':
            for args in configuration[adf]:
                install_adf22bmp(*args, repository_path=repository_path, adas_home=adas_home)
        if adf.lower() == 'adf22bme':
            for args in configuration[adf]:
                install_adf22bme(*args, repository_path=repository_path, adas_home=adas_home)


# todo: move print calls to logging

def install_adf11scd(element, file_path, repository_path=None, adas_home=None):
    """
    Adds the ionisation rate defined in an ADF11 file to the repository.

    :param element: The element described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(element, path)

    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "scd")  # convert from adas to cherab notation

    repository.update_ionisation_rates(rate_cherab, repository_path)


def install_adf11acd(element, file_path, repository_path=None, adas_home=None):
    """
    Adds the recombination rate defined in an ADF11 file to the repository.

    :param element: The element described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(element, path)

    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "acd")  # convert from adas to cherab notation

    repository.update_recombination_rates(rate_cherab, repository_path)


def install_adf11ccd(donor_element, donor_charge, receiver_element, file_path,
                     repository_path=None, adas_home=None):
    """
    Adds the thermal charge exchange rate defined in an ADF11 file to the repository.

    :param donor_element: Element donating the electron, for the case of ADF11 files it is
      neutral hydrogen.
    :param donor_charge: Charge of the donor atom/ion.
    :param receiver_element: Element receiving the electron.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(receiver_element, path)
    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "ccd")  # convert from adas to cherab notation

    # reshape rate dictionary to match cherab convention
    rate_cherab_ccd = RecursiveDict()
    rate_cherab_ccd[donor_element][donor_charge] = rate_cherab

    repository.update_thermal_cx_rates(rate_cherab_ccd, repository_path)


def install_adf11plt(element, file_path, repository_path=None, adas_home=None):
    """
    Adds the line radiated power rates defined in an ADF11 file to the repository.

    :param element: The element described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(element, path)

    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "plt")  # convert from adas to cherab notation

    repository.update_line_power_rates(rate_cherab, repository_path)


def install_adf11prb(element, file_path, repository_path=None, adas_home=None):
    """
    Adds the continuum radiated power rates defined in an ADF11 file to the repository.

    :param element: The element described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(element, path)

    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "prb")  # convert from adas to cherab notation

    repository.update_continuum_power_rates(rate_cherab, repository_path)


def install_adf11prc(element, file_path, repository_path=None, adas_home=None):
    """
    Adds the CX radiated power rates defined in an ADF11 file to the repository.

    :param element: The element described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rate_adas = parse_adf11(element, path)

    rate_cherab = _notation_adf11_adas2cherab(rate_adas, "prc")  # convert from adas to cherab notation

    repository.update_cx_power_rates(rate_cherab, repository_path)


def install_adf12(donor_ion, donor_metastable, receiver_ion, receiver_charge, file_path, repository_path=None, adas_home=None):
    """
    Adds the rates in the ADF12 file to the repository.

    :param donor_ion: The donor ion element described by the rate file.
    :param donor_metastable: The donor ion metastable level.
    :param receiver_ion: The receiver ion element described by the rate file.
    :param receiver_charge: The receiver ion ionisation level described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rates = parse_adf12(donor_ion, donor_metastable, receiver_ion, receiver_charge, path)
    repository.update_beam_cx_rates(rates, repository_path)


def install_adf15(element, ionisation, file_path, repository_path=None, adas_home=None, header_format=None):
    """
    Adds the rates in the ADF15 file to the repository.

    :param element: The element described by the rate file.
    :param ionisation: The ionisation level described by the rate file.
    :param file_path: Path relative to ADAS home.
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # decode file and write out rates
    rates, wavelengths = parse_adf15(element, ionisation, path, header_format=header_format)
    repository.update_pec_rates(rates, repository_path)
    repository.update_wavelengths(wavelengths, repository_path)


def install_adf21(beam_species, target_ion, target_charge, file_path, repository_path=None, adas_home=None):
    """
    Adds the beam stopping rate defined in an ADF21 file to the repository.

    :param beam_species: Beam neutral atom (Element/Isotope).
    :param target_ion: Target species (Element/Isotope).
    :param target_charge: Charge of the target species.
    :param file_path: Path relative to ADAS root.
    :param download: Attempt to download file if not present (Default=True).
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # # decode file and write out rates
    rate = parse_adf21(beam_species, target_ion, target_charge, path)
    repository.update_beam_stopping_rates(rate, repository_path)


def install_adf22bmp(beam_species, beam_metastable, target_ion, target_charge, file_path, repository_path=None, adas_home=None):
    """
    Adds the beam population rate defined in an ADF22 BMP file to the repository.

    :param beam_species: Beam neutral atom (Element/Isotope).
    :param beam_metastable: Metastable level of beam neutral atom.
    :param target_ion: Target species (Element/Isotope).
    :param target_charge: Charge of the target species.
    :param file_path: Path relative to ADAS root.
    :param download: Attempt to download file if not present (Default=True).
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # # decode file and write out rates
    rate = parse_adf22bmp(beam_species, beam_metastable, target_ion, target_charge, path)
    repository.update_beam_population_rates(rate, repository_path)


def install_adf22bme(beam_species, target_ion, target_charge, transition, file_path, repository_path=None, adas_home=None):
    """
    Adds the beam emission rate defined in an ADF22 BME file to the repository.

    :param beam_species: Beam neutral atom (Element/Isotope).
    :param target_ion: Target species (Element/Isotope).
    :param target_charge: Charge of the target species.
    :param transition: Tuple containing (initial level, final level).
    :param file_path: Path relative to ADAS root.
    :param download: Attempt to download file if not present (Default=True).
    :param repository_path: Path to the repository in which to install the rates (optional).
    :param adas_home: Path to ADAS home directory (optional).
    """

    print('Installing {}...'.format(file_path))
    path = _locate_adas_file(file_path, adas_home)
    if not path:
        raise ValueError('Could not locate the specified ADAS file.')

    # # decode file and write out rates
    rate = parse_adf22bme(beam_species, target_ion, target_charge, transition, path)
    repository.update_beam_emission_rates(rate, repository_path)


def install_zeeman_structures(lines=None, adas_fort=None, repository_path=None):
    """
    Runs ADAS603 and adds Zeeman multiplet structures for given spectral lines to the repository.

    :param lines: Spectral lines for which the Zeeman structure is calculated.
        Run cherab.adas.adas6xx.print_adas603_supported_lines() to see the complete list
        of supported lines.
    :param adas_fort: Path to ADAS FORTRAN executables.
        Default path is 'home/adas/bin64' for 64-bit systems or 'home/adas/bin' for 32-bit systems.
    :param repository_path: Path to the repository in which to install the rates (optional).
    """

    if lines is None:
        lines = ADAS603_SUPPORTED_LINES
    else:
        unsupported_lines = set(lines).difference(ADAS603_SUPPORTED_LINES)
        if len(unsupported_lines):
            unsupported_lines_str = '\n'.join([str(line) for line in unsupported_lines])
            raise ValueError("The followoing spectral lines are not supported:\n{}".format(unsupported_lines_str))

    zeeman_structures = RecursiveDict()
    for line in lines:
        data = run_adas603(line, adas_fort=adas_fort)
        zeeman_structures[line.element][line.charge][line.transition] = data

    repository.update_zeeman_structures(zeeman_structures, repository_path)


def install_total_power_rate(element, uid='adas', year=96, repository_path=None):
    """
    Runs ADAS405 and adds total radiated power rate for given species to the repository.

    :param element: Plasma species element.
    :param uid: Username of adf11 location. Defaults to 'adas' for central ADAS data.
    :param year: Year index of the adf11 data. Defaults to 96.
    """

    ne, te, _, total_power_rate, _, _, _, _ = run_adas405(uid=uid, year=year, elem=element.symbol.lower())
    data = {'ne': ne, 'te': te, 'rate': rate}

    repository.add_total_power_rate(element, data, repository_path=repository_path)


def install_fractional_abundances(element, uid='adas', year=96, repository_path=None):
    """
    Runs ADAS405 and adds fractional abundances for given species to the repository.

    :param element: Plasma species element.
    :param uid: Username of adf11 location. Defaults to 'adas' for central ADAS data.
    :param year: Year index of the adf11 data.
    """

    ne, te, fractionl_abundances, _, _, _, _, _ = run_adas405(uid=uid, year=year, elem=element.symbol.lower())
    data = {element: {}}

    for i in range(fractionl_abundances.shape[-1]):
        data[element][i] = {'ne': ne, 'te': te, 'fractional_abundance': fractionl_abundances[:, :, i]}

    repository.update_fractional_abundances(data, repository_path=repository_path)


def _locate_adas_file(file_path, adas_home=None):

    path = None

    if not adas_home:
        # trying to find adas home directory

        try:
            adas_home = os.environ["ADASHOME"]
        except KeyError:
            adas_home = "/home/adas"

        if not os.path.isdir(adas_home):
            raise IOError("Could not find the ADAS root directory.")

    # is file in adas path?
    target = os.path.join(adas_home, file_path)
    if os.path.isfile(target):
        path = target

    return path


def _notation_adf11_adas2cherab(rate_adas, filetype):
    """
    Converts adas unit, charge and numeric notation to cherab notation

    :param rate_adas: Nested dictionary of shape rate_adas[element][charge][te, ne, rates]
    :param filetype: string denoting adas adf11 file type to decide whether charge conversion is to be applied.
      Will be applied for file types: "scd", "ccd", "plt", "pls"
    :return: nested dictionary with cherab rates and units notation
    """

    # Charge correction will be applied if there is difference between adas and cherab charge notation
    if filetype in ["scd", "plt", "pls"]:
        charge_correction = int(-1)
    else:
        charge_correction = int(0)

    # adas units, charge and number notation to be changed to cherab notation
    rate_cherab = RecursiveDict()
    for i in rate_adas.keys():
        for j in rate_adas[i].keys():
            # convert from adas log10 in [cm**-3] notation to cherab [m**-3] electron density notation
            rate_cherab[i][j + charge_correction]["ne"] = PerCm3ToPerM3.to(10**rate_adas[i][j]["ne"])
            # convert from adas log10 to cherab electron temperature notation
            rate_cherab[i][j + charge_correction]["te"] = 10**rate_adas[i][j]["te"]
            rate_cherab[i][j + charge_correction]["rates"] = Cm3ToM3.to(10**rate_adas[i][j]["rates"])

    return rate_cherab
