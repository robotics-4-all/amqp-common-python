# -*- coding: utf-8 -*-
# Copyright (C) 2020  Panayiotou, Konstantinos <klpanagi@gmail.com>
# Author: Panayiotou, Konstantinos <klpanagi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import

import threading
import time
import sys

from .rate import Rate


if sys.version_info[0] < 3:
    Timer = threading.Timer
else:
    class TimerEvent:
        def __init__(self, last_expected, last_real,
                     current_expected, current_real,
                     last_duration):
            self.last_expected = last_expected
            self.last_real = last_real
            self.current_expected = current_expected
            self.current_real = current_real
            self.last_duration = last_duration


    class Timer(threading.Timer):
        def __init__(self, period, callback, oneshot=False):
            """
            Constructor.
            @param period: desired period between callbacks in seconds
            @type period: double
            @param callback: callback to be called
            @type callback: function taking TimerEvent
            @param oneshot: if True, fire only once, otherwise fire continuously
                until shutdown is called [default: False]
            @type oneshot: bool
            """
            super(Timer, self).__init__()
            self._period = period
            self._callback = callback
            self._oneshot = oneshot
            self._shutdown = False
            self.setDaemon(True)

        def shutdown(self):
            """
            Stop firing callbacks.
            """
            self._shutdown = True

        def run(self):
            r = Rate(1.0 / self._period)
            current_expected = time.time() + self._period
            last_expected, last_real, last_duration = None, None, None
            while True:
                try:
                    r.sleep()
                except KeyboardInterrupt as exc:
                    print(exc)
                    break
                if self._shutdown:
                    break
                start = time.time()
                current_real = start
                self._callback(TimerEvent(last_expected, last_real,
                                          current_expected,
                                          current_real,
                                          last_duration))
                if self._oneshot:
                    break
                last_duration = time.time() - start
                last_expected, last_real = current_expected, current_real
                current_expected += self._period
