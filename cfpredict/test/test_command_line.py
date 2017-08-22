#!/usr/bin/env python

from unittest import TestCase

from cfpredict.command_line import main


class TestCmd(TestCase):
    def test_basic(self):
        main()