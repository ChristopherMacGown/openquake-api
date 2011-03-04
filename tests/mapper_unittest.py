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


from openquake_api import mapper

from tests import utils


class MapperTestCase(utils.TestHelper):
    def setUp(self):
        pass

    def test_routes_are_properly_set_up(self):
        self.assertTrue(mapper.Mapper.match('/jobs'))
        self.assertTrue(mapper.Mapper.match('/jobs/fake_job/'))
        self.assertTrue(mapper.Mapper.match('/jobs/fake_job/results'))
        self.assertTrue(mapper.Mapper.match('/jobs/fake_job/update'))
        self.assertTrue(mapper.Mapper.match('/jobs/fake_job/master'))
        self.assertTrue(mapper.Mapper.match('/jobs/fake_job/cfa9b9f2b15e129'))
    
    def test_non_existent_routes_return_none(self):
        self.assertFalse(mapper.Mapper.match('/jerbs'))
        self.assertFalse(mapper.Mapper.match('/jobs/fake_job/foook'))
        self.assertFalse(mapper.Mapper.match('/jobs//'))
        self.assertFalse(mapper.Mapper.match('/jobs/fake_job//'))
        self.assertFalse(mapper.Mapper.match('/jobs/fake_job/'
            "00000000000000000000000000000000000000000000000000"))
