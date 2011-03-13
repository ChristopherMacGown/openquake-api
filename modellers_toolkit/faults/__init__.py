"""
Django app for managing active faults and folds, as part of the Faulted Earth
Global Component.

.. todo:: Add filter by active faults
    http://stackoverflow.com/questions/2251851/django-admin-list-filter-attribute-from-userprofile
    http://code.djangoproject.com/ticket/5833
    http://djangosnippets.org/snippets/2260/

.. todo:: Add info layer of other sections to fault section map.
    http://code.djangoproject.com/ticket/11112
    https://groups.google.com/forum/#topic/django-users/S7E13Y7TUNU
    
.. todo:: Support lat/lon type-in for points
.. todo:: Show coordinates while editing
.. todo:: Show length of section while editing
.. todo:: Provide a summary map for each fault
.. todo:: [BUG] Save and Continue from Fault Section fails
.. todo:: [BUG] Missing Base Layers
.. todo:: [BUG] Missing info layers
.. todo:: [BUG] Crash when editing geom from FaultSection form

.. todo:: Create multiple observations from one map
.. todo:: Change accuracy to Compilation Scale, prepopulate from 2X of Zoom Level in JS and use selection box for bins
.. todo:: Use more collapsed sections, very carefully (e.g. better styling to highlight collapsed areas)
.. todo:: Take the word "angle" off everything

.. todo:: Change is_active and is_episodic to select box with "Non-episodic, episodic and active, episodic and quiescient, episodic and unknown"
.. todo:: Support WMS for base layers (photo source)
.. todo:: All compulsory fields need a matching fitness for use field
.. todo:: Top-level fitness for use should be computed
.. todo:: Rename data completeness to Fitness for Use
.. todo:: Provide tooltips and help text for all fields, using data dictionary content from O&T

.. todo:: Support multi-value fields, with optional preferred value, and optional use of select control for bin ranges
.. todo:: Change labels on fieldsets to geological terms (e.g. provenance and geometry are both wrong.)

.. todo:: Rebuild recurrence, event and displacement relationships (using 'selected' boolean fields to indicate relationship preference)

.. todo:: Add names to sections
.. todo:: Add filter by country, using country bounding polygons
.. todo:: Sections have traces, which have expression, method and compilation scale attached directly. (Moved from Section)

.. todo:: Support missing slash on /admin url
.. todo:: Use thicker lines for better selectability
.. todo:: Normalize CSS on databrowser, make it easier to get back to admin screens


Further notes:

  https://tiger.my/demos/wheel/
  http://www.rkexcelamerica.com/dojo/1.3/release/docs/dojox/widget/AnalogGauge.html

Watch out for migration of geometry column, which breaks it!


"""

# The below code defines classmaker() - you should put this in a separate
# module and import it above your form definitions.
# From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/204197

import inspect, types, __builtin__

############## preliminary: two utility functions #####################

def skip_redundant(iterable, skipset=None):
    "Redundant items are repeated items or items in the original skipset."
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item


def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

##################################################################
## now the core of the module: two mutually recursive functions ##
##################################################################

memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
      return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:         # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1: # another trivial case
       meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases: 
        raise TypeError("Incompatible root metatypes", needed_metas)
    else: # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class