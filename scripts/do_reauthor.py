import os
import subprocess

os.chdir('/Users/snehal/Documents/agent-cache-bench')
env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "kshirsagarps"
env["GIT_AUTHOR_EMAIL"] = "pratyush.kshirsagar@gmail.com"
env["GIT_COMMITTER_NAME"] = "kshirsagarps"
env["GIT_COMMITTER_EMAIL"] = "pratyush.kshirsagar@gmail.com"

# Clean up lock files
for lk in [".git/index.lock", ".git/config.lock"]:
    if os.path.exists(lk):
        try:
            os.remove(lk)
        except Exception:
            pass

# Set local git config directly in .git/config
config_content = """[core]
\trepositoryformatversion = 0
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
\tignorecase = true
\tprecomposeunicode = true
[user]
\tname = kshirsagarps
\temail = pratyush.kshirsagar@gmail.com
[remote "origin"]
\turl = git@github.com:kshirsagarps/agent-cache-bench.git
\tfetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
\tremote = origin
\tmerge = refs/heads/main
"""
with open(".git/config", "w") as f:
    f.write(config_content)

# Step 1: checkout temp branch
subprocess.run(["git", "checkout", "-b", "temp_work"], check=True)

# Step 2: delete old main
subprocess.run(["git", "branch", "-D", "main"], check=True)

# Step 3: create new orphan main
subprocess.run(["git", "checkout", "--orphan", "main"], check=True)

# Step 4: add all files
subprocess.run(["git", "add", "-A"], check=True)

# Step 5: commit as kshirsagarps
subprocess.run([
    "git", "commit",
    "-m", "AgentCacheBench: A Benchmark and Measurement Framework for Realized KV-Cache Reuse in Stateful LLM Agents"
], env=env, check=True)

# Step 6: delete temp branch
subprocess.run(["git", "branch", "-D", "temp_work"], check=True)

print("SUCCESS_CLEAN_REAUTHOR_KSHIRSAGARPS")
