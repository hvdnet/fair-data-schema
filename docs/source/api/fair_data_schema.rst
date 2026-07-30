Python Package and API
======================

Quick Example (Load, Validate, Save)
------------------------------------

.. code-block:: python

   from models import DatasetSchema
   from fair_data_schema.validator import validate_schema

   # 1. Load schema from file
   schema = DatasetSchema.from_file("my-schema.json")

   # 2. Validate schema against FAIR meta-schema
   errors = validate_schema(schema.to_dict())
   assert not errors, f"Validation failed: {errors}"
   print("✓ Schema is valid FAIR Data JSON Schema!")

   # 3. Save modified schema to file
   schema.title = "Updated FAIR Dataset 2024"
   schema.to_file("my-schema-output.json")

Package API Reference
---------------------

.. automodule:: fair_data_schema
   :members:

.. automodule:: fair_data_schema.registry
   :members:

.. automodule:: fair_data_schema.validator
   :members:

.. automodule:: fair_data_schema.cli
   :members:

FAIR Pydantic Models (Standalone)
---------------------------------

.. automodule:: models
   :members:
   :exclude-members: model_config, model_fields, model_computed_fields
