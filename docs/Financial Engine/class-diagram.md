# Financial Engine - Class Diagram

## Project Structure Overview

This diagram illustrates the overall architecture and relationships within the Financial Engine package and the broader Finnie project.

```mermaid
classDiagram
    class FinnieProject {
        +string name: "finnie"
        +string version: "0.1.0"
        +string description: "Finnie"
        +string python_version: ">=3.12"
        +dependencies: List~string~
        +build_system: "hatchling"
    }

    class FinancialEnginePackage {
        +string name: "Financial Engine"
        +string path: "src/Financial Engine/"
        +__init__.py: Module
        +test_setup.py: Module
    }

    class FinancialEngineInit {
        +ConfigurationMixin config_mixin
        +dotenv load_dotenv
        +config: ConfigurationObject
        +load_environment()
        +initialize_config()
    }

    class TestSetupModule {
        +main() function
        +test_python_version()
        +test_working_directory()
        +test_pythonpath()
        +test_project_python()
        +test_module_import()
        +test_configuration()
    }

    class SupportVectorsFramework {
        +svlearn.bootcamp
        +ConfigurationMixin
        +training_materials
        +educational_context
    }

    class MkDocsDocumentation {
        +Material theme
        +Mermaid diagrams
        +Jupyter notebooks
        +API documentation
        +Custom styling
    }

    class ProjectConfiguration {
        +pyproject.toml
        +mkdocs.yml
        +config.yaml
        +.env files
        +.gitignore
    }

    class BuildSystem {
        +build_docs.sh
        +serve_docs.sh
        +hatchling build
        +mkdocs build
    }

    %% Relationships
    FinnieProject --> FinancialEnginePackage : contains
    FinancialEnginePackage --> FinancialEngineInit : contains
    FinancialEnginePackage --> TestSetupModule : contains
    
    FinancialEngineInit --> SupportVectorsFramework : uses
    TestSetupModule --> FinancialEnginePackage : tests
    
    FinnieProject --> MkDocsDocumentation : documents
    FinnieProject --> ProjectConfiguration : configured_by
    FinnieProject --> BuildSystem : built_with
    
    SupportVectorsFramework --> FinancialEngineInit : provides ConfigurationMixin
    SupportVectorsFramework --> TestSetupModule : provides framework_context
```

## Module Dependencies Diagram

This diagram shows the specific dependencies and relationships between the core modules.

```mermaid
classDiagram
    class FinancialEngineInit {
        +from svlearn.config.configuration import ConfigurationMixin
        +from dotenv import load_dotenv
        +load_dotenv()
        +config = ConfigurationMixin().load_config()
    }

    class TestSetupModule {
        +import sys
        +import os
        +from pathlib import Path
        +def main()
        +test_python_version()
        +test_environment_variables()
        +test_module_imports()
    }

    class ConfigurationMixin {
        +load_config() method
        +SupportVectors framework integration
        +standardized configuration management
    }

    class DotEnvModule {
        +load_dotenv() function
        +environment variable loading
        +.env file processing
    }

    class PythonStandardLibrary {
        +sys module
        +os module
        +pathlib module
        +built-in functionality
    }

    %% Dependencies
    FinancialEngineInit --> ConfigurationMixin : imports and uses
    FinancialEngineInit --> DotEnvModule : imports and uses
    
    TestSetupModule --> PythonStandardLibrary : imports and uses
    TestSetupModule --> FinancialEngineInit : tests import capability
    
    ConfigurationMixin --> DotEnvModule : may use for config loading
```

## Environment and Configuration Flow

This diagram illustrates how the environment setup and configuration loading works in the Financial Engine package.

```mermaid
classDiagram
    class EnvironmentSetup {
        +.env file loading
        +environment variable setup
        +PYTHONPATH configuration
        +PROJECT_PYTHON setup
    }

    class ConfigurationLoading {
        +ConfigurationMixin instantiation
        +config object creation
        +SupportVectors framework integration
    }

    class ModuleInitialization {
        +Financial Engine package import
        +automatic configuration loading
        +global config object availability
    }

    class EnvironmentTesting {
        +test_setup.py execution
        +environment validation
        +module import testing
        +configuration verification
    }

    class SupportVectorsIntegration {
        +svlearn-bootcamp framework
        +educational context
        +training material integration
        +standardized patterns
    }

    %% Flow relationships
    EnvironmentSetup --> ConfigurationLoading : provides environment
    ConfigurationLoading --> ModuleInitialization : creates config object
    ModuleInitialization --> EnvironmentTesting : enables testing
    EnvironmentTesting --> SupportVectorsIntegration : validates framework
    SupportVectorsIntegration --> ConfigurationLoading : provides framework
```

## Documentation Structure

This diagram shows the documentation architecture and how it relates to the codebase.

```mermaid
classDiagram
    class MkDocsSite {
        +Material theme
        +site navigation
        +search functionality
        +responsive design
    }

    class FinancialEngineDocs {
        +index.md: package overview
        +__init__.md: module documentation
        +test_setup.md: testing documentation
        +class-diagram.md: visual diagrams
    }

    class ProjectDocumentation {
        +index.md: main project page
        +notebooks/: Jupyter notebooks
        +project-guide/: guides and tips
        +apidocs/: API documentation
    }

    class VisualElements {
        +Mermaid diagrams
        +class diagrams
        +sequence diagrams
        +flowcharts
    }

    class StylingAndAssets {
        +supportvectors.css
        +custom fonts
        +logo and branding
        +mathjax integration
    }

    %% Relationships
    MkDocsSite --> FinancialEngineDocs : contains
    MkDocsSite --> ProjectDocumentation : contains
    MkDocsSite --> VisualElements : renders
    MkDocsSite --> StylingAndAssets : styled_by
    
    FinancialEngineDocs --> VisualElements : includes diagrams
    ProjectDocumentation --> VisualElements : includes diagrams
```

## Key Relationships Summary

### Core Dependencies
- **Financial Engine Package** depends on **SupportVectors Framework** for configuration management
- **Test Setup Module** depends on **Python Standard Library** for basic functionality
- **Configuration Loading** depends on **Environment Setup** for proper initialization

### Documentation Integration
- **MkDocs Site** provides the documentation platform
- **Financial Engine Documentation** covers the core package functionality
- **Visual Diagrams** enhance understanding through Mermaid diagrams
- **Styling and Assets** provide SupportVectors branding and custom appearance

### Build and Development
- **Project Configuration** defines the build and development environment
- **Build System** handles documentation generation and serving
- **Environment Testing** validates proper setup and configuration

This architecture ensures a well-structured, documented, and maintainable financial AI project that follows SupportVectors best practices and educational standards.
