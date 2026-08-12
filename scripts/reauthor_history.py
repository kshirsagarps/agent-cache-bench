import os
import subprocess

def reauthor_all():
    os.chdir('/Users/snehal/Documents/agent-cache-bench')
    
    # Configure git config
    subprocess.run(["git", "config", "user.name", "kshirsagarps"], check=True)
    subprocess.run(["git", "config", "user.email", "pratyush.kshirsagar@gmail.com"], check=True)
    
    # Remove any lock files
    for lk in [".git/index.lock", ".git/config.lock", ".git/refs/heads/main.lock"]:
        if os.path.exists(lk):
            try:
                os.remove(lk)
            except Exception:
                pass

    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "kshirsagarps"
    env["GIT_AUTHOR_EMAIL"] = "pratyush.kshirsagar@gmail.com"
    env["GIT_COMMITTER_NAME"] = "kshirsagarps"
    env["GIT_COMMITTER_EMAIL"] = "pratyush.kshirsagar@gmail.com"

    # Soft reset to root commit to re-commit cleanly with kshirsagarps author
    subprocess.run(["git", "reset", "--soft", "6c69e0a~1"], check=False)
    # If soft reset to 6c69e0a~1 is root:
    subprocess.run(["git", "update-ref", "-d", "HEAD"], check=False)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run([
        "git", "commit",
        "--author=kshirsagarps <pratyush.kshirsagar@gmail.com>",
        "-m", "AgentCacheBench: A Benchmark and Measurement Framework for Realized KV-Cache Reuse in Stateful LLM Agents"
    ], env=env, check=True)

    print("REAUTHOR_ALL_SUCCESS")

if __name__ == "__main__":
    reauthor_all()
