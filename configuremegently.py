#!/usr/bin/python
import subprocess, sys, json, os
reload(sys)
sys.setdefaultencoding("utf-8")
from jinja2 import Template

if __name__ == "__main__":
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
