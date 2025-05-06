Certainly! Here's a visual representation of how pip install -e . (editable install) works across two frameworks sharing the same virtual environment:

📁 Project Structure

/path/to/venv/                  # Shared virtual environment
├── bin/
├── lib/
│   └── pythonX.X/
│       └── site-packages/
│           └── mypackage.egg-link → /path/to/framework1/mypackage
├── ...
/path/to/framework1/
└── mypackage/
    ├── __init__.py
    └── module.py
/path/to/framework2/
└── ...

🔄 How It Works

1. Editable Install: Running pip install -e . inside /path/to/framework1/ creates an .egg-link file in the site-packages directory of the shared virtual environment. This file points to the source code location of mypackage in framework1.


2. Shared Virtual Environment: Since both framework1 and framework2 use the same virtual environment, any changes made to mypackage in framework1 are immediately reflected when framework2 imports and uses mypackage.


3. No Reinstallation Needed: This setup allows for real-time development and testing across multiple projects without the need to reinstall the package after each change.



⚠️ Considerations

Metadata Changes: If you modify project metadata (e.g., dependencies, entry points), you'll need to rerun the editable install command to reflect those changes.

Non-Python Files: Editable installs primarily track Python modules. Changes to non-Python files may not be automatically recognized.

Strict Mode: For a behavior closer to regular installs, you can use strict mode:

pip install -e . --config-settings editable_mode=strict

This mode attempts to mimic a standard installation more closely but may not expose new files automatically.


If you have further questions or need assistance with specific aspects of editable installs, feel free to ask!

