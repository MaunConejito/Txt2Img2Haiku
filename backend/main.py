import os
import uvicorn

def read_env_vars(env_dir, env_files):

    lines = []
    for env_file in env_files:
        with open(os.path.join(env_dir, env_file), 'r') as file:
            lines += file.readlines()

    kvps = [line.strip().split('=') for line in lines\
            if not (line.startswith('#') or line.isspace())]

    for key, value in kvps:
        os.environ[key] = value

if __name__ == '__main__':

    read_env_vars('..', ['secrets.env', 'backend.env'])
    
    uvicorn.run('qdrant_service.service:app', host='0.0.0.0', port=8000, reload=True)
