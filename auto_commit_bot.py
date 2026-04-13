import os
import time
import random
import subprocess
import sys


def run_command(command, cwd):
    result = subprocess.run(command, cwd=cwd, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        sys.exit(1)


def get_file_groups():
    groups = []

    print("\nEnter files to commit. Type 'done' to finish a group, 'exit' to finish all.\n")

    while True:
        group = []

        while True:
            file = input("Enter file (or 'done' / 'exit'): ").strip()

            if file.lower() == "exit":
                if group:
                    groups.append(group)
                return groups

            if file.lower() == "done":
                if group:
                    groups.append(group)
                    print(f"✅ Group added: {group}\n")
                break

            group.append(file)


def commit_and_push(repo_path, groups):
    for i, group in enumerate(groups):
        print(f"\n🚀 Processing group {i + 1}: {group}")

        # Add files
        files_str = " ".join(group)
        run_command(f"git add {files_str}", repo_path)

        # Commit
        commit_msg = f"Add files: {', '.join(group)}"
        run_command(f'git commit -m "{commit_msg}"', repo_path)

        # Push
        run_command("git push", repo_path)

        # Delay (except last commit)
        if i < len(groups) - 1:
            delay = random.randint(300, 720)  # 5 to 12 minutes
            print(f"⏳ Waiting {delay // 60} min {delay % 60} sec before next commit...\n")
            time.sleep(delay)


def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_commit_bot.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.isdir(repo_path):
        print("❌ Invalid folder path")
        sys.exit(1)

    print(f"📁 Using repository: {repo_path}")

    groups = get_file_groups()

    if not groups:
        print("⚠️ No file groups provided.")
        sys.exit(0)

    print(f"\n📦 Total groups: {len(groups)}")
    commit_and_push(repo_path, groups)


if __name__ == "__main__":
    main()
