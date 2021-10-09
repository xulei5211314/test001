# coding:utf-8
from library.common_lib import *


# 模块使用的fixture
@pytest.fixture()
def fix_upgrade():
    log.logger.info("begin test")
    yield
    common_lib.upgrade_j2()


@pytest.fixture()
def fix_upgrade_image():
    log.logger.info("begin test")
    yield
    common_lib.upgrade_j2()