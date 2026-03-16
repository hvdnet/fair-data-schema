# Mechanism 1: Custom Annotations

Custom annotations are the **simplest** and most backward-compatible extension mechanism. Standard JSON Schema validators silently ignore keywords they do not recognise, passing them through as *annotations* — named metadata attached to a schema location.

The FAIR project uses the `fair:` prefix for all annotation keywords. A dataset schema using `fair:concept`, `fair:unit`, etc. validates without error on any standard Draft 2020-12 validator. FAIR-aware tools (such as the `fair-data-schema` CLI) can then read and act on those annotation values.

## Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "population": {
      "type": "integer",
      "fair:conceptRef": "https://www.wikidata.org/wiki/Q1203",
      "fair:concept": { "en": "Population", "fr": "Population" },
      "fair:unitRef": "http://qudt.org/vocab/unit/UNITS",
      "fair:licenseRef": "https://creativecommons.org/licenses/by/4.0/"
    }
  }
}
```

## Available Keywords

See {download}`schemas/vocab/annotations/SPEC.md <../../../schemas/vocab/annotations/SPEC.md>` for the full list.

| Keyword | Type | Description |
|---|---|---|
| `fair:concept` | string / object | Human-readable name of the semantic concept (Literal) |
| `fair:conceptRef` | URI / CURIE | URI or CURIE of the semantic concept (Reference) |
| `fair:label` | string / object | Human-readable label for the property in context |
| `fair:description` | string / object | Rich-text description (Markdown supported) |
| `fair:instanceVariableRef` | URI / CURIE | Link to a dataset-specific variable implementation |
| `fair:representedVariableRef` | URI / CURIE | Link to a shared measurement definition |
| `fair:conceptualVariableRef` | URI / CURIE | Link to a high-level semantic phenomenon |
| `fair:unitType` | string / object | Observation unit type (e.g. 'Person') |
| `fair:unitTypeRef` | URI / CURIE | URI of the observation unit type definition |
| `fair:universe` | string / object | Broad scope or group (e.g. 'Students') |
| `fair:universeRef` | URI / CURIE | URI of the broad universe definition |
| `fair:population` | string / object | Specific group bound by time/space |
| `fair:populationRef` | URI / CURIE | URI of the specific dataset population |
| `fair:unit` | string / object | Human-readable unit name (Literal) |
| `fair:unitRef` | URI / CURIE | URI or CURIE for the unit (Reference) |
| `fair:temporalCoverage` | object | Time period covered (structured) |
| `fair:temporalCoverageRef`| URI / CURIE | URI or CURIE for a standardized time period |
| `fair:spatialCoverage` | string / object | Human-readable geographic area name (Literal) |
| `fair:spatialCoverageRef` | URI / CURIE | URI or CURIE for the geographic area (Reference) |
| `fair:provider` | string / object | Human-readable name of the providing organization |
| `fair:providerRef` | URI | URI of the organization or person (e.g. ROR, ORCID) |
| `fair:license` | string / object | Human-readable license name (Literal) |
| `fair:licenseRef` | URI | URI of the license (Reference) |
| `fair:classification` | array | List of classification system entries (URIs/CURIEs) |

## Working Example File

`examples/mechanism-1-annotations.json`
