#!/usr/bin/env python3
"""
Finnie - Financial AI Engine
Main application entry point
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def main():
    """Main entry point for the Finnie application."""
    try:
        # Import and run the Streamlit app
        from app.main import main as run_streamlit_app
        run_streamlit_app()
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install streamlit streamlit-option-menu plotly pandas numpy")
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
