# 🩺 env-doctor

**`env-doctor`** is a zero-dependency, lightweight CLI tool designed for developers and CI/CD pipelines to validate `.env` configuration files against `.env.example` templates, detect missing or undocumented environment variables, and automatically generate safe templates by stripping sensitive values.

## ✨ Features

- 🔍 **Sync Check**: Quickly identify missing required keys in your local `.env` before your app crashes at runtime.
- ⚠️ **Empty Value Detection**: Catch variables that are defined but accidentally left blank (`--strict` mode supported for CI/CD).
- 🛡️ **Safe Template Generation**: Automatically generate or update `.env.example` from your local `.env` with all secret values stripped, preserving comments and formatting.
- 🚀 **Zero Dependencies**: Built purely with Python's standard library. Fast and portable.

## 📦 Installation & Usage

### 1. Validate your `.env` file
Compare your local `.env` against `.env.example`:

    python env_doctor.py check

Use `--strict` in CI/CD pipelines to fail the build if any variable is empty:

    python env_doctor.py check --strict -e .env.production -t .env.example

### 2. Generate a safe `.env.example`
Strip secret values from your existing `.env` while keeping comments and keys intact:

    python env_doctor.py init -e .env -o .env.example

## 🗺️ Roadmap

- [ ] Support JSON and YAML output formats for CI/CD integration.
- [ ] Add type validation annotations in comments (e.g., `# @type: int`, `# @type: url`).
- [ ] Pre-commit hook integration (`.pre-commit-config.yaml`).

## 📄 License

This project is licensed under the MIT License.
