# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Adopted mise: mise.toml + mise.lock pin python 3.12.16 (SHA256 + GitHub attestations); CI lint/test/zero-pii jobs bootstrap the interpreter via pinned jdx/mise-action with a venv on PATH (was unpinned setup-python@v6). pip install -e .[dev] and all check commands unchanged; job names preserved.
- Initial project structure.
