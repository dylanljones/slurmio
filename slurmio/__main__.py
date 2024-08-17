# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-04

import time
from datetime import timedelta
from typing import List

import click

import slurmio
from slurmio.models import Squeue
from slurmio.utility import get_user, padstr


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


def format_squeue(jobs: List[Squeue], maxw: int = 20):
    rows = list()
    headers = [
        "ID",
        "Name",
        "User",
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
        partition = job.partition  #
        if state == "RUNNING":
            t = str(timedelta(seconds=round(time.time() - job.start_time.number)))
        else:
            t = "00:00"
        # tlim = str(timedelta(minutes=job.time_limit.number))
        mem = str(job.memory_per_node.number)
        nodelist = job.nodes
        nodes = str(job.node_count.number)
        tasks = str(job.tasks.number)
        user = job.user_name

        row = [job_id, name, user, state, t, mem, partition, nodelist, nodes, tasks]
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
        user = get_user()

    try:
        jobs = slurmio.squeue(user=user, job_id=job_id)
    except Exception as e:
        raise click.ClickException(str(e))

    headers, rows = format_squeue(jobs, maxw)
    headerstr = delim.join([click.style(x, bold=True) for x in headers])
    click.echo()
    if not jobs:
        click.echo("No jobs found.")
        click.echo()
        return

    click.echo(headerstr)
    if header_line:
        click.echo("-" * len(headerstr))
    for parts in rows:
        state = parts[3].strip()
        if state != "RUNNING":
            parts = [click.style(x, fg="bright_black") for x in parts]
        else:
            parts[0] = click.style(parts[0], fg="bright_blue")
            parts[3] = click.style(parts[3], fg="green")
            fg = "yellow"
            parts[5] = click.style(parts[5], fg)
            parts[6] = click.style(parts[6], fg)
            parts[7] = click.style(parts[7], fg)
            parts[8] = click.style(parts[8], fg)
            parts[9] = click.style(parts[9], fg)
        click.echo(delim.join(parts))
    click.echo()


@cli.command(["showdirs", "sd"])
def showdirs():
    user = get_user()
    try:
        jobs = slurmio.squeue(user=user)
    except Exception as e:
        raise click.ClickException(str(e))

    if not jobs:
        click.echo("No jobs found.")
        return
    w1 = max(job.job_id for job in jobs) + 2
    w2 = max(len(job.name) for job in jobs) + 1

    for job in jobs:
        cwd = job.current_working_directory
        s1 = f"[{job.job_id}]"
        s2 = f"{job.name}:"
        header = click.style(f"{s1:<{w1}}", fg="bright_blue") + f" {s2:<{w2}} "
        click.echo(header + click.style(cwd, fg="yellow"))


if __name__ == "__main__":
    cli()
