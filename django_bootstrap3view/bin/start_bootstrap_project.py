#!/usr/bin/env python

import sys
from django_bootstrap3view_app.management.commands.create_bootstrap_project import Command

Command().do_run(*sys.argv[1:])
