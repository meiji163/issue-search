import shlex
import subprocess

def get_issues(repo: str, limit: int):
    cmd = f"gh issue list -L {limit} -R {repo} --json title,body,number,labels,comments"
    ret = subprocess.run( 
            shlex.split(cmd), 
            capture_output=True
        ) 
    
    ret.check_returncode()
    return ret.stdout
