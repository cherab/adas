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

import cherab.openadas.repository.beam.emission as _beam_emission
from ..utility import repository_path_decorator


add_beam_emission_rate = repository_path_decorator(_beam_emission.add_beam_emission_rate)
update_beam_emission_rates = repository_path_decorator(_beam_emission.update_beam_emission_rates)
get_beam_emission_rate = repository_path_decorator(_beam_emission.get_beam_emission_rate)
