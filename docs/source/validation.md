# Validation Guide — Validating JSON & YAML Datasets

> **How to validate dataset instances (JSON or YAML) against FAIR Data JSON Schemas using standard tools, command-line utilities, Python, JavaScript, and CI/CD pipelines.**

---

## Zero New Tools to Learn

Because FAIR Data JSON Schema relies on standard JSON Schema extension mechanisms (Draft 2020-12), **standard JSON Schema validators automatically ignore unknown `fair:` annotation keywords during validation**.

This means you can validate dataset payloads (whether formatted in JSON or YAML) using **100% off-the-shelf, standard-compliant JSON Schema tooling** in any language or environment—with **zero custom plugins or proprietary validators required**.

---

## 1. Command Line (CLI)

### Option A: `check-jsonschema` (Python CLI)
[`check-jsonschema`](https://github.com/python-jsonschema/check-jsonschema) is a popular, fast CLI utility that natively supports validating both **JSON and YAML** instance files against local or remote JSON schemas.

```bash
# Install check-jsonschema
pip install check-jsonschema

# Validate a JSON dataset instance
check-jsonschema --schema path/to/schema.json dataset.json

# Validate a YAML dataset instance
check-jsonschema --schema path/to/schema.json dataset.yaml
```

### Option B: `ajv-cli` (Node.js CLI)
[`ajv-cli`](https://www.npmjs.com/package/ajv-cli) is the command-line interface for Ajv, the high-performance JavaScript JSON Schema validator.

```bash
# Install globally or locally via npm
npm install -g ajv-cli ajv-formats

# Validate JSON dataset
ajv validate -s path/to/schema.json -d dataset.json --spec=draft2020-12
```

### Option C: `fair-data-schema` CLI (Included SDK)
The FAIR Data JSON Schema Python package includes a built-in CLI command:

```bash
# Validate using local schema registry resolution
fair-data-schema validate path/to/schema.json dataset.json
```

---

## 2. REST API Validation (`/v1/validate` & `/v1/lint`)

When the API server is running (`fair-data-schema serve`), you can perform validation via HTTP POST requests:

```bash
curl -X POST http://localhost:8000/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "$schema": "https://highvaluedata.net/fair-data-schema/dev",
      "title": "My Dataset"
    }
  }'
```

To enable **strict mode** (failing on misspelled or unknown `fair:` keywords):

```bash
curl -X POST "http://localhost:8000/v1/validate?strict=true" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### Semantic Quality Linting (`/v1/lint`)

```bash
curl -X POST http://localhost:8000/v1/lint \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

---

## 2. Python

### Option A: Standard `jsonschema` Library (JSON & YAML)
You can use the standard Python [`jsonschema`](https://python-jsonschema.readthedocs.io/) package with [`PyYAML`](https://pyyaml.org/) to validate both JSON and YAML data:

```python
import json
import yaml
from jsonschema import validate

# 1. Load your FAIR Data JSON Schema
with open("schema.json") as f:
    schema = json.load(f)

# 2. Load JSON dataset instance
with open("dataset.json") as f:
    data_json = json.load(f)

# Validate JSON
validate(instance=data_json, schema=schema)
print("✓ JSON dataset is valid!")

# 3. Load YAML dataset instance
with open("dataset.yaml") as f:
    data_yaml = yaml.safe_load(f)

# Validate YAML
validate(instance=data_yaml, schema=schema)
print("✓ YAML dataset is valid!")
```

### Option B: `fair_data_schema.validator` (With Offline Meta-Schema Registry)
To ensure offline resolution of local `$schema` URIs without network calls:

```python
from fair_data_schema.validator import FAIRSchemaValidator

validator = FAIRSchemaValidator("path/to/schema.json")

# Validate instance dictionary (from JSON or YAML)
errors = validator.validate_instance({"temp": 21.5, "quality_flag": 0})
if not errors:
    print("✓ Dataset is valid!")
else:
    for err in errors:
        print(f"Validation Error: {err.message}")
```

---

## 3. JavaScript / Node.js

Using [Ajv](https://ajv.js.org/) (Draft 2020-12) and `yaml` in Node.js or browser environments:

```javascript
import Ajv2020 from "ajv/dist/2020.js";
import fs from "fs";
import yaml from "yaml";

const ajv = new Ajv2020({ strict: false });

// 1. Read Schema
const schema = JSON.parse(fs.readFileSync("schema.json", "utf8"));
const validate = ajv.compile(schema);

// 2. Validate JSON Data
const jsonData = JSON.parse(fs.readFileSync("dataset.json", "utf8"));
if (validate(jsonData)) {
  console.log("✓ JSON dataset is valid!");
} else {
  console.error("Validation errors:", validate.errors);
}

// 3. Validate YAML Data
const yamlData = yaml.parse(fs.readFileSync("dataset.yaml", "utf8"));
if (validate(yamlData)) {
  console.log("✓ YAML dataset is valid!");
}
```

---

## 4. Other Ecosystems (Rust, Go, Java)

- **Go**: Use [`santhosh-tekuri/jsonschema`](https://github.com/santhosh-tekuri/jsonschema) or [`sanitizers/go-jsonschema`](https://github.com/sanitizers/go-jsonschema). Unmarshal YAML via `gopkg.in/yaml.v3` before validation.
- **Rust**: Use [`jsonschema-rs`](https://github.com/Stranger6667/jsonschema-rs) or [`boon`](https://github.com/santhosh-tekuri/boon).
- **Java**: Use [`networknt/json-schema-validator`](https://github.com/networknt/json-schema-validator) (supports Draft 2020-12 and YAML input).

---

## 5. CI/CD Integration (GitHub Actions)

Automatically validate dataset files (JSON and YAML) on every commit or pull request using GitHub Actions:

```yaml
name: Validate FAIR Datasets

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install check-jsonschema
        run: pip install check-jsonschema

      - name: Validate Datasets against FAIR Schema
        run: |
          check-jsonschema --schema schemas/my-schema.json data/**/*.json
          check-jsonschema --schema schemas/my-schema.json data/**/*.yaml
```

---

## Summary Matrix

| Platform | Tool / Library | JSON | YAML | Standard Draft 2020-12 |
|---|---|:---:|:---:|:---:|
| **CLI** | `check-jsonschema` | ✓ | ✓ | ✓ |
| **CLI** | `ajv-cli` | ✓ | | ✓ |
| **CLI** | `fair-data-schema validate` | ✓ | ✓ | ✓ |
| **Python** | `jsonschema` + `pyyaml` | ✓ | ✓ | ✓ |
| **Python** | `fair_data_schema.validator` | ✓ | ✓ | ✓ |
| **Node.js** | `ajv` + `yaml` | ✓ | ✓ | ✓ |
| **CI/CD** | GitHub Actions (`check-jsonschema`) | ✓ | ✓ | ✓ |
