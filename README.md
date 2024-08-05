# 📁 Slurm-I/O

Slurm-I/O is a lightweight Python package for managing slurm jobs and scripts. The package provides
a simple interface for reading, writing and updating slurm scripts and managing slurm
jobs.


> [!NOTE]
>
> This project was written for my **personal** workflow and might not be suitable for
> your use case.


## 🛠️ Installation

Install via

```bash
pip install git+ssh://git@github.com/dylanljones/slurmio.git
```

## 🚀 Usage


### Slurm Scripts

Slurm scripts can be read, saved and updated using the `SlurmScript` class.
The file handler supports slurm options, commands and comments and can be used
to re-order commands in the file.

```python
import slurmio

slurm = slurmio.SlurmScript(job_name="Test", mail_user="example@mail.com", mem="2gb")
slurm.add_line()
slurm.add_comment("Run commands")
slurm.add_cmd("echo Hello world", comment="Print Hello world")
slurm.dump("test.slurm")
```
This will generate the following file:
```bash
#!/bin/bash
#SBATCH --job-name=Test
#SBATCH --mail-user=example@mail.com
#SBATCH --mem=2gb

# Run commands
echo Hello world # Print Hello world
```

A job can be run without writing a slurm script via the sbatch method:
```python
slurm.sbatch()
```

### Managing Slurm Jobs

`slurmio` provides methods to manage slurm jobs, mirroring the CLI commands:
```python
import slurmio

# Get a list of all slurm jobs for a user
jobs = slurmio.squeue(user="user")

 # Get a specific job by id
job = slurmio.squeue(job_id="12345678")

# Start a job via a slurm script file
job = slurmio.sbatch("test.slurm")

# Cancel a job by id
slurmio.scancel(job_id=job.job_id)
```

### CLI

`slurmio` provides a CLI for managing slurm jobs and scripts. These commands are
basically clones of the original slurm commands - with some improvements:

```bash
slurmio squ -u user
```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
