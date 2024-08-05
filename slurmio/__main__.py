# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-04

import os
import pwd
import time
from datetime import timedelta
from typing import List

import click

import slurmio
from slurmio.models import Squeue


class AliasedGroup(click.Group):
    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` but for lists."""

        def decorator(f):
            if isinstance(args[0], list):
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    cmd = super(AliasedGroup, self).command(alias, *args[1:], **kwargs)(
                        f
                    )
                    cmd.short_help = "Alias for '{}'".format(_args[0])
            else:
                _args = args
            cmd = super(AliasedGroup, self).command(*_args, **kwargs)(f)
            return cmd

        return decorator


def padstr(s: str, w: int, align: str = ">", placeholder: str = "...") -> str:
    s = s[:w] if len(s) <= w else s[: w - len(placeholder)] + placeholder
    return f"{s:{align}{w}}"


def format_squeue(jobs: List[Squeue], maxw: int = 20):
    rows = list()
    headers = [
        "ID",
        "Name",
        "State",
        "Time",
        "Memory",
        "Partition",
        "Node-List",
        "Nodes",
        "Tasks",
    ]
    widths = [len(x) for x in headers]
    for job in jobs:
        job_id = str(job.job_id)
        name = job.name
        state = ",".join(job.job_state)
        partition = job.partition
        t = str(timedelta(seconds=round(time.time() - job.start_time.number)))
        # tlim = str(timedelta(minutes=job.time_limit.number))
        mem = str(job.memory_per_node.number)
        nodelist = job.nodes
        nodes = str(job.node_count.number)
        tasks = str(job.tasks.number)

        row = [job_id, name, state, t, mem, partition, nodelist, nodes, tasks]
        widths = [max(len(x), y) for x, y in zip(row, widths)]

        rows.append(row)

    widths = [min(x, maxw) for x in widths]
    headers = [padstr(x.upper(), w) for x, w in zip(headers, widths)]
    padded_rows = list()
    for row in rows:
        parts = [padstr(x, w) for x, w in zip(row, widths)]
        padded_rows.append(parts)
    return headers, padded_rows


@click.group(name="slurmio", cls=AliasedGroup)
def cli():
    pass


@cli.command(["squeue", "squ"])
@click.option("--me", "-m", is_flag=True, help="Show only my jobs", default=False)
@click.option("--user", "-u", help="Filter jobs by user", default=None)
@click.option("--job_id", "-i", help="Filter jobs by job id", default=None)
def squeue(me: bool, user: str, job_id: str):
    delim = " | "
    maxw = 20
    header_line = False

    if me:
        # Get current user name
        if user:
            raise click.BadOptionUsage(
                "--me", "Cannot use --me and --user at the same time."
            )
        user = pwd.getpwuid(os.getuid()).pw_name

    jobs = slurmio.squeue(user=user, job_id=job_id)
    headers, rows = format_squeue(jobs, maxw)
    headerstr = delim.join([click.style(x, bold=True) for x in headers])
    click.echo()
    click.echo(headerstr)
    if header_line:
        click.echo("-" * len(headerstr))
    for parts in rows[1:]:
        state = parts[2].strip()
        if state != "RUNNING":
            parts = [click.style(x, fg="bright_black") for x in parts]
        else:
            parts[0] = click.style(parts[0], fg="bright_blue")
            parts[2] = click.style(parts[2], fg="green")
            fg = "yellow"
            parts[4] = click.style(parts[4], fg)
            parts[5] = click.style(parts[5], fg)
            parts[6] = click.style(parts[6], fg)
            parts[7] = click.style(parts[7], fg)
            parts[8] = click.style(parts[8], fg)
        click.echo(delim.join(parts))
    click.echo()


if __name__ == "__main__":
    cli()