from piston import handler
from modellers_toolkit.openquake_mt import models


class JobHandler(handler.BaseHandler):
    model = models.Job


class ModelHandler(handler.BaseHandler):
    model = models.Model
