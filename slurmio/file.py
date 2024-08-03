# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-03

import re
from collections.abc import MutableSequence
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Union

from .options import SlurmOptions
from .slurm import SlurmJob, sbatch


@dataclass
class SlurmCommand:
    cmd: str
    comment: str = ""

    def tostring(self) -> str:
        s = self.cmd
        if self.comment:
            s += f" # {self.comment}" if s else f"# {self.comment}"
        return s

    def replace(self, pattern: str, repl: str) -> None:
        self.cmd = re.sub(pattern, repl, self.cmd)

    def replace_comment(self, pattern: str, repl: str) -> None:
        self.comment = re.sub(pattern, repl, self.comment)


class SlurmFile(MutableSequence):
    def __init__(
        self,
        file: Union[str, Path] = None,
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
        shell: str = "/bin/bash",
        **kwargs,
    ):
        self._file: Union[Path, None] = Path(file) if file is not None else None
        self._shell: str = shell
        self._options: SlurmOptions = SlurmOptions()
        self._commands: List[SlurmCommand] = list()

        self.load(missing_ok=True)
        for key, val in locals().items():
            if key not in ("self", "kwargs", "file", "shell") and val is not None:
                kwargs[key] = val
        self.options.update(kwargs)

    @property
    def file(self) -> Path:
        return self._file

    @property
    def options(self) -> SlurmOptions:
        return self._options

    @property
    def shell(self) -> str:
        return self._shell

    @shell.setter
    def shell(self, value: str) -> None:
        self._shell = value

    @property
    def commands(self) -> List[SlurmCommand]:
        return self._commands

    def insert(self, index: int, value: SlurmCommand) -> None:
        self._commands.insert(index, value)

    def __len__(self) -> int:
        return len(self._commands)

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[SlurmCommand, MutableSequence[SlurmCommand]]:
        return self._commands[index]

    def __setitem__(
        self,
        index: Union[int, slice],
        value: Union[SlurmCommand, Iterable[SlurmCommand]],
    ) -> None:
        if isinstance(index, int):
            self._commands[index] = value
        else:
            self._commands[index] = list(value)

    def __delitem__(self, index: Union[int, slice]) -> None:
        del self._commands[index]

    def loads(self, data: str) -> None:
        """Parse the content of a SLURM file."""
        lines = data.splitlines(keepends=False)
        # Parse shebang line
        if lines[0].startswith("#!"):
            self._shell = lines.pop(0).replace("#!", "").strip()

        # Parse SLURM options
        self._options.clear()
        # Skip empty lines
        while lines and not lines[0].strip():
            lines.pop(0)

        while lines:
            line = lines[0].strip()
            if not line.startswith("#SBATCH"):
                break
            line = lines.pop(0).replace("#SBATCH", "").strip()
            key, value = line[1:].split("=", 1)
            self._options[key.lstrip("--")] = value

        # Parse commands
        cmds = list()
        for s in lines:
            s = s.strip()
            if "#" in s:
                command, comment = s.split("#", 1)
                cmds.append(SlurmCommand(command.strip(), comment.strip()))
            else:
                cmds.append(SlurmCommand(s))
        self._commands = cmds

    def dumps(self, linesep: str = "\n") -> str:
        """Serialize the SLURM file to a string."""
        lines = ["#!" + self._shell]
        for k, v in self._options.items():
            lines.append(f"#SBATCH --{k.replace('_', '-')}={v}")

        for cmd in self._commands:
            line = cmd.cmd
            if cmd.comment:
                if line:
                    line += " "
                line += f"# {cmd.comment}"
            lines.append(line)

        return linesep.join(lines) + linesep

    def load(self, file: Union[str, Path] = None, missing_ok: bool = False) -> None:
        """Load a SLURM file from disk."""
        file = Path(file) if file is not None else self._file
        if file is None:
            return
        if not file.exists():
            if missing_ok:
                return
            raise FileNotFoundError(f"File not found: {file}")

        with open(str(file), "r") as fh:
            data = fh.read()
        self.loads(data)

    def dump(self, file: Union[str, Path] = None, mkdir: bool = False) -> None:
        """Save the SLURM file to disk."""
        file = Path(file) if file is not None else self._file
        if mkdir:
            file.parent.mkdir(parents=True, exist_ok=True)

        data = self.dumps()
        with open(str(file), "w") as fh:
            fh.write(data)

    def add_cmd(
        self,
        command: str = "",
        comment: str = None,
        after: SlurmCommand = None,
        before: SlurmCommand = None,
    ) -> SlurmCommand:
        """Add a command to the SLURM file."""
        if after is not None and before is not None:
            raise ValueError("Only one of 'after' and 'before' can be specified.")

        cmd = SlurmCommand(command, comment)
        if after is not None:
            idx = self._commands.index(after)
            self._commands.insert(idx + 1, cmd)
        elif before is not None:
            idx = self._commands.index(before)
            self._commands.insert(idx, cmd)
        else:
            self._commands.append(cmd)
        return cmd

    def add_comment(
        self, comment: str, after: SlurmCommand = None, before: SlurmCommand = None
    ) -> SlurmCommand:
        """Add a comment to the SLURM file."""
        return self.add_cmd(comment=comment, after=after, before=before)

    def add_line(
        self, after: SlurmCommand = None, before: SlurmCommand = None
    ) -> SlurmCommand:
        """Add an empty line to the SLURM file."""
        return self.add_cmd(after=after, before=before)

    def add(
        self, text: str = "", after: SlurmCommand = None, before: SlurmCommand = None
    ) -> SlurmCommand:
        text = text.strip()
        if "#" in text:
            command, comment = text.split("#", 1)
        else:
            command, comment = text, None
        return self.add_cmd(command, comment, after=after, before=before)

    def echo(
        self,
        text: str,
        comment: str = None,
        after: SlurmCommand = None,
        before: SlurmCommand = None,
    ) -> SlurmCommand:
        return self.add_cmd(f"echo {text}", comment=comment, after=after, before=before)

    def remove_cmd(self, cmd: SlurmCommand) -> None:
        self._commands.remove(cmd)

    def clear_cmds(self) -> None:
        self._commands.clear()

    def matchall(self, query: Union[str, re.Pattern]) -> List[SlurmCommand]:
        if isinstance(query, str):
            query = re.compile(query)
        return [cmd for cmd in self._commands if query.match(cmd.tostring())]

    def match(self, query: Union[str, re.Pattern]) -> SlurmCommand:
        matches = self.matchall(query)
        if len(matches) == 0:
            raise ValueError(f"No matches found for {query}!")
        elif len(matches) > 1:
            raise ValueError(f"Multiple matches found for {query}!")
        return matches[0]

    def findall(
        self,
        command: Union[str, re.Pattern] = None,
        comment: Union[str, re.Pattern] = None,
    ) -> List[SlurmCommand]:
        if command is not None:
            if isinstance(command, str):
                command = re.compile(command)
            return [cmd for cmd in self._commands if command.match(cmd.cmd)]

        if comment is not None:
            if isinstance(comment, str):
                comment = re.compile(comment)
            return [cmd for cmd in self._commands if comment.match(cmd.comment)]

    def sbatch(self) -> SlurmJob:
        """Submit the SLURM file as a job."""
        return sbatch(self.dumps())
