import os
import subprocess

def reauthor():
    cwd = '/Users/snehal/Documents/agent-cache-bench'
    os.chdir(cwd)
    
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "kshirsagarps"
    env["GIT_AUTHOR_EMAIL"] = "pratyush.kshirsagar@gmail.com"
    env["GIT_COMMITTER_NAME"] = "kshirsagarps"
    env["GIT_COMMITTER_EMAIL"] = "pratyush.kshirsagar@gmail.com"

    subprocess.run(["git", "config", "--local", "user.name", "kshirsagarps"], check=True)
    subprocess.run(["git", "config", "--local", "user.email", "pratyush.kshirsagar@gmail.com"], check=True)

    # Clean up lock files
    for lk in [".git/index.lock", ".git/config.lock"]:
        if os.path.exists(os.path.join(cwd, lk)):
            os.remove(os.path.join(cwd, lk))

    # Switch to temp branch, recreate orphan main
    subprocess.run(["git", "checkout", "-B", "temp_work"], check=True)
    subprocess.run(["git", "branch", "-D", "main"], check=False)
    subprocess.run(["git", "checkout", "--orphan", "main"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run([
        "git", "commit",
        "-m", "AgentCacheBench: A Benchmark and Measurement Framework for Realized KV-Cache Reuse in Stateful LLM Agents"
    ], env=env, check=True)
    subprocess.run(["git", "branch", "-D", "temp_work"], check=False)
    
    print("REAUTHOR SUCCESSFUL!")

if __name__ == "__main__":
    reauthor()
