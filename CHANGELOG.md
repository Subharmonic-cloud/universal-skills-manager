# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-02-09

### Added
- ClawHub integration as third search source (5,700+ versioned skills, semantic search, no API key required).
- Three-source skill discovery: SkillsMP (curated, AI semantic search) + SkillHub (open catalog) + ClawHub (versioned, semantic search).
- ClawHub semantic/vector search via `/api/v1/search` endpoint with similarity scoring.
- ClawHub browse/list via `/api/v1/skills` endpoint with cursor pagination and sorting (stars, downloads, trending).
- Direct file fetch install flow for ClawHub skills (bypasses `install_skill.py`, uses ClawHub's `/file` endpoint + manual `scan_skill.py`).
- ZIP download fallback for multi-file ClawHub skills via `/download` endpoint.
- Onboarding flow expanded from A/B to A/B/C choice (SkillsMP / SkillHub / ClawHub).
- Source labeling extended to include `[ClawHub]` tag in search results.
- ClawHub API documentation in SKILL.md, README.md, and CLAUDE.md.

### Changed
- "Search More Sources" generalized to offer all remaining unsearched sources (was SkillHub-only).
- Cross-source deduplication extended: SkillsMP ↔ SkillHub by ID, ClawHub ↔ others by skill name.
- Installation sections reorganized: A (SkillsMP), B (SkillHub), C (ClawHub), D (Local Source).

## [1.3.0] - 2026-02-10

### Added
- SkillHub integration as secondary search source (173k+ community skills, no API key required).
- Multi-source skill discovery: SkillsMP (curated, AI semantic search) + SkillHub (open catalog).
- New onboarding flow: users without a SkillsMP API key can search SkillHub immediately.
- "Search More Sources" option for SkillsMP users to also query SkillHub.
- Source labeling in search results ([SkillsMP] vs [SkillHub]).
- Deduplication logic across sources by full skill ID.
- SkillHub API documentation in SKILL.md, README.md, and CLAUDE.md.

### Changed
- Rebranded from "Universal Skill Manager" to "Universal Skills Manager".
- Renamed skill folder from `universal-skill-manager/` to `universal-skills-manager/` for consistency with branding and repo name. **Breaking:** existing installations will need to remove the old folder manually.
- Updated repository URL to `https://github.com/jacob-bd/universal-skills-manager`.
- SkillsMP API key is now optional (was previously required for all skill discovery).
- Updated install.sh messaging to reflect dual-source availability.

## [1.1.0] - 2026-02-07

### Added
- Security scanning for skill files at install time (`scan_skill.py`).
- 14 detection categories across 3 severity levels (Critical/Warning/Info).
- Detects invisible Unicode, data exfiltration URLs, shell pipe execution, credential references, command execution patterns, prompt injection, role hijacking, safety bypass attempts, HTML comments, encoded content, delimiter injection, and cross-skill escalation.
- `--skip-scan` flag for `install_skill.py` to bypass security scan.
- `docs/SECURITY_SCANNING.md` reference documentation.

## [1.0.1] - 2026-02-03

### Added
- ZIP packaging capability for claude.ai and Claude Desktop
- Hybrid API key discovery (environment variable → config file → runtime prompt)
- `config.json` template for embedded API key storage
- Documentation for claude.ai and Claude Desktop installation

### Changed
- Updated API key discovery logic to support multiple sources
- Expanded supported platforms to include claude.ai and Claude Desktop

## [1.0.0] - 2026-02-01

### Added
- Initial release of the Universal Skills Manager.
- Skill definition with `SKILL.md`.
- `install_skill.py` script for atomic, safe installation.
- Support for multiple AI ecosystems (Claude Code, Gemini, Anti-Gravity, OpenCode, etc.).
- SkillsMP.com API integration for skill discovery.
