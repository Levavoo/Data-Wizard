| Purpose               | Tool                                                            |
| --------------------- | --------------------------------------------------------------- |
| Language              | Python                                                          |
| IDE                   | [VS Code](https://code.visualstudio.com?utm_source=chatgpt.com) |
| Version control       | [Git](https://git-scm.com?utm_source=chatgpt.com)               |
| Virtual env           | built-in `venv`                                                 |
| Testing               | `pytest`                                                        |
| Formatting            | `black`                                                         |
| Import sorting        | `isort`                                                         |
| Linting               | `ruff`                                                          |
| Type checking         | `mypy` later                                                    |
| Dependency management | `pip` + `requirements.txt` initially                            |

py -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install pytest black isort ruff #instal inital tooling

pip freeze > requirements.txt # freeze dependencies 

#workspace settings
mkdir .vscode

New-Item .vscode\settings.json
New-Item .vscode\extensions.json

pytest # run test
 
 # check formatting
ruff check .
black .
isort .

# set Git
git remote add Levavoo https://github.com/Levavoo/Data-Wizard.git

# Git flow
git status

# stage changes:
git add .

# Commit 
git commit -m "Add CSV type inference"

# git push

git push

git push --set-upstream Levavoo master