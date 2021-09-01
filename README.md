# NetWorth

Project for the [Agile development course](https://jj.github.io/curso-tdd)

The template contains the bare minimum needed to start a project, including a
GitHub action that checks the presence of certain files, a folder for tests and
another for documentation.

NetWorth is a personalizable web app to automate the collection of updated information
from different sources (bank accounts, pensions, funds, stock, crypto, real state, etc)
to generate estimates of net worth over time.

MVP solution ("solución") chosen will be the modules (classes and methods) required to manage a
portfolio of assets and a basic dashboard. See details of the proposed roadmap in the [Roadmap Wiki page](https://github.com/team-mhered/NetWorth/wiki/Roadmap)

# Instructions
* `$ invoke check` to run linter on all files in `/src/` and `/tests/` folders
* `$ invoke test` to run the complete test suite (simply calls `python3 -m run_tests`)


# Dependencies
* [logging](https://docs.python.org/3/howto/logging.html): for logging
* [uuid](https://docs.python.org/3/library/uuid.html): for unique identification of items
* [invoke](http://www.pyinvoke.org/): task runner
* [pylint](https://www.pylint.org/): linter


For details on other dependencies currently under consideration check the [Dependencies Wiki page](https://github.com/team-mhered/NetWorth/wiki/Dependencies)

# Release history
| Release | Description                      | Date       |
| ------- | -------------------------------- | ---------- |
| v0.0.1  | First Release.                   | 10.08.2021 |
| v1.0.1  | [Personas](./personas.md) defined.   | 12.08.2021 |
| v2.0.1  | [Kanban](https://github.com/team-mhered/dummy-project/projects/1) and [Wiki](https://github.com/team-mhered/dummy-project/wiki) added. | 16.08.2021    |
| v3.0.1  | User Stories. Close #9.          | 17.08.2021 |
| v4.0.2  | Services.                        | 18.08.2021 |
| v9.0.1  | Roadmap, Exceptions, Task runner.| 19.08.2021 |
| v9.0.2  | Configure linter.                | 20.08.2021 |

# Authors

| Github Nick                                 | Name                  |
| ------------------------------------------- | --------------------- |
| [mhered](https://github.com/mhered)         | Manuel Heredia        |
| [other-mhered](https://github.com/mhered)  | not Manuel Heredia    |
