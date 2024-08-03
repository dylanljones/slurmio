# 📁 Slurm-I/O

> [!WARNING]
>
> This project was written for my **personal** workflow and might not be suitable for
> your use case.


## 🛠️ Installation

Install via

```bash
pip install git+ssh://git@github.com/dylanljones/slurmio.git
```

## 🚀 Usage

Basic example:

```python
import slurmio

slurm = slurmio.SlurmFile(job_name="Test", mail_user="example@mail.com", mem="2gb")
slurm.add_line()
slurm.add_comment("Run commands")
slurm.add_cmd("echo Hello world", comment="Print Hello world")
print(slurm.dumps())
```
returns
```bash
#!/bin/bash
#SBATCH --job-name=Test
#SBATCH --mail-user=example@mail.com
#SBATCH --mem=2gb

# Run commands
echo Hello world # Print Hello world
```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
