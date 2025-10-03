# Test Setup Module (`test_setup.py`)

## Overview

The `test_setup.py` module provides comprehensive environment verification and testing utilities for the Financial Engine package. This module is designed to validate that the SupportVectors training environment is properly configured and that all necessary components are functioning correctly.

## Purpose

This module serves as a diagnostic tool that:

- **Environment Validation**: Verifies Python version, paths, and environment variables
- **Module Testing**: Tests the ability to import and use the Financial Engine package
- **Configuration Verification**: Ensures configuration objects are accessible
- **Diagnostic Output**: Provides detailed information for troubleshooting setup issues

## Module Documentation

### Source Code

```python
#!/usr/bin/env python3
"""
Test script to verify that the environment and configuration are set up correctly.
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 SupportVectors Environment Setup Test")
    print("=" * 50)
    
    # Test Python version
    print(f"✅ Python version: {sys.version}")
    
    # Test current working directory
    print(f"✅ Working directory: {os.getcwd()}")
    
    # Test PYTHONPATH
    pythonpath = os.environ.get('PYTHONPATH', 'Not set')
    print(f"✅ PYTHONPATH: {pythonpath}")
    
    # Test PROJECT_PYTHON
    project_python = os.environ.get('PROJECT_PYTHON', 'Not set')
    print(f"✅ PROJECT_PYTHON: {project_python}")
    
    # Verify the Python executable exists
    if project_python != 'Not set':
        if os.path.exists(project_python):
            print(f"✅ Project Python executable found at: {project_python}")
        else:
            print(f"⚠️  Project Python executable not found at: {project_python}")
    
    # Test that we can import our module
    try:
        # Dynamic import based on the module structure
        src_path = Path('src')
        if src_path.exists():
            module_dirs = [d for d in src_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            if module_dirs:
                module_name = module_dirs[0].name
                print(f"✅ Found module: {module_name}")
                
                # Try to import the module
                sys.path.insert(0, str(src_path))
                try:
                    module = __import__(module_name)
                    print(f"✅ Successfully imported {module_name}")
                    
                    # Try to access the config if it exists
                    if hasattr(module, 'config'):
                        print("✅ Configuration object found and accessible")
                    else:
                        print("ℹ️  Configuration object not yet accessible (this is normal)")
                        
                except ImportError as e:
                    print(f"⚠️  Could not import {module_name}: {e}")
                    print("   This might be normal if dependencies aren't fully installed yet")
            else:
                print("ℹ️  No module directories found in src/")
        else:
            print("⚠️  src/ directory not found")
    
    except Exception as e:
        print(f"⚠️  Error during module test: {e}")
    
    print("=" * 50)
    print("🎉 Hello World! Environment setup test completed!")
    print("🎯 Your SupportVectors project environment is ready to use!")

if __name__ == "__main__":
    main()
```

## Function Documentation

### `main()` Function

**Purpose**: Main function that orchestrates the environment testing process.

**Parameters**: None

**Returns**: None

**Side Effects**: 
- Prints diagnostic information to stdout
- Modifies `sys.path` temporarily for module testing
- Performs file system checks

**Description**: 
The main function performs a comprehensive test of the SupportVectors environment setup. It checks Python version, working directory, environment variables, and module import capabilities. The function provides detailed output with emoji indicators to make the results easily readable.

#### Test Categories

1. **Python Environment Tests**
   - Python version verification
   - Current working directory check
   - PYTHONPATH environment variable validation
   - PROJECT_PYTHON environment variable validation

2. **File System Tests**
   - Python executable existence verification
   - Source directory structure validation
   - Module directory discovery

3. **Module Import Tests**
   - Dynamic module discovery
   - Module import capability testing
   - Configuration object accessibility verification

## Usage

### Command Line Usage

```bash
# Run the test script directly
python src/test_setup.py

# Or make it executable and run
chmod +x src/test_setup.py
./src/test_setup.py
```

### Programmatic Usage

```python
# Import and run the test function
from Financial Engine.test_setup import main

# Run the environment test
main()
```

### Integration with Other Tools

```python
# Use in automated testing
import subprocess
import sys

def run_environment_test():
    result = subprocess.run([sys.executable, 'src/test_setup.py'], 
                          capture_output=True, text=True)
    return result.returncode == 0
```

## Output Interpretation

### Success Indicators

- **✅**: Test passed successfully
- **ℹ️**: Informational message (normal condition)
- **🎉**: Overall success message

### Warning Indicators

- **⚠️**: Warning condition that may need attention
- **🚀**: Test initiation message

### Example Output

```
🚀 SupportVectors Environment Setup Test
==================================================
✅ Python version: 3.12.0 (main, Oct 25 2023, 10:00:00) [Clang 15.0.0]
✅ Working directory: /Users/sankar/sankar/courses/finnie
✅ PYTHONPATH: /Users/sankar/sankar/courses/finnie/src
✅ PROJECT_PYTHON: /Users/sankar/sankar/courses/finnie/.venv/bin/python
✅ Project Python executable found at: /Users/sankar/sankar/courses/finnie/.venv/bin/python
✅ Found module: Financial Engine
✅ Successfully imported Financial Engine
✅ Configuration object found and accessible
==================================================
🎉 Hello World! Environment setup test completed!
🎯 Your SupportVectors project environment is ready to use!
```

## Error Handling

### Common Error Scenarios

1. **Missing Dependencies**
   - **Symptom**: ImportError during module testing
   - **Solution**: Install required dependencies using `uv add` or `pip install`

2. **Incorrect PYTHONPATH**
   - **Symptom**: Module not found during import
   - **Solution**: Verify PYTHONPATH includes the `src` directory

3. **Missing Source Directory**
   - **Symptom**: "src/ directory not found" warning
   - **Solution**: Ensure running from project root directory

4. **Configuration Issues**
   - **Symptom**: Configuration object not accessible
   - **Solution**: Check that `svlearn-bootcamp` is installed and `.env` file exists

### Troubleshooting Steps

1. **Verify Environment Variables**
   ```bash
   echo $PYTHONPATH
   echo $PROJECT_PYTHON
   ```

2. **Check Python Path**
   ```python
   import sys
   print(sys.path)
   ```

3. **Test Module Import Manually**
   ```python
   import sys
   sys.path.insert(0, 'src')
   import Financial Engine
   ```

## Dependencies

### Required Dependencies

- **Python 3.12+**: Required for proper functionality
- **pathlib**: For path manipulation (built-in)
- **sys**: For system-specific parameters (built-in)
- **os**: For operating system interface (built-in)

### Optional Dependencies

- **Financial Engine package**: For full functionality testing
- **svlearn-bootcamp**: For configuration object testing

## Best Practices

### Development Workflow

1. **Run Before Development**: Always run this test before starting development
2. **CI/CD Integration**: Include in continuous integration pipelines
3. **Documentation**: Use output to document environment requirements
4. **Troubleshooting**: Use as first step when encountering import issues

### Environment Setup

1. **Consistent Environment**: Ensure all developers use the same environment setup
2. **Version Control**: Include environment files in version control
3. **Documentation**: Document any environment-specific requirements

## Integration with SupportVectors Framework

### Framework Compatibility

The test setup module is designed to work with the SupportVectors training framework:

- **Environment Variables**: Tests SupportVectors-specific environment variables
- **Module Structure**: Validates SupportVectors project structure
- **Configuration Testing**: Tests SupportVectors configuration system

### Educational Context

This module serves educational purposes by:

- **Learning Tool**: Helps students understand environment setup
- **Debugging Aid**: Provides clear feedback on configuration issues
- **Best Practices**: Demonstrates proper Python environment management

## Related Documentation

- [Financial Engine Package Overview](index.md) - Package-level documentation
- [Financial Engine Module](__init__.md) - Main module documentation
- [SupportVectors Environment Setup](https://supportvectors.ai/docs) - Framework documentation

## Version History

- **v0.1.0**: Initial implementation with basic environment testing
- **Current**: Enhanced with dynamic module discovery and comprehensive testing

---

*This module is part of the SupportVectors AI training curriculum and follows established patterns for educational financial AI projects.*
