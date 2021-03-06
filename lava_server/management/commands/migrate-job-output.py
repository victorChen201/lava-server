# Copyright (C) 2017 Linaro Limited
#
# Author: Remi Duraffort <remi.duraffort@linaro.org>
#
# This file is part of LAVA Dispatcher.
#
# LAVA Dispatcher is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# LAVA Dispatcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along
# with this program; if not, see <http://www.gnu.org/licenses>.

from django.conf import settings
from django.core.management.base import BaseCommand

from lava_scheduler_app.models import TestJob
from lava_scheduler_app.utils import mkdir

import os


class Command(BaseCommand):
    help = "Move job outputs into the new location"

    def handle(self, *_, **options):
        base_dir = "/var/lib/lava-server/default/media/job-output/"
        len_base_dir = len(base_dir)
        jobs = TestJob.objects.all().order_by("id")

        self.stdout.write("Browsing all jobs")
        for job in jobs:
            old_path = os.path.join(settings.MEDIA_ROOT, 'job-output', 'job-%s' % job.id)
            date_path = os.path.join(settings.MEDIA_ROOT, 'job-output',
                                     "%02d" % job.submit_time.year,
                                     "%02d" % job.submit_time.month,
                                     "%02d" % job.submit_time.day,
                                     str(job.id))
            if not os.path.exists(old_path):
                continue

            self.stdout.write("* %d {%s => %s}" % (job.id,
                                                   old_path[len_base_dir:],
                                                   date_path[len_base_dir:]))
            mkdir(os.path.dirname(date_path))
            if not os.path.exists(old_path):
                self.stdout.write("  -> no output directory")
                continue
            os.rename(old_path, date_path)
