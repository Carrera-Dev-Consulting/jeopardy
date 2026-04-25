"""
.. include:: ../README.md
   :start-line: 2
   :end-before: Contribution
"""

import logging
from pydantic_settings import BaseSettings
from zombie_nomnom_api.game import GameMakerType


class Configs(BaseSettings):
    cors_methods: set[str] = ["*"]
    cors_headers: set[str] = ["*"]
    cors_origins: set[str] = ["*"]
    cors_allow_credentials: bool = True
    log_level: str = "DEBUG"
    game_maker_type: GameMakerType = GameMakerType.memory
    oauth_issuer: str = ""
    oauth_domain: str = ""
    oauth_algorithms: str = ""
    oauth_audience: str = ""


configs = Configs()


logging.basicConfig(level=configs.log_level)
