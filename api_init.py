import subprocess
cmd = ["uvicorn", "api:app"]
subprocess.Popen(cmd, close_fds=True)