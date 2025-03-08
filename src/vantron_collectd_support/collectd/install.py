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
    """
    Installs the CollectD plugin configuration.
    
    Reads a configuration template from package resources, substitutes the source directory and virtual
    environment paths, and writes the resulting configuration file to the designated location. Logs a warning
    if the environment variable for the virtual environment path is not set.
    """
    logger.info("Installing CollectD plugin")

    conf = importlib.resources.read_text(conf_package, COLLECTD_CONFIG_RESOURCE_BASENAME)
    venv_path = os.getenv(VENV_PATH_ENV_NAME)
    if not venv_path:
        logger.warning(f"{VENV_PATH_ENV_NAME} environment variable not set. Virtual environment path may be incorrect.")

    formatted_conf = conf.format(
        **{
            SRC_PATH_TEMPLATE_VAR_NAME: find_src_dir().as_posix(),
            VENV_PATH_TEMPLATE_VAR_NAME: venv_path,
        }
    )

    write_conf(formatted_conf)


def write_conf(formatted_conf):
    """
    Write formatted configuration to the CollectD config file.
    
    Logs the configuration details and writes the provided configuration string to the
    file at COLLECTD_CONFIG_PATH. If a PermissionError occurs, the function logs the
    exception and recommends running the command with elevated privileges.
    """
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
    """
    Return the absolute path of the source directory for the vantron package.
    
    This function locates the file for the vantron package using the inspect module,
    ascends two directory levels from the file location, and resolves the resulting
    path to an absolute path.
    """
    return Path(inspect.getfile(vantron_package)).parents[1].resolve()
