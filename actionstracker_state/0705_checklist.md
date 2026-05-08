# Initial Project Setup Checklist

## 01 Project Repository

- [ ] Create local project folder
- [ ] Initialize Git repository
- [ ] Create GitHub repository
- [ ] Add remote origin
- [ ] Verify remote with `git remote -v`

Commands:

```powershell
git init
git remote add origin YOUR_REPOSITORY_URL
git remote -v
```

---

# 02 Virtual Environment

- [ ] Create virtual environment
- [ ] Activate virtual environment
- [ ] Verify Python interpreter

Commands:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

---

# 03 Development Dependencies

- [ ] Install pytest
- [ ] Install black
- [ ] Install isort
- [ ] Install ruff
- [ ] Freeze dependencies

Commands:

```powershell
pip install pytest black isort ruff
pip freeze > requirements.txt
```

---

# 04 Core Project Files

- [ ] Create README.md
- [ ] Create .gitignore
- [ ] Create pyproject.toml
- [ ] Create core_workflow.md
- [ ] Create docs/dependencies.md

---

# 05 VSCode Setup

- [ ] Create `.vscode/`
- [ ] Create `settings.json`
- [ ] Create `extensions.json`
- [ ] Select `.venv` interpreter in VSCode

Recommended extensions:

- Python
- Pylance
- Ruff

---

# 06 Data Safety Structure

- [ ] Create `data/raw`
- [ ] Create `data/processed`
- [ ] Add `.gitkeep`
- [ ] Verify `.gitignore` excludes datasets

Structure:

```text
data/
├── raw/
└── processed/
```

---

# 07 Base Project Structure

- [ ] Create `data_processor/`
- [ ] Create adapters/
- [ ] Create core/
- [ ] Create inference/
- [ ] Create cleaners/
- [ ] Create validators/
- [ ] Create transformers/
- [ ] Create exporters/
- [ ] Create tests/
- [ ] Create scripts/
- [ ] Add `__init__.py` files

---

# 08 Initial Git Commit

- [ ] Run formatter
- [ ] Run linter
- [ ] Stage files
- [ ] Commit initial setup
- [ ] Push to GitHub

Commands:

```powershell
ruff check .
black .
isort .

git add .
git commit -m "Initial project setup"

git branch -M main
git push -u origin main
```

---

# 09 Recommended Next Step

After setup is complete:

Development order:

1. `core/table.py`
2. `core/schema.py`
3. `adapters/base_adapter.py`
4. `csv_adapter.py`
5. `pipeline.py`
6. First end-to-end CSV cleaning flow

---

# 10 Architecture Rules

- [ ] One internal canonical table model
- [ ] No format-specific cleaning logic
- [ ] Keep modules small
- [ ] One responsibility per file
- [ ] Add tests early
- [ ] Avoid unnecessary dependencies
- [ ] Prefer standard library when possible
- [ ] Never commit sensitive datasets

---

# 11 Daily Workflow

Startup:

```powershell
.\.venv\Scripts\Activate.ps1
git pull
```

Before commit:

```powershell
ruff check .
black .
isort .
pytest
```

Shutdown:

```powershell
git add .
git commit -m "Describe changes"
git push
deactivate
```