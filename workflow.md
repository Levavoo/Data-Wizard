1. Read relevant files
2. Identify exact scope
3. Modify only necessary code
4. Add/update matching .md docs
5. Run available tests or lightweight checks
6. Summarize changed behavior
7. Commit

Commit message convention

Recommended:

<area>: <short action>

# Local module documentation

Lives near the code:

data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md

Purpose:

what this file does
what it must not do
main functions/classes
inputs
outputs
developer notes

# Plan/stage documentation

Lives in:

docs/

Purpose:

development plan
stage checklist
architectural decisions
migration notes

Example:

docs/0805_improvement_plan_csv.md
docs/0805_completion_report_csv.md
docs/0900_constraint_engine_plan.md


# Proposed official workflow


1. Active plan selected
   docs/0805_improvement_plan_csv.md

2. Create/checkout plan branch
   improvement/0805-csv-foundation

3. Inspect repository and plan

4. Convert plan into checklist

5. For each checklist item:
   a. inspect relevant files
   b. implement one focused change
   c. update/add matching .md docs
   d. run checks/tests
   e. update plan status
   f. commit

6. When all checklist items are done:
   a. create completion report
   b. final review
   c. merge branch
   d. create next improvement plan