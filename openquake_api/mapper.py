"""
This module contains a route Mapper which maps a path to a controller.
"""

import routes


Mapper = routes.Mapper()  # pylint: disable=C0103
Mapper.connect('jobs', '/jobs', controller='job', action='list')
Mapper.connect('/jobs/:job_name/', controller='job', action='view',
               requirements={"job_name": "\w{1,32}"})
Mapper.connect('/jobs/:job_name/results', controller='job', action='view',
               requirements={"job_name": "\w{1,32}"})
Mapper.connect('/jobs/:job_name/update', controller='job', action='update',
               requirements={"job_name": "\w{1,32}"})
Mapper.connect('/jobs/:job_name/:revision', controller='job', action='view',
               requirements={"job_name": "\w{1,32}",
                             "revision": "master|[a-fA-F0-9]{1,40}"})
