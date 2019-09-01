from .data_station import DataStation
from .jr_coin import JrCoin
from .double_sign import DoubleSign
from .daka_app import DakaApp
from .sign_jr import SignJR
from .bean_app import BeanApp
from .bean import Bean
from config import config
import logging

logger = logging.getLogger('jobs')


__all__ = ['jobs_all', 'logger']

jobs_mobile = [DakaApp, BeanApp, DataStation, JrCoin]
jobs_web = [Bean, SignJR]
jobs_all = jobs_mobile + jobs_web + [DoubleSign]


def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(config.log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


set_logger()
