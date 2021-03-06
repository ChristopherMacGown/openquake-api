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

import json
import routes
import webob
import webob.dec
import webob.exc

from openquake_api.wsgi import controller
from openquake_api.wsgi import router

from tests import utils


class FakeController(controller.Controller):
    def index(self, req):
        return req


class RouterTestCase(utils.TestHelper):
    def setUp(self):
        self.fake_req = webob.Request.blank("/fake_request")

    def test_dispatch_route_dispatches_request_to_controller(self):
        self.fake_req.environ['routing_args'] = {
            'action': "index",
            'controller': "tests.router_unittest.FakeController"}
        self.assertEqual(
            json.dumps(self.fake_req.environ['routing_args']),
            router.dispatch_controller(self.fake_req))

    def test_dispatch_route_raises_if_no_such_controller_exists(self):
        self.fake_req.environ['routing_args'] = {
            'action': "index",
            'controller': "doesnt.exist"}
        self.assertRaises(webob.exc.HTTPServerError,
                          router.dispatch_controller,
                          self.fake_req)

    def test_router_properly_dispatches_on_receiving_a_mapped_path(self):
        router.dispatch_controller = utils.WasCalled(router.dispatch_controller)
        req = webob.Request.blank("/fake_route")
        mapper = routes.Mapper()
        mapper.connect('fake_route', '/fake_route', 
                       controller="tests.router_unittest.FakeController",
                       action="index")

        r = router.Router("fake_route", route_map=mapper)
        self.assertCalled(r._process_request, (router.dispatch_controller,),
                          req)

    def test_router_raises_404_on_receiving_unmapped_path(self):
        req = webob.Request.blank("/fake_route_doesn't_exist")

        mapper = routes.Mapper()
        mapper.connect('fake_route', '/fake_route', 
                       controller="tests.router_unittest.FakeController")

        r = router.Router("fake_app", route_map=mapper)
        self.assertRaises(webob.exc.HTTPNotFound,
                          r._process_request, req)
