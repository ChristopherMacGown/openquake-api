import eventlet
import git
import openquake
import openquake.job
import os
import time
import shutil

from django import db

# ONLY TO FIX THE LACK OF MIXINS
# HACKHACKHACK
# TODO(chris): Get this out of here, put it in a good spot in openquake.
from openquake.hazard import job as hazjob
from openquake.hazard import opensha
from openquake.risk import job as riskjob
from openquake.risk.job import probabilistic
#
# END HACK
#

from modellers_toolkit import logs
from modellers_toolkit import scheduler
from modellers_toolkit import settings
from modellers_toolkit import utils
from modellers_toolkit.openquake_mt import validators


NO_SPAWN_STATUSES = ['error', 'running']

def handle_job(gt, *args, **kwargs):
    return gt.wait()


class Model(db.models.Model):
    class Meta:
        app_label = "openquake"

    name = db.models.CharField(max_length=255,
                               null=False,
                               unique=True)
    model_type = db.models.CharField(max_length=10,
                                     choices=validators.MODEL_TYPES,
                                     validators=[validators.validate_model_type,],
                                     editable=True)
    model_blob = db.models.TextField(verbose_name="NRML Model",
                                     validators=[validators.validate_nrml,],)
    created_at = db.models.DateTimeField(auto_now_add=True)
    updated_at = db.models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


    def save(self):
        super(Model, self).save() # Save the object to the db.
        
        # write the model to a file on disk.
        with open("/tmp/%s-model" % model_type, "w") as model:
            model.write(model_blob)

        # Then update the RuiUI Job.



class Job(db.models.Model):
    """ An instance of an openquake Job. """

    class Meta:
        app_label = "openquake"


    created_at = db.models.DateTimeField(auto_now_add=True)
    updated_at = db.models.DateTimeField(auto_now=True)
    status = db.models.CharField(max_length=10, 
                                 choices=validators.STATUSES,
                                 editable=False,
                                 default='new')
    name = db.models.CharField(max_length=40, unique=True)
    job_hash = db.models.CharField(max_length=40, 
                                   editable=False)
    repo = db.models.CharField(max_length=255,
                               validators=[validators.validate_git_url,], 
                               verbose_name="git repository")

    def __unicode__(self):
        return self.name

    @property
    def repo_name(self):
        return unicode.join(u'', self.name.split())

    @property
    def repo_dir(self):
        return utils.repo_dir(self.repo_name)

    def save(self):
        # actually save.
        super(Job, self).save()

        # Spawn IT!
        if not self.status in NO_SPAWN_STATUSES:
            # download the repo.
            self.__clone_repo()
            self.__spawn_job()


    def delete(self):
        try:
            super(Job, self).delete()
        finally:
            shutil.rmtree(self.repo_dir)

    def __clone_repo(self):
        try:
            repo = git.Repo.clone_from(self.repo, self.repo_dir)
        except git.GitCommandError:
            # Already cloned
            repo = git.Repo(self.repo_dir)

        # Grab the latest configs.
        for remote in repo.remotes:
            remote.pull()

    def __spawn_job(self):
        # TODO(chris): Move me into the daemonized job runner.
        config_file = os.path.join(self.repo_dir, 'config.gem')
        job = openquake.job.Job.from_file(config_file)
        self.job_hash = job.job_id
        self.status = 'running'
        self.save()
        try:
            return job.launch()
        except Exception, e:
            self.status = "error"
            self.save()
            return False

