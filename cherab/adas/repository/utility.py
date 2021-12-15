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

import os
from inspect import signature
from functools import wraps
from cherab.openadas.repository.utility import encode_transition, valid_charge


DEFAULT_REPOSITORY_PATH = os.path.expanduser('~/.cherab/adas/repository')


def repository_path_decorator(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) == len(signature(f).parameters):  # repository_path is passed in args
            if not args[-1]:  # repository_path is None
                kwargs['repository_path'] = DEFAULT_REPOSITORY_PATH
                return f(*args[:-1], **kwargs)

            return f(*args, **kwargs)  # repository_path is not None

        try:  # repository_path is passed in kwargs
            kwargs['repository_path'] = kwargs['repository_path'] or DEFAULT_REPOSITORY_PATH
        except KeyError:  # repository_path is not passed
            kwargs['repository_path'] = DEFAULT_REPOSITORY_PATH

        return f(*args, **kwargs)

    return wrapper
