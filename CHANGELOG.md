# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.5] - 2026-02-14

### Fixed
- **`install.sh` API key prompt hangs on Enter**: When run via `curl ... | sh`, the `read` command tried to read from the exhausted pipe instead of the terminal. Now reads from `/dev/tty` explicitly, and the non-interactive detection tests `/dev/tty` availability in a subshell instead of checking `stdin`.
- **`install.sh --tools` flag ignored**: The `--tools claude` filter installed to all detected tools instead of just Claude Code. Root cause: `IFS=','` set for comma-splitting the filter list also prevented the inner loop from splitting newline-separated tool entries, causing the entire tool list to match as one blob. Fixed by splitting the comma list into positional params first, then restoring IFS before iterating tools.
- **`install.sh` tool names with spaces caused bad word-splitting**: Multi-word tool names like "Claude Code", "Gemini CLI", and "OpenAI Codex" were split into separate tokens when iterating the space-separated tool list (e.g., "Claude" and "Code|/path" as two entries). Switched `DETECTED_TOOLS` from space-separated to newline-separated entries, with proper `IFS` management in all loops.

### Credits
- Thanks to `@GuyJames` on YouTube for reporting the API key prompt and `--tools` flag bugs.

## [1.5.4] - 2026-02-13

### Changed
- **Hardened credential safety in ZIP packaging (Section 5):** API key embedding is now explicitly optional — SkillHub and ClawHub search work without a key. Added prominent credential safety warning with guidance on scoped keys, key rotation, and distribution risks. Updated security reminders to differentiate key-included vs key-free ZIPs. Addresses ClawHub security review feedback.

## [1.5.3] - 2026-02-13

### Added
- **Cline support**: Added Cline as the 10th supported AI tool. User scope: `~/.cline/skills/`, Project scope: `./.cline/skills/`. Cline uses the same `SKILL.md` format with `name` and `description` frontmatter — no manifest generation required.
- Cline detection in `install.sh` one-liner installer (`--tools cline`).
- Cline included in Skill Matrix Report tool detection and skill collection.
- Cross-Platform Adaptation note: Cline also reads `.claude/skills/` at the project level, so Claude Code project skills work in Cline automatically.

## [1.5.2] - 2026-02-10

### Fixed
- **Cursor path correction**: Fixed Cursor skills path from `.cursor/extensions/` to `.cursor/skills/` in the ecosystem table, Skill Matrix Report detection, and install script.

## [1.5.1] - 2026-02-10

### Fixed
- **Frontmatter fix**: Moved `disable-model-invocation` from nested `metadata` block to top-level frontmatter for correct parsing.

## [1.5.0] - 2026-02-10

### Added
- **Homoglyph transliteration**: Cyrillic homoglyphs are now transliterated to ASCII before running semantic pattern checks (instruction override, role hijacking, safety bypass, prompt extraction). This closes the M2 evasion gap where attackers could use Cyrillic look-alike characters to bypass denylist detection.
- 3 new tests for homoglyph transliteration (instruction override, safety bypass, and combined detection).
- Empty file edge case test.
- `SECURITY.md` with vulnerability reporting process, full security architecture documentation, and known limitations.

### Changed
- **scan_skill.py bumped to v1.2.0**: Includes homoglyph transliteration, performance fix, and Windows portability.
- `_join_continuation_lines` refactored from quadratic string concatenation (`+=`) to list accumulator (`''.join()`), preventing potential 10-20s stalls on large files with many continuation lines.
- Homoglyph map consolidated: single module-level `_HOMOGLYPH_MAP` dict used by both detection and transliteration (was duplicated as class attribute).
- Tests converted from manual `try/finally` global mutation to pytest `monkeypatch` fixture (safe for parallel test execution).
- Multi-line detection test fixed: `test_multiline_bash_c_detected` now correctly tests continuation-line joining at natural word boundaries (was previously testing single-line matching).
- Homoglyph test strengthened: `test_homoglyph_instruction_override_detected` now asserts BOTH `homoglyph_detected` AND `instruction_override` findings (was previously accepting either, masking the M2 gap).

### Fixed
- **install_skill.py integration bug** (pre-existing): Security scan findings were never displayed to the user. `severity_order` used uppercase (`"CRITICAL"`) but scanner outputs lowercase (`"critical"`), and field name was `"message"` instead of `"description"`. Users saw "Security scan found N issue(s)" with a blank findings section.
- **scan_skill.py Windows portability**: `os.O_NOFOLLOW` caused `AttributeError` crash on Windows where the flag doesn't exist. Now guarded with `hasattr()` check; falls back to `is_symlink()` pre-check.

### Security
- All 20 findings from [@ben-alkov](https://github.com/ben-alkov)'s security analysis are now fully closed, including the M2 homoglyph evasion that was previously only detected but not neutralized.

### Credits
- Massive thanks to **[@ben-alkov](https://github.com/ben-alkov)** (Ben Alkov) for an outstanding security contribution: full Claude Code-driven security analysis of `scan_skill.py`, a detailed remediation work plan, 18 atomic commits addressing 20 security findings across 4 severity levels, comprehensive test suite (62 tests), and a final code review by a separate Claude Code instance. This work transformed the scanner from a baseline pattern matcher into a hardened security tool with defense-in-depth against symlink traversal, resource exhaustion, ANSI injection, scanner evasion via dotfiles/continuations/homoglyphs/unclosed comments, and expanded detection coverage for credentials and dangerous URIs. The collaboration — initiated via a Slack message offering unsolicited security help — exemplifies the best of open-source community contribution.

## [1.4.2] - 2026-02-10

### Fixed
- install_skill.py severity case mismatch and field name mismatch (see v1.5.0 for details).
- scan_skill.py O_NOFOLLOW Windows portability (see v1.5.0 for details).

### Added
- SECURITY.md initial creation.
- Updated README.md, CLAUDE.md with security scanning docs.

## [1.4.1] - 2026-02-10

### Fixed
- Address ClawHub security review: declare runtime requirements (`python3`, `curl`), primary env var (`SKILLSMP_API_KEY`), and `disable-model-invocation` in YAML frontmatter metadata.
- Add `homepage` field to frontmatter.
- Add security note for API key handling in ZIP packaging.
- Remove `save_memory` reference.

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
