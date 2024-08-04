# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-03

import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from subprocess import PIPE, Popen
from time import sleep
from typing import Any, Dict, List, Union

from .models import Sacct, Squeue


@dataclass
class SlurmJob:
    """..deprecated:: 1.0.0."""

    jobid: str
    account: str = None
    array_job_id: str = None
    array_task_id: str = None
    command: str = None
    comment: str = None
    contiguous: str = None
    cores_per_socket: str = None
    core_spec: str = None
    cpus: str = None
    sct: str = None
    dependency: str = None
    end_time: str = None
    exc_nodes: str = None
    exec_host: str = None
    features: str = None
    group: str = None
    licenses: str = None
    min_cpus: str = None
    min_memory: str = None
    min_tmp_disk: str = None
    name: str = None
    nice: str = None
    nodelist: str = None
    nodelist_reason: str = None
    nodes: str = None
    over_subscribe: str = None
    partition: str = None
    priority: str = None
    qos: str = None
    reason: str = None
    req_nodes: str = None
    reservation: str = None
    schednodes: str = None
    sockets_per_node: str = None
    st: str = None
    start_time: str = None
    state: str = None
    submit_time: str = None
    threads_per_core: str = None
    time: str = None
    time_left: str = None
    time_limit: str = None
    tres_per_node: str = None
    uid: str = None
    user: str = None
    wckey: str = None
    work_dir: str = None

    @property
    def output_file(self) -> Path:
        return Path(f"slurm-{self.jobid}.out")

    def pformat(self) -> str:
        lines = list()
        for k, v in self.__dict__.items():
            if v is not None:
                lines.append(f"{k + ':':<20} {v}")
        return "\n".join(lines)

    def dict(self) -> Dict[str, Any]:
        return dict(self.__dict__.items())

    def __repr__(self) -> str:
        return f"Job({self.jobid}, {self.name}, {self.state})"


def _run(cmd: List[str], shell: bool = None) -> str:
    """Run a command and return the output or raise an exception if it fails."""
    process = Popen(cmd, shell=shell, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    if err:
        raise Exception(err.decode("utf-8"))
    return out.decode("utf-8")


def _parse_time(t: str) -> timedelta:
    days, time = t.split("-") if "-" in t else (0, t)
    parts = time.split(":")
    seconds = int(parts[-1])
    if len(parts) > 1:
        seconds += 60 * int(parts[-2])
    if len(parts) > 2:
        seconds += 3600 * int(parts[-3])
    seconds += 24 * 3600 * int(days)
    return timedelta(seconds=seconds)


def squeue_old(
    user: str = None,
    job_id: str = None,
    fields: List[str] = None,
    delim: str = "|",
) -> List[SlurmJob]:
    """Get a list of jobs from the squeue command."""
    # Build squeue command with options
    cmd = ["squeue"]
    if user:
        cmd += ["-u", user]
    if job_id:
        cmd += ["--job", job_id]

    if fields is None:
        # Return all fields by default
        fields = ["all"]
        delim = "|"

    cmd += ["-o", delim.join([f"%{f}" for f in fields])]

    # Run squeue command
    data = _run(cmd)

    # Parse squeue output
    lines = data.splitlines()
    header = lines.pop(0)
    columns = list()
    for c in header.split(delim):
        c = c.strip().lower()
        if c == "nodelist(reason)":
            c = "nodelist_reason"
        if c == "s:c:t":
            c = "sct"
        columns.append(c)
    items = list()
    for line in lines:
        values = [x.strip() for x in line.split(delim)]
        item = {k: v for k, v in zip(columns, values)}
        items.append(SlurmJob(**item))
    return items


def squeue(user: str = None, job_id: str = None) -> List[Squeue]:
    cmd = ["squeue", "--json"]
    if user:
        cmd += ["-u", user]
    if job_id:
        cmd += ["--job", job_id]
    out = _run(cmd)
    raw = json.loads(out)
    errors = raw["errors"]
    warnings = raw["warnings"]
    if warnings:
        print("Warning:", warnings)
    if errors:
        raise Exception(errors)
    return [Squeue(**job) for job in raw["jobs"]]


def sacct(user: str = None, job_id: str = None) -> List[Sacct]:
    cmd = ["sacct", "--json"]
    if user:
        cmd += ["-u", user]
    if job_id:
        cmd += ["--job", job_id]
    out = _run(cmd)
    raw = json.loads(out)
    errors = raw["errors"]
    warnings = raw["warnings"]
    if warnings:
        print("Warning:", warnings)
    if errors:
        raise Exception(errors)
    return [Sacct(**job) for job in raw["jobs"]]


def sbatch(file_or_script: Union[str, Path]) -> Squeue:
    """Submit a slurm job and return the job id."""
    file = Path(file_or_script)
    if file.exists():
        cmd = ["sbatch", str(file)]
    else:
        cmd = [
            "\n".join(["sbatch << EOF", file_or_script, "EOF"]),
        ]
    stdout = _run(cmd, shell=True)
    success_msg = "Submitted batch job"
    assert success_msg in stdout
    job_id = stdout.split()[3].strip()

    jobs = squeue(job_id=job_id)
    while len(jobs) == 0:
        sleep(0.1)
        jobs = squeue(job_id=job_id)
    return jobs[0]


def scancel(job_id: str) -> str:
    """Cancel a slurm job and return the output."""
    cmd = ["scancel", job_id]
    out = _run(cmd)
    return out


def rm_slurm_files(root: Union[str, Path] = ".") -> None:
    """Remove all slurm files in the current directory."""
    root = Path(root)
    for file in root.glob("slurm-*.out"):
        file.unlink()
