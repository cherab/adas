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

import cherab.openadas.repository.beam.cx as _beam_cx
from ..utility import repository_path_decorator


add_beam_cx_rate = repository_path_decorator(_beam_cx.add_beam_cx_rate)
update_beam_cx_rates = repository_path_decorator(_beam_cx.update_beam_cx_rates)
get_beam_cx_rates = repository_path_decorator(_beam_cx.get_beam_cx_rates)
