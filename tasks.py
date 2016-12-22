import json
import os
import invoke
from invoke import run, task, env
from invoke.util import cd, contextmanager
from dotenv import load_dotenv
from os import environ as env


@task
def build(ctx, cmd: str = '--help', dry_run: bool = False, capture: bool = False):
    """ Wrapper for docker-machine

    :param cmd: The docker-machine command to execute, see --help for details
    :param dry_run: If True, does not execute command, only print it
    :param capture: Passed on to local
    :return:
    """
    run('python setup.py bdist_wheel')
    run('docker-compose build superset')

