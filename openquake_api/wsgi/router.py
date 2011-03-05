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

"""
    The Router middleware takes an incoming request and dispatches it to the
    appropriate controller based on its path.
"""

import webob.exc

from openquake_api import mapper
from openquake_api.wsgi import controller
from openquake_api.wsgi import middleware


def dispatch_controller(cname, request):
    """
    Given a controller name, load the wsgi APP for that name and dispatch the
    request to that wsgi app.
    """

    try:
        cont = [cls() for cls
                      in controller.Controller.__subclasses__()
                      if cls.fully_qualified_name() == cname][0]
        return cont(request)
    except IndexError:
        raise webob.exc.HTTPServerError("Could not find class for %s" % cname)


class Router(middleware.Middleware):
    """
    Route the incoming request to the appropriate App based on its path.
    """

    def __init__(self, app, route_map=mapper.Mapper):
        super(Router, self).__init__(app)
        self.route_map = route_map

    def _process_request(self, request):
        """
        """

        route = self.route_map.match(request.path)
        if not route:
            raise webob.exc.HTTPNotFound()

        return dispatch_controller(route['controller'], request)
