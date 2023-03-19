# -*- coding: utf-8 -*-

import typing as T
import dataclasses

if T.TYPE_CHECKING:
    from .main import Env


@dataclasses.dataclass
class AppMixin:
    pass