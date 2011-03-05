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
Base Controller class.
"""

import json
import webob.dec
import webob.exc


def _get_serializer(serialize_format):
    """ Return a serializer for the requested format """
    serializers = {
            "json": json.dumps
            }
    return serializers[serialize_format]


class Controller(object):
    """
    This a base controller class.
    """

    @webob.dec.wsgify
    def __call__(self, request):
        try:
            routing_args = request.environ['routing_args']
            action = getattr(self, routing_args['action'])
            serialize_format = routing_args.get('format')

            result = action(request.environ['routing_args'])
            if isinstance(result, dict):
                if serialize_format:
                    return self._serialize(result, serialize_format)
                return self._serialize(result)
            else:
                return result
        except KeyError:
            raise webob.exc.HTTPServerError("Invalid Request")

    def _serialize(self, result, serialize_format="json"):
        return _get_serializer(serialize_format)(result)

    @classmethod
    def fully_qualified_name(cls):
        """
        Return the fully qualified name of the class. This is used for
        sub-classes of Controller so we can have a job.Controller and a
        hazard.Controller and be able to route to them without their
        stomping on each other in the route mapper.
        """
        return "%s.%s" % (cls.__module__, cls.__name__)
