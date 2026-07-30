# TypeScript SDK — Types & Zod Schemas

The FAIR Data JSON Schema project provides auto-generated **TypeScript interfaces** and **Zod schemas** for client-side web applications, Node.js API servers, and AI / MCP tool-calling integrations.

## Overview

The generated TypeScript code is located in `schemas/<version>/typescript/index.ts` (and mirrored in the web distribution at `dist/<version>/typescript/index.ts`).

It provides:
- **Compile-time TypeScript interfaces**: `SchemaNode`, `DatasetSchema`, `TemporalCoverage`, `DatasetRelation`
- **Runtime validation Zod schemas**: `SchemaNodeSchema`, `DatasetSchemaSchema`, `TemporalCoverageSchema`, `DatasetRelationSchema`
- **Type Aliases**: `I18nString`, `I18nText`, `JsonType`

## Installation

To validate data at runtime using Zod, install `zod` in your JavaScript/TypeScript project:

```bash
npm install zod
```

## Basic Usage

### Parsing & Validating Schemas (Zod)

You can validate incoming JSON dataset schemas at runtime using `DatasetSchemaSchema`:

```typescript
import { DatasetSchemaSchema, DatasetSchema } from "./schemas/dev/typescript/index.ts";

const rawJson = {
  $schema: "https://highvaluedata.net/fair-data-schema/dev",
  title: "Annual Employee Payroll 2024",
  "fair:license": "CC-BY-4.0",
  "fair:unitType": "Employee",
  type: "object",
  properties: {
    salary: {
      title: "Annual Base Salary",
      type: "number",
      "fair:measurementUnit": "USD"
    }
  }
};

// Validate raw JSON schema at runtime
const schema: DatasetSchema = DatasetSchemaSchema.parse(rawJson);

console.log(schema.title); // "Annual Employee Payroll 2024"
console.log(schema["fair:license"]); // "CC-BY-4.0"
```

### TypeScript Compile-Time Autocomplete

When authoring schemas programmatically in TypeScript, use the `DatasetSchema` and `SchemaNode` interfaces for full IDE autocomplete:

```typescript
import { DatasetSchema, SchemaNode } from "./schemas/dev/typescript/index.ts";

const ageVariable: SchemaNode = {
  type: "integer",
  title: "Age",
  minimum: 0,
  "fair:measurementUnit": "years",
  "fair:quantity": "Time duration"
};

const myDataset: DatasetSchema = {
  $schema: "https://highvaluedata.net/fair-data-schema/dev",
  title: "Census 2024",
  "fair:license": "CC-BY-4.0",
  "fair:population": "Total Resident Population",
  properties: {
    age: ageVariable
  }
};
```

## Auto-Generation

The TypeScript definition file `schemas/<version>/typescript/index.ts` is **auto-generated** from the FAIR annotation meta-schemas using Jinja2 templates.

To regenerate TypeScript models for the development track:

```bash
uv run python scripts/generate_typescript.py --version dev
```
