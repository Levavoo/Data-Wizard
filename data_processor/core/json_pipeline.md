# JSON Pipeline

## Purpose

Runs supported JSON input through the existing Data Wizard processing layers.

---

## Entry Point

```text
run_json_pipeline()
```

---

## Flow

```text
JsonAdapter
cleaning
type inference
type casting
schema metadata
validation
quality report
diagnostic bundle
pipeline status
CSV export
optional JSON report
optional HTML report
optional quarantine exports
```

---

## Notes

The JSON pipeline is separate from the CSV pipeline to avoid destabilizing CSV behavior.
