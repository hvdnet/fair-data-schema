# TypeScript Package & API Reference

The TypeScript package (`@fair-data-schema/core` or `schemas/<version>/typescript/index.ts`) provides auto-generated TypeScript interfaces and Zod validation schemas for the FAIR Data JSON Schema dialect.

## Quick Example (Load, Validate, Save)

```typescript
import * as fs from "fs";
import { DatasetSchemaSchema, DatasetSchema } from "./schemas/dev/typescript/index.ts";

// 1. Load schema JSON from disk
const rawJson = JSON.parse(fs.readFileSync("my-schema.json", "utf-8"));

// 2. Validate at runtime using Zod
const schema: DatasetSchema = DatasetSchemaSchema.parse(rawJson);
console.log("✓ Valid FAIR dataset:", schema.title);

// 3. Save modified schema to disk
schema.title = "Updated FAIR Dataset 2024";
fs.writeFileSync("my-schema-output.json", JSON.stringify(schema, null, 2));
```

---

## Exported Interfaces

### `DatasetSchema`
Root-level FAIR dataset schema interface extending `SchemaNode`.

```typescript
export interface DatasetSchema extends SchemaNode {
  $schema?: string;
}
```

### `SchemaNode`
Core recursive interface representing a FAIR-extended JSON Schema node.

```typescript
export interface SchemaNode {
  $id?: string;
  $ref?: string;
  $anchor?: string;
  $defs?: Record<string, SchemaNode>;
  $vocabulary?: Record<string, boolean>;
  $comment?: string;

  title?: string;
  description?: string;
  default?: any;
  deprecated?: boolean;
  readOnly?: boolean;
  writeOnly?: boolean;
  examples?: any[];

  type?: JsonType | JsonType[];
  enum?: any[];
  const?: any;
  minimum?: number;
  maximum?: number;
  exclusiveMinimum?: number;
  exclusiveMaximum?: number;
  multipleOf?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  minItems?: number;
  maxItems?: number;
  uniqueItems?: boolean;
  minContains?: number;
  maxContains?: number;
  required?: string[];
  dependentRequired?: Record<string, string[]>;
  minProperties?: number;
  maxProperties?: number;

  properties?: Record<string, SchemaNode>;
  patternProperties?: Record<string, SchemaNode>;
  additionalProperties?: SchemaNode | boolean;
  items?: SchemaNode;
  prefixItems?: SchemaNode[];
  contains?: SchemaNode;
  allOf?: SchemaNode[];
  anyOf?: SchemaNode[];
  oneOf?: SchemaNode[];
  not?: SchemaNode;
  if?: SchemaNode;
  then?: SchemaNode;
  else?: SchemaNode;

  unevaluatedProperties?: SchemaNode | boolean;
  unevaluatedItems?: SchemaNode | boolean;

  format?: string;
  contentEncoding?: string;
  contentMediaType?: string;
  contentSchema?: SchemaNode;

  // FAIR Annotations
  "fair:resourceType"?: string;
  "fair:conceptRef"?: string;
  "fair:concept"?: I18nString;
  "fair:label"?: I18nString;
  "fair:description"?: I18nText;
  "fair:datasetRelations"?: DatasetRelation[];
  "fair:contributors"?: Record<string, any>[];
  "fair:provider"?: I18nString;
  "fair:providerRef"?: string;
  "fair:license"?: I18nString;
  "fair:licenseRef"?: string;
  "fair:temporalCoverage"?: TemporalCoverage;
  "fair:temporalCoverageRef"?: string;
  "fair:spatialCoverage"?: I18nString;
  "fair:spatialCoverageRef"?: string;
  "fair:population"?: I18nString;
  "fair:populationRef"?: string;
  "fair:structureType"?: string;
  "fair:quality"?: Record<string, any>[];
  "fair:classification"?: I18nString;
  "fair:classificationRef"?: any[];
  "fair:measurementUnit"?: I18nString;
  "fair:measurementUnitRef"?: string;
  "fair:measurementTechnique"?: I18nString;
  "fair:measurementTechniqueRef"?: string;
  "fair:quantity"?: I18nString;
  "fair:quantityRef"?: string;
  "fair:measurementScale"?: I18nString;
  "fair:measurementScaleRef"?: string;
  "fair:unitType"?: I18nString;
  "fair:unitTypeRef"?: string;
  "fair:universe"?: I18nString;
  "fair:universeRef"?: string;
  "fair:variableRef"?: string;
  "fair:instanceVariableRef"?: string;
  "fair:representedVariableRef"?: string;
  "fair:conceptualVariableRef"?: string;
  "fair:sentinel"?: boolean;
}
```

### Helper Interfaces
- **`TemporalCoverage`**: `{ description?: I18nString; start?: string; end?: string; }`
- **`DatasetRelation`**: `{ relationType: string; targetRef: string; sourceVariables?: string[]; targetVariables?: string[]; cardinality?: string; description?: I18nString; }`

---

## Exported Zod Validation Schemas

- **`DatasetSchemaSchema`**: `z.ZodType<DatasetSchema>` — Validates root FAIR dataset schemas.
- **`SchemaNodeSchema`**: `z.ZodType<SchemaNode>` — Lazy recursive Zod schema for any schema node.
- **`TemporalCoverageSchema`**: Zod schema for `fair:temporalCoverage`.
- **`DatasetRelationSchema`**: Zod schema for `fair:datasetRelations`.
- **`I18nStringSchema`**: `z.union([z.string(), z.record(z.string(), z.string())])`.
- **`I18nTextSchema`**: `z.union([z.string(), z.record(z.string(), z.string())])`.
- **`JsonTypeSchema`**: `z.enum(["string", "integer", "number", "boolean", "array", "object", "null"])`.
