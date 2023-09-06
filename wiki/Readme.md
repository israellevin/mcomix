# Wiki synchronization

## Summary
This tool allows syncing the SourceForge Wiki pages with locally stored markdown files.
Files are stored in a flat directory structure, in the `content` folder relative to this directory.
To perform the *push* operation, a bearer token from [SourceForce OAuth management](https://sourceforge.net/auth/oauth/) is needed.
Add a new authorized application (named *sfwikisync*, for example), and generate a Bearer token for this application.

## Workflow
1. Initialize a virtual environment: `python3 -m venv env`.
2. Enter the environment: `source env/bin/activate`.
3. Install the sfsyncwiki script: `pip install .`. To work on the sync script itself, install it in editable mode with development dependencies: `pip install -e .[dev]`
4. Push contents to SourceForge wiki: `sfwikisync -p mcomix -b <your SF bearer token> push`
