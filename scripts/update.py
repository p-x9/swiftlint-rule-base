import os
import subprocess

repo_path = os.path.dirname(__file__) + "/.."


def get_swiftlint_tags() -> list[str]:
    tags_cp = subprocess.run(
        ["curl https://api.github.com/repos/realm/swiftlint/releases | jq .[].tag_name"],
        capture_output=True,
        text=True,
        shell=True)
    tags: str = tags_cp.stdout
    tags = tags.split("\n")
    tags = list(map(lambda tag: tag[1:-1], tags))
    tags = tags[:-1]
    tags.reverse()

    return tags[:-1]

def get_tags(repo_root: str) -> list[str]:
    current_dir = os.getcwd()
    os.chdir(repo_root)

    tags_cp = subprocess.run(
        ["git", "tag", "--list", "--sort=v:refname"],
        capture_output=True,
        text=True)
    tags: str = tags_cp.stdout
    tags = tags.split("\n")
    tags = tags[:-1]

    os.chdir(current_dir)

    return tags


os.chdir(repo_path)

swiftlint_tags = get_swiftlint_tags()
own_latest_tag = get_tags(repo_path)[-1]

if swiftlint_tags[-1] == own_latest_tag:
    subprocess.run(["echo", f"up to date"])
    exit(0)

index = swiftlint_tags.index(own_latest_tag)


for tag in swiftlint_tags[index+1:]:
    if "rc" in tag:
        print(f"skip: {tag}")
    else:
        print(f"new tag: {tag}")
        subprocess.call(["./scripts/generate_base.sh", tag])
