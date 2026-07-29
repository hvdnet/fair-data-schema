# Validating Data with Standard JSON Schema Tools

Because FAIR Data JSON Schema relies on standard **JSON Schema Draft 2020-12** extension mechanisms (`$vocabulary`, custom dialect, metadata annotations), **you can validate your data using any standard JSON Schema validator across any programming language out of the box.**

Standard validators perform technical data validation and treat `fair:` keywords as transparent metadata annotations.

---

## 1. Python (`jsonschema` package)

Standard Python `jsonschema` validates FAIR-annotated schemas without requiring any plugins.

### Installation
```bash
pip install jsonschema
```

### Usage
```python
import json
from jsonschema import validate, ValidationError

# Load schema and data instance
with open("examples/simple-dataset.json") as f:
    schema = json.load(f)

with open("examples/simple-dataset.data.json") as f:
    data = json.load(f)

# Validate data instance against schema
try:
    validate(instance=data, schema=schema)
    print("✓ Data is valid!")
except ValidationError as e:
    print(f"✗ Validation error: {e.message}")
    print(f"  Path: {list(e.absolute_path)}")
```

---

## 2. JavaScript / Node.js (`ajv` package)

`Ajv` is the most popular JSON Schema validator in the JavaScript and TypeScript ecosystem. Use the Draft 2020-12 build (`ajv/dist/2020`).

### Installation
```bash
npm install ajv
```

### Usage
```javascript
const Ajv2020 = require("ajv/dist/2020");
const fs = require("fs");

const ajv = new Ajv2020();

const schema = JSON.parse(fs.readFileSync("examples/simple-dataset.json", "utf8"));
const data = JSON.parse(fs.readFileSync("examples/simple-dataset.data.json", "utf8"));

const validate = ajv.compile(schema);
const valid = validate(data);

if (valid) {
  console.log("✓ Data is valid!");
} else {
  console.log("✗ Validation errors:", validate.errors);
}
```

---

## 3. Command-Line Validation (CLI)

### Option A: `fair-data-schema` CLI
Use the built-in FAIR CLI for dialect-aware validation and schema checking:

```bash
fair-data-schema validate examples/simple-dataset.json examples/simple-dataset.data.json
```

### Option B: Standard `check-jsonschema` CLI
Use the generic `check-jsonschema` tool used in CI/CD pipelines:

```bash
pip install check-jsonschema

check-jsonschema --schemafile examples/simple-dataset.json examples/simple-dataset.data.json
```

---

## 4. Python SDK (`fair_data_schema` package)

The `fair_data_schema` Python package wraps `jsonschema` with offline local URI resolution so `$ref` pointers resolve without needing an internet connection:

```python
from pathlib import Path
from fair_data_schema import validator

schema_path = Path("examples/simple-dataset.json")
instance_path = Path("examples/simple-dataset.data.json")

errors = validator.validate_file(schema_path, instance_path)

if not errors:
    print("✓ Data is valid!")
else:
    for err in errors:
        print(f"✗ {err.message} at {list(err.absolute_path)}")
```

---

## 5. Summary Matrix across Languages

| Language / Tool | Library | Draft 2020-12 Support | Out-of-the-Box FAIR Support |
| :--- | :--- | :--- | :--- |
| **Python** | `jsonschema` | Native | ✅ 100% Validated |
| **JavaScript / TS** | `ajv` (`ajv/dist/2020`) | Native | ✅ 100% Validated |
| **Go** | `santhosh-tekuri/jsonschema/v5` | Native | ✅ 100% Validated |
| **Rust** | `boon` / `jsonschema` | Native | ✅ 100% Validated |
| **Java** | `networknt/json-schema-validator` | Native | ✅ 100% Validated |
| **C# / .NET** | `JsonSchema.Net` | Native | ✅ 100% Validated |
| **CLI** | `check-jsonschema` | Native | ✅ 100% Validated |
