import os
import subprocess

repo_path = os.path.dirname(__file__) + "/.."

swiftlint_path = f"{repo_path}/SwiftLint"


def update_swiftlint():
    current_dir = os.getcwd()

    if os.path.exists(swiftlint_path):
        os.chdir(swiftlint_path)
        subprocess.run(["git", "pull"])
        os.chdir(current_dir)
    else:
        subprocess.run(["git", "clone", "https://github.com/realm/SwiftLint.git"])


def get_tags(repo_root: str) -> list[str]:
    current_dir = os.getcwd()
    os.chdir(repo_root)

    tags_cp = subprocess.run(
        ["git", "tag", "--list", "--sort=v:refname"], capture_output=True,
        text=True)
    tags: str = tags_cp.stdout
    tags = tags.split("\n")

    os.chdir(current_dir)

    return tags[:-1]


os.chdir(repo_path)

update_swiftlint()

swiftlint_tags = get_tags(swiftlint_path)
own_latest_tag = get_tags(repo_path)[-1]

if swiftlint_tags[-1] == own_latest_tag:
    subprocess.run(["echo", f"up to date"])
    exit(0)

index = swiftlint_tags.index(own_latest_tag)


for tag in swiftlint_tags[index+1:]:
    print(f"new tag: {tag}")
    subprocess.call(["./scripts/generate_base.sh", tag])
