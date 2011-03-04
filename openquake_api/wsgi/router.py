#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright © 2011, GEM Foundation.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import webob.exc

import openquake_api.mapper
import openquake_api.wsgi.middleware


def dispatch_controller(controller, request):
    """
    Given a controller name, load the wsgi APP for that name and dispatch the
    request to that wsgi app.
    """
    print controller
    print request


class Router(openquake_api.wsgi.middleware.Middleware):
    """
    Route the incoming request to the appropriate App based on its path.
    """
    
    def __init__(self, app, mapper=openquake_api.mapper.Mapper):
        super(Router, self).__init__(app)
        self.mapper = mapper


    def _process_request(self, request):
        """
        """

        route = self.mapper.match(request.path)
        if not route:
            raise webob.exc.HTTPNotFound()

        return dispatch_controller(route['controller'], request)
