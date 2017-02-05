#!/usr/bin/python
import subprocess
import sys
import json
import os
reload(sys)
sys.setdefaultencoding("utf-8")
from jinja2 import Template


def parse_output(proc):
    for line in iter(proc.stdout.readline, ''):
        if "nothing to commit, working directory clean" in line:
            return "clean"
        if "modified: " in line:
            return "dirty"
        if "Your branch is ahead of" in line:
            return "unpushed"
    return None


if __name__ == "__main__":
    proc = subprocess.Popen(
        ['git', 'status'], cwd="dotfiles/", stdout=subprocess.PIPE)
    sys.stdout.flush()
    git_status = parse_output(proc)
    if git_status == "clean":
        subprocess.call(["git", "pull"], cwd="dotfiles")
        with open("paths.txt", "r") as paths, open("vars.json", "r") as varsfile:
            files = paths.read().split("\n")[:-1]
            varsdict = json.loads(varsfile.read())
            for filename in files:
                with open("dotfiles/" + filename.split("/")[-1]) as dotfile:
                    template = Template(dotfile.read())
                    localfilecontent = template.render(varsdict)
                    with open(os.path.expanduser(filename), "w") as localfile:
                        localfile.write(localfilecontent)
                print "written " + filename
    elif git_status == "dirty":
        subprocess.call(["git", "add", "--all"], cwd="dotfiles/")
        subprocess.call(["git", "commit", "-mconfiguredgently"], cwd="dotfiles/")
        subprocess.call(["git", "push", "origin", "master"], cwd="dotfiles/")
    elif git_status == "unpushed":
        subprocess.call(["git", "push", "origin", "master"], cwd="dotfiles/")
    else:
        print "git status failed, unknown status"
