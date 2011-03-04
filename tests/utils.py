#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# 
# Portions Copyright © 2011, Christopher MacGown
# Modifications Copyright © 2011, GEM Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
import unittest

def testdata(filename):
    """ Returns the full tests/data path of the passed filename """
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    if not os.path.exists(path):
        raise IOError("%s does not exist in the data directory." % path)
    return path

def load(filename, decode=True):
    """
    Opens the passed file, if decode is True, json decodes and returns the
    deserialized result. Otherwise returns the string.
    """

    with open(filename) as fp:
        res = fp.read()
        if decode:
            res = json.loads(res)
        return res

class WasCalled(object):
    """
    Wrapper for a callable that is "True" if the callable was called, "False"
    otherwise.
    """

    def __init__(self, method):
        self.was_called = False
        self.method = method
    
    def __call__(self, *args, **kwargs):
        try:
            self.method(*args, **kwargs)
        finally:
            self.was_called = True

    def __nonzero__(self):
        return self.was_called

class TestHelper(unittest.TestCase):
    """
    Test helper class that adds a couple useful methods to unittest.TestCase:
        assertCalled(…): asserts that methods are called in a callable.
        assertNothingRaised(…): asserts that no exception is raised in a 
                                callable.
    """

    def assertCalled(self, caller, expected_methods, *args, **kwargs):
        """
        Asserts that expected_methods are called in a callable. To use you'll
        need to wrap each expected method using WasCalled(method):
            def test_some_test(self):
                log.info = WasCalled(log.info)
                self.assertCalled(some_callable, expected_methods=(log.info,))
        """
        if not isinstance(expected_methods, tuple):
            raise AttributeError("expected_methods must be a tuple!")

        caller(*args, **kwargs)
        for method in expected_methods:
            self.assertTrue(method)

    def assertNothingRaised(self, caller, *args, **kwargs):
        """
        Asserts that no exception is raised in the caller.
        """
        raised=None
        try:
            caller(*args, **kwargs)
        except Exception:
            raised=True

        self.assertFalse(raised)
