#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class Rate:
    def __init__(self, hz):
        self._hz = hz
        self._tsleep = 1.0 / hz

    def sleep(self):
        time.sleep(self._tsleep)
