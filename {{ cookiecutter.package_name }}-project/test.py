import subprocess

args = ["git", "branch"]
res = subprocess.run(args, capture_output=True, check=True)
for line in res.stdout.decode("utf-8").strip().split("\n"):
    line = line.strip()
    print(line)
    if line.startswith("*"):
        branch = line[1:].strip()
        print(branch)