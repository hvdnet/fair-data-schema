# CDIF v1.1 Profile Alignment Example

This example demonstrates how **FAIR Data JSON Schema** maps directly to the **Cross-Domain Interoperability Framework (CDIF) Version 1.1** profiles ([book.cdif.org](https://book.cdif.org)).

---

## Key Alignment Features

The accompanying schema ([`cdif-profile-alignment.json`](cdif-profile-alignment.json)) demonstrates the following CDIF v1.1 profile mappings:

1. **CDIF Core & Access Profile**:
   - `title` & `description`: Basic dataset identification (`schema:name`, `schema:description`).
   - `fair:license` & `fair:licenseRef`: Machine-actionable SPDX license reference.
   - `fair:contributors`: Human, organizational, and agent attribution with explicit role names and ROR/ORCID URIs.

2. **CDIF Discovery Profile**:
   - `fair:spatialCoverageRef`: Geographic extent linked to EU Publications Office Country authority.
   - `fair:temporalCoverage`: ISO 8601 calendar observation interval (`2024-01-01/2024-12-31`).
   - `fair:quality`: Data quality measurements aligned with W3C Data Quality Vocabulary (`dqv:hasQualityMeasurement`).
   - `fair:measurementTechnique` & `fair:measurementTechniqueRef`: Sensor technology and protocol specification.

3. **CDIF Data Structure Profile**:
   - `fair:structureType`: Explicit layout subtyping (`"wide"` tabular format).
   - Technical validation rules (`type`, `minimum`, `format`) enforced directly by JSON Schema.

4. **DDI Variable Cascade Profile**:
   - `fair:conceptualVariableRef`: High-level semantic phenomenon link.
   - `fair:representedVariableRef`: Shared representation / code list link.
   - `fair:instanceVariableRef`: Dataset-specific variable implementation link.

---

## Tooling & CLI Commands

### 1. Validate the Schema

Validate `cdif-profile-alignment.json` against the FAIR Data JSON Schema meta-schema:

```bash
fair-data-schema validate examples/cdif-profile-alignment.json
```

### 2. Export to RO-Crate 1.1 Manifest

Convert the FAIR Data JSON Schema directly into a valid **RO-Crate 1.1** metadata document (`ro-crate-metadata.json`) complying with CDIF Manifest specifications:

```bash
fair-data-schema export ro-crate examples/cdif-profile-alignment.json -o ro-crate-metadata.json
```
