import importlib
import importlib.resources
import inspect
import os
import sys
from pathlib import Path

from loguru import logger

import vantron_collectd_support as vantron_package

from . import conf as conf_package

logger.remove()
logger.add(sys.stderr, colorize=True, format="<green>{elapsed}</green> <lvl>{level}</lvl> {message}")

COLLECTD_CONFIG_RESOURCE_BASENAME = "vantron.collectd.conf"
SRC_PATH_TEMPLATE_VAR_NAME = "vantron_package_src_path"
VENV_PATH_TEMPLATE_VAR_NAME = "vantron_package_venv_packages_path"
VENV_PATH_ENV_NAME = "VIRTUAL_ENV"
COLLECTD_CONFIG_PATH = "/etc/collectd/collectd.conf.d/vantron.collectd.conf"


def run():
    logger.info("Installing CollectD plugin")

    conf = importlib.resources.read_text(conf_package, COLLECTD_CONFIG_RESOURCE_BASENAME)
    venv_path = os.getenv(VENV_PATH_ENV_NAME)
    if not venv_path:
        raise EnvironmentError(
            f"{VENV_PATH_ENV_NAME} environment variable not set. Virtual environment path may be incorrect."
        )

    venv_packages_path = (
        next((Path(venv_path) / "lib").glob("python3.*/", case_sensitive=True)) / "site-packages"
    ).resolve()

    formatted_conf = conf.format(
        **{
            SRC_PATH_TEMPLATE_VAR_NAME: find_src_dir().as_posix(),
            VENV_PATH_TEMPLATE_VAR_NAME: venv_packages_path.as_posix(),
        }
    )

    write_conf(formatted_conf)


def write_conf(formatted_conf):
    logger.info(f"Config:\n\n{formatted_conf}")
    try:
        logger.info(f"Writing to {COLLECTD_CONFIG_PATH}")
        with open(COLLECTD_CONFIG_PATH, "w") as f:
            f.write(formatted_conf)
    except PermissionError:
        logger.exception(f"Cannot write to {COLLECTD_CONFIG_PATH}")
        logger.error("Try:")
        logger.error("sudo -E `which uv` run install-collectd-plugin")


def find_src_dir() -> Path:
    return Path(inspect.getfile(vantron_package)).parents[1].resolve()
