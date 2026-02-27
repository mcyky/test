## Cursor Cloud specific instructions

This is a minimal single-script Python project — an image downloader for the LLaVA Bench-in-the-Wild dataset.

### Project overview

- **`download.py`**: Downloads 24 images (001.jpg–024.jpg) from HuggingFace into an `images/` directory using `wget`.
- No package manager, no dependencies file, no build system, no tests, no linter config.
- Only runtime requirements: Python 3 (stdlib only — uses `os`) and system `wget`.

### Running the application

```
python3 download.py
```

This creates an `images/` directory and downloads 24 JPEG files (~9.4 MB total). The script is idempotent — re-running overwrites existing files.

### Caveats

- The script requires outbound HTTPS access to `huggingface.co` and its CDN (`cas-bridge.xethub.hf.co`).
- There are no lint, test, or build commands — the project has no such configuration.
- The `.gitignore` is a C/C++ template and not relevant to this Python project.
