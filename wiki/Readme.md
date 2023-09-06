# Wiki synchronization

## Summary
This tool allows syncing the SourceForge Wiki pages with locally stored markdown files.
Files are stored in a flat directory structure, in the `content` folder relative to this directory.

## Workflow
1. Initialize a virtual environment: `python3 -m venv env`.
2. Enter the environment: `source env/bin/activate`.
3. Install the sfsyncwiki script: `pip install .`. To work on the sync script itself, install it in editable mode with development dependencies: `pip install -e .[dev]`
4. Push contents to SourceForge wiki: `sfwikisync -p mcomix -b <your SF bearer token> push`
