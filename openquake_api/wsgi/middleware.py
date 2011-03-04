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


import webob.dec


class Middleware(object):
    """
    A generic WSGI Middleware Class.
    """

    def __init__(self, application):
        self.application = application

    def _process_request(self, req):
        """
        Classes that inherit from this Middleware class will override this 
        method to provide their functionality.
        """
        pass

    def _process_response(self, res):
        """
        Classes that inherit from this Middleware class will override this
        method if they wish to render their responses differently from how the
        base application chooses to.
        """
        return res

    @webob.dec.wsgify
    def __call__(self, req):
        """
        Classes that inherit from this Middleware class do not need to override
        this method. Doing so will prevent middleware from acting like
        middleware.
        """
        result = self._process_request(req)
        if not result:
            result = req.get_response(self.application)
        return self._process_response(result)
