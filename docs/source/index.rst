FAIR JSON Meta-Schema
=====================

.. caution::
   **EARLY DEVELOPMENT STAGE**: This project and its meta-schemas are in **early development for prototyping and testing only**. Focus is on implementing core vocabularies and ensuring architectural consistency. Avoid production-ready assumptions.

A custom JSON Schema dialect and vocabularies for FAIR Datasets.

Versioning
----------
The FAIR Data JSON Schema follows a versioned release strategy:

* **Release Versions** (e.g., ``/0.1.0/``): Stable points documented in the changelog.
* **Development Track** (``/dev/``): The bleeding edge where new features are prototyped.
* **Landing Page**: The root URL (https://highvaluedata.net/fair-data-schema/) serves the interactive project overview.

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   background
   cdif_comparison

.. toctree::
   :maxdepth: 1
   :caption: Publications

   publications/index
   publications/vision-and-positioning
   publications/bridging-the-gap-fair-json-schema

.. toctree::
   :maxdepth: 2
   :caption: Specifications

   specs/index
   specs/keywords

.. toctree::
   :maxdepth: 2
   :caption: Cookbook & Guides

   cookbook/index
   validation
   python-sdk

.. toctree::
   :maxdepth: 2
   :caption: Extension Mechanisms (Advanced)

   mechanisms/index

.. toctree::
   :maxdepth: 1
   :caption: Python Package

   api/fair_data_schema

.. toctree::
   :maxdepth: 1
   :caption: Project

   changelog
