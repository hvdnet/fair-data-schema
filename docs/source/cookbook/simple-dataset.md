# Tier 1 Simple Dataset Example

This recipe demonstrates how to annotate a **simple, single-table dataset** using **Tier 1 Essential Properties**.

With minimal effort and zero steep learning curve, you can make any basic dataset self-documenting, standards-compliant, and AI-ready out of the box.

- See the companion schema files: {download}`../../../examples/simple-dataset.json` and {download}`../../../examples/simple-dataset.data.json`

:::{admonition} How-to: Annotate a Simple Dataset
:class: tip

1. **Root Metadata**: Add `title`, `description`, `fair:license`/`fair:licenseRef`, and `fair:contributors` at the schema root.
2. **Define Unit Type**: Use `fair:unitType` to specify what entity 1 row represents (e.g., `"Weather Station Observation"`).
3. **Annotate Fields**: Add `fair:measurementUnit`/`Ref` for physical units, `fair:conceptRef` for human meaning, and `oneOf` + `const` + `title` for self-documenting status codes.
4. **Validation**: Validate using `fair-data-schema validate examples/simple-dataset.json examples/simple-dataset.data.json`.
:::

---

## The Story: Weather Station Observations

In this example, we have a flat table (array of objects) containing weather station observations: `station_id`, `temperature`, and operational `status`.

Without metadata, a machine or developer looking at raw JSON wouldn't know:
- What entity 1 row represents.
- What unit `temperature` is in (Celsius, Fahrenheit, Kelvin?).
- What numeric status codes like `1`, `2`, or `3` mean.

By adding Tier 1 `fair:` annotations directly into a standard JSON Schema, we answer all of these questions effortlessly.

---

## 1. Dataset-Level Metadata

At the root of the schema, we define the dataset title, license, contributors, and the row entity (`fair:unitType`):

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema/dev",
  "$id": "https://highvaluedata.net/fair-data-schema/dev/examples/simple-dataset",
  "title": "Weather Station Observations (Tier 1 Simple Dataset)",
  "description": "A simple flat dataset containing daily temperature and status readings across weather stations.",
  "fair:resourceType": "dataset",
  "fair:license": "CC-BY-4.0",
  "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
  "fair:unitType": "Weather Station Observation",
  "fair:contributors": [
    {
      "name": "Global Meteorological Network",
      "role": "Producer",
      "type": "Organization",
      "contributorRef": "https://example.org/orgs/gmn"
    }
  ]
}
```

### Key Takeaways
- **`fair:unitType`**: Explains in plain English what 1 row in the table represents (`"Weather Station Observation"`).
- **`fair:license` & `fair:licenseRef`**: Follows the **Plain String vs. Machine Web Link (`Ref`) Rule** to document legal reuse rights.

---

## 2. Field-Level Metadata

Inside the property definitions, we annotate the fields with units, concepts, and self-documenting coded values:

```json
"properties": {
  "station_id": {
    "title": "Station Identifier",
    "type": "string",
    "fair:conceptRef": "https://example.org/concepts/station-id"
  },
  "temperature": {
    "title": "Air Temperature",
    "type": "number",
    "fair:measurementUnit": "Celsius",
    "fair:measurementUnitRef": "http://www.wikidata.org/entity/Q52261"
  },
  "status": {
    "title": "Operational Status",
    "type": "integer",
    "fair:classification": "Station Status Codes",
    "oneOf": [
      { "const": 1, "title": "Active" },
      { "const": 2, "title": "Maintenance" },
      { "const": 3, "title": "Offline" }
    ]
  }
}
```

### Key Takeaways
- **`fair:measurementUnit` & `Ref`**: Disambiguates numbers (`21.5`) as **Celsius** with a Wikidata URI.
- **Self-Documenting Coded Values (`oneOf` + `const` + `title`)**: Converts raw status integers (`1`, `2`, `3`) into human-readable titles (`"Active"`, `"Maintenance"`, `"Offline"`).

---

## 3. Full Schema & Instance

```{literalinclude} ../../../examples/simple-dataset.json
:language: json
:caption: The Simple Dataset Schema
```

### Example Data Instance

```{literalinclude} ../../../examples/simple-dataset.data.json
:language: json
:caption: Valid data instance for this dataset
```

---

## Next Steps: Advanced & Hierarchical Datasets (Tier 2)

For multi-table datasets (like nested Census files with households and persons) or deep variable lineage cascades, see the advanced recipe:
- 📖 [Hierarchical Data Products Recipe](complex-data-product.md)
