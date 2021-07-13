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

from cherab.core.math.interpolators import Interpolate1DLinear
from cherab.core import AtomicData
from cherab.core.atomic.elements import Isotope
from cherab.core.atomic import ZeemanStructure
from cherab.adas.repository import DEFAULT_REPOSITORY_PATH
from cherab.adas.adas4xx.adas405 import run_adas405
from cherab.adas.adas6xx.adas603 import run_adas603

from cherab.adas.rates import *
from cherab.adas import repository


class ADAS(AtomicData):
    """

    """

    def __init__(self, data_path=None, permit_extrapolation=False, missing_rates_return_null=False):

        super().__init__()
        self._data_path = data_path or DEFAULT_REPOSITORY_PATH

        # if true informs interpolation objects to allow extrapolation beyond the limits of the tabulated data
        self._permit_extrapolation = permit_extrapolation

        # if true, allows Null rate objects to be returned when the requested atomic data is missing
        self._missing_rates_return_null = missing_rates_return_null

    @property
    def data_path(self):
        return self._data_path

    def wavelength(self, ion, charge, transition):
        """
        :param ion: Element object defining the ion type.
        :param charge: Charge state of the ion.
        :param transition: Tuple containing (initial level, final level)
        :return: Wavelength in nanometers.
        """

        if isinstance(ion, Isotope):
            ion = ion.element
        return repository.get_wavelength(ion, charge, transition)

    def ionisation_rate(self, ion, charge):

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            data = repository.get_ionisation_rate(ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullIonisationRate()
            raise

        return IonisationRate(data, extrapolate=self._permit_extrapolation)

    def recombination_rate(self, ion, charge):

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            data = repository.get_recombination_rate(ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullRecombinationRate()
            raise

        return RecombinationRate(data, extrapolate=self._permit_extrapolation)

    def thermal_cx_rate(self, donor_element, donor_charge, receiver_element, receiver_charge):

        if isinstance(donor_element, Isotope):
            donor_element = donor_element.element

        if isinstance(receiver_element, Isotope):
            receiver_element = receiver_element.element

        try:
            data = repository.get_thermal_cx_rate(donor_element, donor_charge,
                                                  receiver_element, receiver_charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullThermalCXRate()
            raise

        return ThermalCXRate(data, extrapolate=self._permit_extrapolation)

    def beam_cx_pec(self, donor_ion, receiver_ion, receiver_charge, transition):
        """

        :param donor_ion:
        :param receiver_ion:
        :param receiver_charge:
        :param transition:
        :return:
        """

        # extract element from isotope
        if isinstance(donor_ion, Isotope):
            donor_ion = donor_ion.element

        if isinstance(receiver_ion, Isotope):
            receiver_ion = receiver_ion.element

        try:
            # read data
            wavelength = repository.get_wavelength(receiver_ion, receiver_charge - 1, transition)
            data = repository.get_beam_cx_rates(donor_ion, receiver_ion, receiver_charge, transition)

        except RuntimeError:
            if self._missing_rates_return_null:
                return [NullBeamCXPEC()]
            raise

        # load and interpolate the relevant transition data from each file
        rates = []
        for donor_metastable, rate_data in data:
            rates.append(BeamCXPEC(donor_metastable, wavelength, rate_data, extrapolate=self._permit_extrapolation))
        return rates

    def beam_stopping_rate(self, beam_ion, plasma_ion, charge):
        """

        :param beam_ion:
        :param plasma_ion:
        :param charge:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        try:
            # locate data file
            data = repository.get_beam_stopping_rate(beam_ion, plasma_ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullBeamStoppingRate()
            raise

        # load and interpolate data
        return BeamStoppingRate(data, extrapolate=self._permit_extrapolation)

    def beam_population_rate(self, beam_ion, metastable, plasma_ion, charge):
        """

        :param beam_ion:
        :param metastable:
        :param plasma_ion:
        :param charge:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        try:
            # locate data file
            data = repository.get_beam_population_rate(beam_ion, metastable, plasma_ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullBeamPopulationRate()
            raise

        # load and interpolate data
        return BeamPopulationRate(data, extrapolate=self._permit_extrapolation)

    def beam_emission_pec(self, beam_ion, plasma_ion, charge, transition):
        """

        :param beam_ion:
        :param plasma_ion:
        :param charge:
        :param transition:
        :return:
        """

        # extract element from isotope
        if isinstance(beam_ion, Isotope):
            beam_ion = beam_ion.element

        if isinstance(plasma_ion, Isotope):
            plasma_ion = plasma_ion.element

        try:
            # locate data file
            data = repository.get_beam_emission_rate(beam_ion, plasma_ion, charge, transition)
            wavelength = repository.get_wavelength(beam_ion, 0, transition)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullBeamEmissionPEC()
            raise

        # load and interpolate data
        return BeamEmissionPEC(data, wavelength, extrapolate=self._permit_extrapolation)

    def impact_excitation_pec(self, ion, charge, transition):
        """

        :param ion:
        :param charge:
        :param transition:
        :return:
        """

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            wavelength = repository.get_wavelength(ion, charge, transition)
            data = repository.get_pec_excitation_rate(ion, charge, transition)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullImpactExcitationPEC()
            raise

        return ImpactExcitationPEC(wavelength, data, extrapolate=self._permit_extrapolation)

    def recombination_pec(self, ion, charge, transition):
        """

        :param ion:
        :param charge:
        :param transition:
        :return:
        """

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            wavelength = repository.get_wavelength(ion, charge, transition)
            data = repository.get_pec_recombination_rate(ion, charge, transition)

        except (FileNotFoundError, KeyError):
            if self._missing_rates_return_null:
                return NullRecombinationPEC()
            raise

        return RecombinationPEC(wavelength, data, extrapolate=self._permit_extrapolation)

    def line_radiated_power_rate(self, ion, charge):

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            data = repository.get_line_radiated_power_rate(ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullLineRadiationPower(ion, charge)
            raise

        return LineRadiationPower(ion, charge, data, extrapolate=self._permit_extrapolation)

    def continuum_radiated_power_rate(self, ion, charge):

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            data = repository.get_continuum_radiated_power_rate(ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullContinuumPower(ion, charge)
            raise

        return ContinuumPower(ion, charge, data, extrapolate=self._permit_extrapolation)

    def cx_radiated_power_rate(self, ion, charge):

        if isinstance(ion, Isotope):
            ion = ion.element

        try:
            data = repository.get_cx_radiated_power_rate(ion, charge)

        except RuntimeError:
            if self._missing_rates_return_null:
                return NullCXRadiationPower(ion, charge)
            raise

        return CXRadiationPower(ion, charge, data, extrapolate=self._permit_extrapolation)

    def total_radiated_power(self, ion):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        electron_densities, electron_temperatures, _, total_power_array, _, _, _, _ = run_adas405(elem=ion.symbol.lower())

        return TotalRadiatedPower(ion, electron_densities, electron_temperatures, total_power_array,
                                  extrapolate=self._permit_extrapolation)

    def fractional_abundance(self, ion, ionisation):

        # extract element from isotope
        if isinstance(ion, Isotope):
            ion = ion.element

        electron_densities, electron_temperatures, fraction, _, _, _, _, _ = run_adas405(elem=ion.symbol.lower())
        name = ion.symbol + '_' + str(ionisation)

        return FractionalAbundance(ion, ionisation, electron_densities, electron_temperatures, fraction[:, :, ionisation], name=name)

    def zeeman_structure(self, line, b_field=None):
        r"""
        Provides wavelengths and ratios of
        :math:`\pi`-/:math:`\sigma`-polarised Zeeman components of the specified spectral line
        for any given value of magnetic field strength.

        :param Line line: Spectral line object.
                          Run cherab.adas.adas6xx.print_adas603_supported_lines() to see
                          the complete list of supported lines.
        :param b_field: The grid of magnetic field strength (list or ndarray)
                        to interpolate from. Defaults to np.arange(0, bmax, 0.1),
                        where bmax is B_FIELD_MAX[line] if B_FIELD_MAX is
                        specified for this line, or 20.0 T if B_FIELD_MAX is not specified.
        :return:
        """

        b_field, pi_comp, sigma_plus_comp, sigma_minus_comp = run_adas603(line, b_field)

        pi_components = []
        sigma_plus_components = []
        sigma_minus_components = []

        for component in pi_comp:
            wvl = Interpolate1DLinear(b_field, component[0])
            ratio = Interpolate1DLinear(b_field, component[1])
            pi_components.append((wvl, ratio))

        for component in sigma_plus_comp:
            wvl = Interpolate1DLinear(b_field, component[0])
            ratio = Interpolate1DLinear(b_field, component[1])
            sigma_plus_components.append((wvl, ratio))

        for component in sigma_minus_comp:
            wvl = Interpolate1DLinear(b_field, component[0])
            ratio = Interpolate1DLinear(b_field, component[1])
            sigma_minus_components.append((wvl, ratio))

        return ZeemanStructure(pi_components, sigma_plus_components, sigma_minus_components)
