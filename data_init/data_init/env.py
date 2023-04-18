from typing import List
import os

def read_env_vars(env_dir: str, env_files: List[str]):

    lines = []
    for env_file in env_files:
        with open(os.path.join(env_dir, env_file), 'r') as file:
            lines += file.readlines()

    kvps = [line.strip().split('=') for line in lines\
            if not (line.startswith('#') or line.isspace())]

    for key, value in kvps:
        os.environ[key] = value
