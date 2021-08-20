#!/usr/bin/env python3

from invoke import task, call

# references:
# invoke documentation http://docs.pyinvoke.org/en/stable/index.html
# invoke tutorial: https://www.youtube.com/watch?v=fqS2TBcxoeA
# below some dummy tasks created with invoke

# Example 1
# Usage: $invoke linter
from pylint import epylint as lint  # v1
from pylint.lint import Run  # v2


@task(name="linter")
def linter(c):
    # Run(['utils.py', '--errors-only'])  # v2

    ARGS = ["-r", "n", "--rcfile=rcpylint", "return_std=True"]  # v1
    (pylint_stdout, pylint_stderr) = lint.py_run('utils.py', ARGS)  # v1
    print(pylint_stdout.getvalue())
    # print(pylint_stderr.getvalue())


# Example 1
# Usage: $invoke webopener --url http://python.org


@task(name="webopener")
def openwebpage(c, url=None):
    if url:
        c.run(f"xdg-open {url}")
    else:
        print("Need an url to run!")

# Example 2
# Chained tasks. Usage: $invoke secondstep


@task
def firststep(c):
    print("Step 1")


@task
def thirdstep(c, name="Default!"):
    print(f"Step 3: argument name = {name}")


@task(pre=[firststep],
      post=[call(thirdstep, name="Chained!")])
def secondstep(c):
    print("Step 2")

# Example 3
# Usage: $invoke gitter --name repo --commit "commit message"


@task(name="gitter")
def commitrepo(c, name=None, commit="Default commit message"):
    if not name:
        print("please specify a repository name to commit to")
    else:
        c.run(
            r'cd /home/mhered/{name} && git commit -a -m "{commit}"'.format(name=name, commit=commit))
        c.run(r'cd /home/mhered/{name} && git push -u origin main'.format(name=name))
