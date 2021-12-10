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


import cherab.openadas.repository.radiated_power as _radiated_power
from .utility import repository_path_decorator


add_line_power_rate = repository_path_decorator(_radiated_power.add_line_power_rate)
update_line_power_rates = repository_path_decorator(_radiated_power.update_line_power_rates)
get_line_radiated_power_rate = repository_path_decorator(_radiated_power.get_line_radiated_power_rate)

add_continuum_power_rate = repository_path_decorator(_radiated_power.add_continuum_power_rate)
update_continuum_power_rates = repository_path_decorator(_radiated_power.update_continuum_power_rates)
get_continuum_radiated_power_rate = repository_path_decorator(_radiated_power.get_continuum_radiated_power_rate)

add_cx_power_rate = repository_path_decorator(_radiated_power.add_cx_power_rate)
update_cx_power_rates = repository_path_decorator(_radiated_power.update_cx_power_rates)
get_cx_radiated_power_rate = repository_path_decorator(_radiated_power.get_cx_radiated_power_rate)
