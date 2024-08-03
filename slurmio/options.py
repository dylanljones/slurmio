# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-03

"""Slurm options module."""

from collections import OrderedDict
from collections.abc import MutableMapping
from typing import Iterable, Union

from .enums import Options

# noinspection PyProtectedMember
OPTIONS = set(Options._member_names_)

K = Union[str, Options]
V = Union[str, int, float]


class SlurmOptions(MutableMapping):
    PREFIX = "#SBATCH"

    def __init__(
        self,
        cpus_per_gpu: Union[str, int] = None,
        cpus_per_task: Union[str, int] = None,
        gpus_per_node: Union[str, int] = None,
        gpus_per_socket: Union[str, int] = None,
        gpus_per_task: Union[str, int] = None,
        gpus: Union[str, int] = None,
        job_name: str = None,
        mail_type: str = None,
        mail_user: str = None,
        mem: Union[str, int] = None,
        mem_per_cpu: Union[str, int] = None,
        mem_per_gpu: Union[str, int] = None,
        nodes: Union[str, int] = None,
        ntasks: Union[str, int] = None,
        ntasks_per_node: Union[str, int] = None,
        ntasks_per_socket: Union[str, int] = None,
        ntasks_per_core: Union[str, int] = None,
        ntasks_per_gpu: Union[str, int] = None,
        partition: str = None,
        priority: Union[str, int] = None,
        time: str = None,
        **kwargs,
    ):
        self._options = OrderedDict()

        for key, val in locals().items():
            if key not in ("self", "kwargs") and val is not None:
                kwargs[key] = val
        self.update(kwargs)

    def __iter__(self) -> Iterable[str]:
        return iter(self._options)

    def __len__(self) -> int:
        return len(self._options)

    def __getitem__(self, key: K) -> V:
        key = key.value if isinstance(key, Options) else key.replace("-", "_")
        return self._options[key]

    def __setitem__(self, key: K, value: V) -> None:
        key = key.value if isinstance(key, Options) else key.replace("-", "_")
        if key not in OPTIONS:
            raise ValueError(f"Invalid option: {key}")
        self._options[key] = str(value)

    def __delitem__(self, key: K) -> None:
        key = key.value if isinstance(key, Options) else key.replace("-", "_")
        del self._options[key]

    def __getattr__(self, key: str) -> V:
        return self.__getitem__(key)

    def __setattr__(self, key: str, value: V) -> None:
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def set(self, key: K, value: V) -> "SlurmOptions":
        self.__setitem__(key, value)
        return self

    def require(self, *keys: K) -> bool:
        for key in keys:
            key = key.value if isinstance(key, Options) else key.replace("-", "_")
            if key not in self:
                return False
        return True

    def loads(self, text: str) -> None:
        for line in text.splitlines():
            line = line.replace(self.PREFIX, "")
            key, value = line[1:].split("=", 1)
            self.__setitem__(key.lstrip("--"), value)

    def dumps(self, indent: bool = False) -> str:
        w = 20 if indent else 0
        lines = list()
        for k, v in self.items():
            lines.append(f"{self.PREFIX} --{k.replace('_', '-'):<{w}}={v}")
        return "\n".join(lines)

    def pformat(self) -> str:
        return "\n".join(f"{k + ':':<20}{v}" for k, v in self.items())

    def __str__(self) -> str:
        return self.pformat()
