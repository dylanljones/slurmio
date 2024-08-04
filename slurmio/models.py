# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2024-08-03

from enum import Enum
from pprint import pformat
from typing import Any, Dict, List, Union

from pydantic import BaseModel


class Options(Enum):
    account = "account"
    acctg_freq = "acctg_freq"
    array = "array"
    batch = "batch"
    bb = "bb"
    bbf = "bbf"
    begin = "begin"
    chdir = "chdir"
    cluster_constraint = "cluster_constraint"
    clusters = "clusters"
    comment = "comment"
    constraint = "constraint"
    container = "container"
    container_id = "container_id"
    contiguous = "contiguous"
    core_spec = "core_spec"
    cores_per_socket = "cores_per_socket"
    cpu_freq = "cpu_freq"
    cpus_per_gpu = "cpus_per_gpu"
    cpus_per_task = "cpus_per_task"
    deadline = "deadline"
    delay_boot = "delay_boot"
    dependency = "dependency"
    distribution = "distribution"
    error = "error"
    exclude = "exclude"
    exclusive = "exclusive"
    export = "export"
    export_file = "export_file"
    extra = "extra"
    extra_node_info = "extra_node_info"
    get_user_env = "get_user_env"
    gid = "gid"
    gpu_bind = "gpu_bind"
    gpu_freq = "gpu_freq"
    gpus_per_node = "gpus_per_node"
    gpus_per_socket = "gpus_per_socket"
    gpus_per_task = "gpus_per_task"
    gpus = "gpus"
    gres = "gres"
    gres_flags = "gres_flags"
    hint = "hint"
    hold = "hold"
    ignore_pbs = "ignore_pbs"
    input = "input"
    job_name = "job_name"
    kill_on_invalid_dep = "kill_on_invalid_dep"
    licenses = "licenses"
    mail_type = "mail_type"
    mail_user = "mail_user"
    mcs_label = "mcs_label"
    mem = "mem"
    mem_bind = "mem_bind"
    mem_per_cpu = "mem_per_cpu"
    mem_per_gpu = "mem_per_gpu"
    mincpus = "mincpus"
    network = "network"
    nice = "nice"
    no_kill = "no_kill"
    no_requeue = "no_requeue"
    nodefile = "nodefile"
    nodelist = "nodelist"
    nodes = "nodes"
    ntasks_per_core = "ntasks_per_core"
    ntasks_per_gpu = "ntasks_per_gpu"
    ntasks_per_node = "ntasks_per_node"
    ntasks_per_socket = "ntasks_per_socket"
    ntasks = "ntasks"
    open_mode = "open_mode"
    output = "output"
    overcommit = "overcommit"
    oversubscribe = "oversubscribe"
    partition = "partition"
    power = "power"
    prefer = "prefer"
    priority = "priority"
    profile = "profile"
    propagate = "propagate"
    qos = "qos"
    quiet = "quiet"
    reboot = "reboot"
    requeue = "requeue"
    reservation = "reservation"
    signal = "signal"
    sockets_per_node = "sockets_per_node"
    spread_job = "spread_job"
    switches = "switches"
    test_only = "test_only"
    thread_spec = "thread_spec"
    threads_per_core = "threads_per_core"
    time_min = "time_min"
    time = "time"
    tmp = "tmp"
    tres_per_task = "tres_per_task"
    uid = "uid"
    use_min_nodes = "use_min_nodes"
    verbose = "verbose"
    wait_all_nodes = "wait_all_nodes"
    wait = "wait"
    wckey = "wckey"
    wrap = "wrap"


class Base(BaseModel):
    def to_dict(self) -> Dict[str, Any]:
        """Convert the schema to a dictionary **without** serialization."""
        return {key: getattr(self, key) for key in self.model_fields}

    def pformat(self) -> str:
        return pformat(self.to_dict())


class Number(Base):
    set: bool
    infinite: bool
    number: int


class Signal(Base):
    id: Number
    name: str


class ExitCode(Base):
    status: List[str]
    return_code: Number
    signal: Signal


class Squeue(Base):
    job_id: int
    account: str = None
    accrue_time: Number = None
    admin_comment: str = None
    allocating_node: str = None
    array_job_id: Number = None
    array_task_id: Number = None
    array_max_tasks: Number = None
    array_task_string: str = None
    association_id: int = None
    batch_features: str = None
    batch_flag: bool = None
    batch_host: str = None
    flags: List[str] = None
    burst_buffer: str = None
    burst_buffer_state: str = None
    cluster: str = None
    cluster_features: str = None
    command: str = None
    comment: str = None
    container: str = None
    container_id: str = None
    contiguous: bool = None
    core_spec: int = None
    thread_spec: int = None
    cores_per_socket: Number = None
    billable_tres: Number = None
    cpus_per_task: Number = None
    cpu_frequency_minimum: Number = None
    cpu_frequency_maximum: Number = None
    cpu_frequency_governor: Number = None
    cpus_per_tres: str = None
    cron: str = None
    deadline: Number = None
    delay_boot: Number = None
    dependency: str = None
    derived_exit_code: ExitCode = None
    eligible_time: Number = None
    end_time: Number = None
    excluded_nodes: str = None
    exit_code: ExitCode = None
    extra: str = None
    failed_node: str = None
    features: str = None
    federation_origin: str = None
    federation_siblings_active: str = None
    federation_siblings_viable: str = None
    gres_detail: List[str] = None
    group_id: int = None
    group_name: str = None
    het_job_id: Number = None
    het_job_id_set: str = None
    het_job_offset: Number = None
    job_resources: Dict[str, Any] = None
    job_size_str: List[str] = None
    job_state: List[str] = None
    last_sched_evaluation: Number = None
    licenses: str = None
    mail_type: List[str] = None
    mail_user: str = None
    max_cpus: Number = None
    max_nodes: Number = None
    mcs_label: str = None
    memory_per_tres: str = None
    name: str = None
    network: str = None
    nodes: str = None
    nice: int = None
    tasks_per_core: Number = None
    tasks_per_tres: Number = None
    tasks_per_node: Number = None
    tasks_per_socket: Number = None
    tasks_per_board: Number = None
    cpus: Number = None
    node_count: Number = None
    tasks: Number = None
    partition: str = None
    prefer: str = None
    memory_per_cpu: Number = None
    memory_per_node: Number = None
    minimum_cpus_per_node: Number = None
    minimum_tmp_disk_per_node: Number = None
    power: Dict[str, Any] = None
    preempt_time: Number = None
    preemptable_time: Number = None
    pre_sus_time: Number = None
    hold: bool = None
    priority: Number = None
    profile: List[str] = None
    qos: str = None
    reboot: bool = None
    required_nodes: str = None
    minimum_switches: int = None
    requeue: bool = None
    resize_time: Number = None
    restart_cnt: int = None
    resv_name: str = None
    scheduled_nodes: str = None
    selinux_context: str = None
    shared: List[str] = None
    exclusive: List[str] = None
    oversubscribe: bool = None
    show_flags: List[str] = None
    sockets_per_board: int = None
    sockets_per_node: Number = None
    start_time: Number = None
    state_description: str = None
    state_reason: str = None
    standard_error: str = None
    standard_input: str = None
    standard_output: str = None
    submit_time: Number = None
    suspend_time: Number = None
    system_comment: str = None
    time_limit: Number = None
    time_minimum: Number = None
    threads_per_core: Number = None
    tres_bind: str = None
    tres_freq: str = None
    tres_per_job: str = None
    tres_per_node: str = None
    tres_per_socket: str = None
    tres_per_task: str = None
    tres_req_str: str = None
    tres_alloc_str: str = None
    user_id: int = None
    user_name: str = None
    maximum_switch_wait_time: int = None
    wckey: str = None
    current_working_directory: str = None

    def __str__(self) -> str:
        return f"Job({self.job_id}, {self.name}, {','.join(self.job_state)})"


class TimeValues(Base):
    seconds: int
    microseconds: int


class Time(Base):
    elapsed: int
    eligible: int = None
    end: Union[int, Number] = None
    start: Union[int, Number] = None
    submission: int = None
    suspended: int = None
    system: TimeValues = None
    limit: Union[int, Number] = None
    total: TimeValues = None
    user: TimeValues = None


class TresItem(Base):
    type: str
    name: str
    id: int
    count: int
    task: int = None
    node: str = None


class TresItems(Base):
    min: List[TresItem]
    max: List[TresItem]
    average: List[TresItem]
    total: List[TresItem]


class TresSteps(Base):
    requested: TresItems
    consumed: TresItems
    allocated: List[TresItem]


class Tres(Base):
    requested: List[TresItem]
    allocated: List[TresItem]


class Step(Base):
    time: Time
    exit_code: ExitCode
    nodes: Dict[str, Any]
    tasks: Dict[str, Any]
    pid: str
    CPU: Dict[str, Any]
    kill_request_user: str
    state: List[str]
    statistics: Dict[str, Any]
    step: Dict[str, str]
    task: Dict[str, str]
    tres: TresSteps


class Sacct(Base):
    account: str
    comment: Dict[str, str]
    allocation_nodes: int
    array: Dict[str, Any]
    association: Dict[str, Any]
    block: str
    cluster: str
    constraints: str
    container: str
    derived_exit_code: ExitCode
    time: Time
    exit_code: ExitCode
    extra: str
    failed_node: str
    flags: List[str]
    group: str
    het: Dict[str, Union[int, Number]]
    job_id: int
    name: str
    licenses: str
    mcs: Dict[str, str]
    nodes: str
    partition: str
    hold: bool
    priority: Number
    qos: str
    required: Dict[str, Any]
    kill_request_user: str
    reservation: Dict[str, Any]
    script: str
    state: Dict[str, Any]
    steps: List[Step]
    submit_line: str
    tres: Tres
    used_gres: str
    user: str
    wckey: Dict[str, Any]
    working_directory: str

    def __str__(self) -> str:
        return f"SacctJob({self.job_id}, {self.name})"
