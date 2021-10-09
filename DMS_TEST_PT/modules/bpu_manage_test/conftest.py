# -*- coding: utf-8 -*-
# @Time    : 2021/1/6
# @Author  : TingTing.Zhao
import pytest

from modules.bpu_manage_test.pylib.bpu_manage_library import *


@pytest.fixture(scope="module", autouse=True)
def bpumanage_suite_setup():
    goto_and_check_bpu_page()
