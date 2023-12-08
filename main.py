from git import Repo, Commit
from argparse import ArgumentParser
import os
from graphviz import Digraph


def get_message(commit: Commit) -> str:
    message = '"' + commit.message[:31]
    message = message[:-1]
    if len(commit.message) > 30:
        message += "..."
    message += '"'
    return message


def get_branch(commit: Commit) -> str:
    for branch in repo.references:
        if "/" in str(branch):
            continue
        if commit in repo.iter_commits(rev=branch):
            return str(branch)


parser = ArgumentParser()
parser.add_argument("path", nargs=1, default=os.getcwd())
args = parser.parse_args()
path = args.path[0]

if not (os.path.exists(path) and ".git" in os.listdir(path)):
    print(f"{path} не является директорией или в ней не инициализирован git")
    exit(-1)

repo = Repo(path)
di = Digraph(path, "shows commit history", edge_attr={"color": "#938d87"}, graph_attr={"splines": "ortho"},
             node_attr={"fontcolor": "white", "color": "white", "fontname": "Helvetica", "style": "filled",
                        "shape": "polygon"})
for commit in repo.iter_commits():
    branch = get_branch(commit)
    message = get_message(commit)

    name = f"{str(branch)}\n{str(commit)[:6]}\n{message}"
    di.node(str(commit), name, fillcolor="#cd9f00")
    if commit.parents != tuple():
        for parent in commit.parents:
            di.edge(str(parent), str(commit))
    queue = [[commit.tree, str(commit)]]

    while len(queue) != 0:
        current, parent = queue.pop()
        di.node(str(current), f"{str(current)[:6]}\ntree", fillcolor="#159099")
        di.edge(parent, str(current))

        for blob in current.blobs:
            di.node(str(blob), str(blob)[:6], fillcolor="#ffbe98")
            di.edge(str(current), str(blob), headlabel=blob.name, labelfloat="true", labelfontsize="10")

        for tree in current.trees:
            queue.append([tree, str(current)])

di.render("table.gv", view=True)
