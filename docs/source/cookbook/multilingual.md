# Multilingual Metadata & Internationalization (i18n)

FAIR Data JSON Schema has **native, first-class support for multilingual metadata** across all human-readable titles, labels, descriptions, units, and concepts.

---

## 1. The Dual-Format Rule (`i18nString` & `i18nText`)

Every human-readable text annotation in FAIR Data JSON Schema supports **two formats out of the box**:

### Format A: Simple String (Single Language)
When you only need a single language (e.g. English), use a plain literal string:
```json
"fair:label": "Annual Base Salary",
"fair:unitType": "Employee"
```

### Format B: Language Map Object (Multilingual BCP-47 Tags)
When you need to support multiple languages, use a JSON object where keys are standard **[BCP-47 language tags](https://tools.ietf.org/html/bcp47)** (e.g., `en`, `fr`, `es`, `de`, `fr-CA`, `zh-CN`):
```json
"fair:label": {
  "en": "Annual Base Salary",
  "fr": "Salaire de base annuel",
  "es": "Salario base anual"
},
"fair:unitType": {
  "en": "Employee",
  "fr": "Employé",
  "es": "Empleado"
}
```

---

## 2. Keywords Supporting Multilingual Metadata

The following keywords natively accept language maps (`str | dict[str, str]`):

| Scope | Supported Multilingual Keywords |
| :--- | :--- |
| **Dataset Scope** | `title`, `description`, `fair:label`, `fair:description`, `fair:license`, `fair:unitType`, `fair:spatialCoverage`, `fair:universe`, `fair:population` |
| **Property Scope** | `fair:label`, `fair:description`, `fair:measurementUnit`, `fair:classification`, `fair:concept`, `fair:quantity`, `fair:measurementScale` |
| **Coded Values** | `oneOf` element `title` (e.g. `{ "const": 1, "title": { "en": "Active", "fr": "Actif" } }`) |
| **Contributors** | `fair:contributors` item `name`, `type`, and `role` |

---

## 3. Multilingual Markdown Descriptions

`fair:description` supports **multilingual Markdown text** (`i18nText`), allowing rich formatting, lists, and links per language:

```json
{
  "title": {
    "en": "2024 National Health Survey",
    "fr": "Enquête Nationale sur la Santé 2024"
  },
  "fair:description": {
    "en": "Survey covering health indicators across households. **Note**: Excludes institutional residents.",
    "fr": "Enquête couvrant les indicateurs de santé des ménages. **Remarque**: Exclut les résidents en institution."
  }
}
```

---

## 4. Multilingual Coded Values (`oneOf` + `title`)

You can provide localized titles for numeric database codes inside `oneOf` definitions:

```json
"employment_status": {
  "title": {
    "en": "Employment Status",
    "fr": "Statut d'emploi"
  },
  "type": "integer",
  "oneOf": [
    {
      "const": 1,
      "title": { "en": "Full-Time", "fr": "À plein temps", "es": "Tiempo completo" }
    },
    {
      "const": 2,
      "title": { "en": "Part-Time", "fr": "À temps partiel", "es": "Tiempo parcial" }
    }
  ]
}
```

---

## 5. Python SDK Usage (`I18nString`)

In the auto-generated Python SDK, all `i18n` fields are typed as `str | dict[str, str]`:

```python
from models import SchemaNode

node = SchemaNode(
    type="integer",
    fair_label={"en": "Age", "fr": "Âge", "es": "Edad"},
    fair_measurement_unit={"en": "years", "fr": "ans", "es": "años"}
)

# Export to JSON
print(node.model_dump_json(by_alias=True, exclude_none=True))
```

Output:
```json
{
  "type": "integer",
  "fair:label": {
    "en": "Age",
    "fr": "Âge",
    "es": "Edad"
  },
  "fair:measurementUnit": {
    "en": "years",
    "fr": "ans",
    "es": "años"
  }
}
```
