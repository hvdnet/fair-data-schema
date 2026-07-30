# Coded Values: From Enums to FAIR Domains

This explains by example how to handle categorical data (code lists, classifications, or response domains) using JSON Schema, evolving from simple technical validation to rich FAIR metadata.

See the companion schema file: {download}`../../../examples/enum-to-fair-coded-values.json`

:::{admonition} How-to: Implement Rich Coded Values
:class: tip

1. **Define the Base Type**: Start with `type: string` or `type: integer`.
2. **Use `oneOf`**: Instead of `enum`, use `oneOf` to allow for annotations on each value.
3. **Add Standard Labels**: Use `title` for the default human-readable label.
4. **Add FAIR Labels**: Use `fair:label` for multilingual support (e.g., `{"en": "Yes", "fr": "Oui"}`).
5. **Link to Concepts**: Use `fair:conceptRef` to point to a stable URI (e.g., Wikidata, SKOS).
:::

---

## 1. The Standard `enum` (Validation only)

The most basic way to restrict a value in JSON Schema is the [`enum`](https://json-schema.org/draft/2020-12/json-schema-validation#name-enum) keyword.

```json
{
  "type": "integer",
  "enum": [1, 2, 9]
}
```

**Pros**: extremely simple; natively supported by all tools.
**Cons**: No way to associate human-readable labels (`"Yes"`, `"No"`, `"Did not answer"`) or semantic context with each numeric code.

---

## 2. The Labeled Enum Pattern (Standard JSON Schema)

To associate labels like `"Yes"` or `"Did not answer"` with numerical codes like `1`, `2`, and `9`, we use the [**`oneOf`**](https://json-schema.org/draft/2020-12/json-schema-core#name-oneof) + [**`const`**](https://json-schema.org/draft/2020-12/json-schema-validation#name-const) pattern. This is **100% standard JSON Schema**, requires no extensions, and is natively supported by all standard-compliant JSON Schema validators.

```json
{
  "type": "integer",
  "oneOf": [
    { "const": 1, "title": "Yes" },
    { "const": 2, "title": "No" },
    { "const": 9, "title": "Did not answer" }
  ]
}
```

By using the standard [`title`](https://json-schema.org/draft/2020-12/json-schema-validation#name-title) keyword inside each `oneOf` branch, you create an unambiguous mapping between the stored numeric value and its human-readable representation.

---

## 3. The Shared Response Domain (DRY Principle)

In data stewardship, many variables often share the same "Response Domain" (e.g., several "Yes/No/Did not answer" survey questions). Instead of repeating the `oneOf` logic, you define it once in `$defs` and reference it using `$ref`.

```json
{
  "$defs": {
    "SimpleSharedDomain": {
      "type": "integer",
      "oneOf": [
        { "const": 1, "title": "Yes" },
        { "const": 2, "title": "No" },
        { "const": 9, "title": "Did not answer" }
      ]
    }
  },
  "properties": {
    "satisfied": { "$ref": "#/$defs/SimpleSharedDomain" },
    "completed": { "$ref": "#/$defs/SimpleSharedDomain" }
  }
}
```

This ensures consistency: if you decide to update a label, you only change it in one place, and it updates across all variables.

---

## 4. The FAIR Data Domain (Rich Metadata)

While `title` is great for simple labels, FAIR data requires more depth: multilingual support, semantic pointers, and persistence. The **FAIR Data JSON Schema** dialect extends the `oneOf` pattern with custom keywords.

```json
"oneOf": [
  {
    "const": 1,
    "title": "Yes",
    "fair:label": { "en": "Yes", "fr": "Oui", "de": "Ja" },
    "fair:conceptRef": "https://www.wikidata.org/wiki/Q6452715"
  },
  {
    "const": 2,
    "title": "No",
    "fair:label": { "en": "No", "fr": "Non", "de": "Nein" },
    "fair:conceptRef": "https://www.wikidata.org/wiki/Q1814990"
  },
  {
    "const": 9,
    "title": "Did not answer",
    "fair:label": { "en": "Did not answer", "fr": "Pas de réponse", "de": "Keine Antwort" },
    "fair:sentinel": true
  }
]
```

### Why use FAIR extensions instead of just `title`?

1. **Multilingualism**: Standard `title` is a single string. `fair:label` supports localized objects.
2. **Sentinel Values**: Flag non-response or missing data codes (e.g. `9: Did not answer`) with `"fair:sentinel": true` so data pipelines and AI agents filter them automatically.
3. **Semantic Context**: `fair:conceptRef` links valid codes to global ontology URIs (like Wikidata or SKOS).
4. **Variable Cascade**: This pattern implements a lightweight version of the DDI "Variable Cascade." The shared definition in `$defs` acts as the *Represented Variable*, while the property in `properties` acts as the *Instance Variable*.

---

## 5. External Semantic Mapping (SKOS)

For high-value datasets, the code list is often defined in an external authority or registry using [SKOS](https://www.w3.org/2004/02/skos/) (Simple Knowledge Organization System).

### The "Hybrid" Approach

Crucially, this is a **hybrid approach**. We do not replace the technical validation logic with semantic URIs; we anchor them together.

In each entry, we keep:
- **`const`**: Ensures that data files still validate against the correct codes (e.g., "FR").
- **`title`**: Provides a baseline human label for standard tools.
- **`fair:conceptRef`**: Provides the "semantic bridge" to the official authority URI.

Note that at this stage, we **no longer need `fair:label`** inside the schema. Since each code is mapped to a formal URI, a FAIR-aware application can dynamically retrieve the multilingual labels directly from the authoritative source (the SKOS Concept).

```json
{
  "fair:classification": ["http://data.europa.eu/nuts"],
  "oneOf": [
    {
      "const": "FR",
      "title": "France",
      "fair:conceptRef": "http://data.europa.eu/nuts/code/FR"
    }
  ]
}
```

This mapping allows a FAIR data harvester to:
1.  Discover that the variable follows the **NUTS** classification.
2.  Automatically translate "FR" to "France" in any language supported by the Eurostat registry.
3.  Perform automated data integration with other datasets that also use the NUTS level 0 URIs.

---

## Summary Comparison

| Feature | Standard `enum` | Standard `oneOf` | FAIR Dialect | SKOS Mapping |
| :--- | :---: | :---: | :---: | :---: |
| Value Validation | ✅ | ✅ | ✅ | ✅ |
| Human Labels | ❌ | ✅ (`title`) | ✅ (`fair:label`) | ✅ (External) |
| Shared Definitions | ❌ | ✅ (`$ref`) | ✅ (`$ref`) | ✅ (`$ref`) |
| Multilingual (i18n) | ❌ | ❌ | ✅ | ✅ (External) |
| Semantic Mapping | ❌ | ❌ | ✅ | ✅ (`skos:Concept`) |
| Authority Link | ❌ | ❌ | ❌ | ✅ (`skos:ConceptScheme`) |
| Standard Compatibility| ✅ | ✅ | ✅ (ignored by defaults) | ✅ |

---

## Full Schema Implementation

```{literalinclude} ../../../examples/enum-to-fair-coded-values.json
:language: json
```
