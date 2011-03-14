import eventlet
import git
import openquake
import openquake.job
import os
import re
import time

from django import db
from django.core import exceptions

from modellers_toolkit import logs
from modellers_toolkit import scheduler
from modellers_toolkit import settings
from modellers_toolkit import utils


GIT_URL_RE = re.compile("^.*\.git$")
STATUSES = (
    ('complete', 'Complete'),
    ('new', 'New'),
    ('running', 'Running'),
)


def validate_git_url(url):
    # stupid, use gitpython
    if not GIT_URL_RE.match(url):
        raise exceptions.ValidationError("Must be the URL of a git repo.")


def handle_job(gt, *args, **kwargs):
    return gt.wait()

class Job(db.models.Model):
    """ An instance of an openquake Job. """

    class Meta:
        app_label = "openquake"


    created_at = db.models.DateTimeField(auto_now_add=True)
    updated_at = db.models.DateTimeField(auto_now=True)
    status = db.models.CharField(max_length=10, 
                                 choices=STATUSES,
                                 editable=False,
                                 default='new')
    name = db.models.CharField(max_length=40, unique=True)
    job_hash = db.models.CharField(max_length=40, 
                                   editable=False)
    repo = db.models.URLField(validators=[validate_git_url,], 
                              verify_exists=False,
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
        # download the repo.
        self.__clone_repo()

        # actually save.
        super(Job, self).save()

        # Then spawn a job.
        if self.status == 'new':
            self.job = scheduler.schedule(self.__spawn_job)

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
        eventlet.sleep(0)
        config_file = os.path.join(self.repo_dir, 'config.gem')
        job = openquake.job.Job.from_file(config_file)
        self.job_hash = job.job_id
        self.status = 'running'
        print self.status
        print self.job_hash
        self.save()
        job.launch()
