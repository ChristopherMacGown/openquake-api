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

import git
import os
import re


from django.core import exceptions
from lxml import etree
from StringIO import StringIO

GIT_URL_RE = re.compile("^.*\.git$")
STATUSES = (
    ("error", "Error"),
    ("complete", "Complete"),
    ("new", "New"),
    ("running", "Running"),
)

MODEL_TYPES = (
    ("vuln", "Vulnerability Model"),
    ("source", "Source Model"),
)


def validate_git_url(url):
    """
    Uses GitPython to validate that the repo is a git repository
    """
    try:
        repo = git.cmd.Git()
        repo.ls_remote(url)
    except git.exc.GitCommandError, e:
        raise exceptions.ValidationError("URL should be a git repository.")


def validate_model_type(model_type):
    if not model_type in [k for k, v in MODEL_TYPES] or model_type == "vuln":
        raise exceptions.ValidationError("Not yet implemented")


def validate_nrml(xml):
    """
    Currently uses lxml to verify that the passed string is valid xml. It should
    instead use whatever validation OpenQuake itself provides.
    """

    schema = etree.XMLSchema(file=os.path.join(os.path.dirname(__file__),
                                               '../../schema/nrml.xsd'))
    parser = etree.parse(StringIO(str(xml)))
    if not schema.validate(parser):
        raise exceptions.ValidationError("Invalid NRML document.")
