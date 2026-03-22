FAIR JSON Meta-Schema
=====================

A custom JSON Schema dialect and vocabularies for FAIR Datasets.

Versioning
----------
The FAIR Data JSON Schema follows a versioned release strategy:
* **Release Versions** (e.g., ``/0.1.0/``): Stable points documented in the changelog.
* **Development Track** (``/dev/``): The bleeding edge where new features are prototyped.
* **Landing Page**: The root URL serves the interactive project overview.

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   background

.. toctree::
   :maxdepth: 2
   :caption: Extension Mechanisms

   mechanisms/annotations
   mechanisms/vocabulary
   mechanisms/dialect
   mechanisms/refinements

.. toctree::
   :maxdepth: 2
   :caption: Examples & Guides

   examples/variable-cascade
   examples/enum-to-fair-coded-values
   examples/complex-data-product

.. toctree::
   :maxdepth: 1
   :caption: Python Package

   api/fair_data_schema

.. toctree::
   :maxdepth: 1
   :caption: Project

   changelog
