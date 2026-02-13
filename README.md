# Universal Skills Manager

<p align="center">
  <img src="assets/mascot.png" alt="Universal Skills Manager" width="100%">
</p>

<p align="center">
  <a href="https://skillsmp.com">SkillsMP.com</a> •
  <a href="https://skills.palebluedot.live">SkillHub</a> •
  <a href="https://clawhub.ai">ClawHub</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#supported-tools">Supported Tools</a>
</p>

---

**v1.5.3** · Three-source skill discovery · 10 supported AI tools · Hardened security scanning

A centralized skill manager for AI coding assistants. Discovers, installs, and synchronizes skills from multiple sources — [SkillsMP.com](https://skillsmp.com) (curated, AI semantic search), [SkillHub](https://skills.palebluedot.live) (173k+ community skills, no API key required), and [ClawHub](https://clawhub.ai) (5,700+ versioned skills, semantic search, no API key required) — across multiple AI tools including Claude Code, OpenAI Codex, Gemini CLI, and more.

## Demo

<p align="center">
  <a href="https://youtu.be/PnOD9pJCk1U">
    <img src="https://img.youtube.com/vi/PnOD9pJCk1U/0.jpg" alt="Universal Skills Manager Demo" width="100%">
  </a>
</p>

This video covers:
- Installation
- Searching for a skill
- Installing a skill
- Generating a skill report
- Synchronizing skills among multiple tools

## Features

- 🔍 **Multi-Source Search**: Find skills from SkillsMP (curated, AI semantic search), SkillHub (173k+ community catalog), and ClawHub (5,700+ versioned skills, semantic search) — no API key needed for SkillHub or ClawHub
- 📦 **One-Click Install**: Download and validate skills with atomic installation (temp → validate → install)
- 🛡️ **Security Scanning**: 20+ detection categories across 3 severity levels — catches invisible Unicode, data exfiltration, shell injection, prompt injection, homoglyphs, hardcoded secrets, and more
- 🔄 **Cross-Tool Sync**: Automatically sync skills across all your installed AI tools
- 📊 **Skill Matrix Report**: See which skills are installed on which tools at a glance
- ⚡ **One-Liner Installer**: `curl | sh` auto-detects your tools and installs everywhere, with `--tools` flag for targeting specific tools
- ✅ **Multi-File Validation**: Validates `.py`, `.sh`, `.json`, `.yaml` files during install
- 🌍 **Global Installation**: User-level skills available across all projects
- ☁️ **Cloud Upload Packaging**: Create ready-to-upload ZIP files for claude.ai/Claude Desktop

## Security Scanning

Skills are automatically scanned for security threats at install time. The scanner (`scan_skill.py` v1.1.0) checks 20+ threat categories:

**Critical:**
- Symlink traversal and path escape attempts
- Invisible/zero-width Unicode characters hiding instructions
- Data exfiltration via markdown images with variable interpolation
- Remote code piped into shell interpreters (`curl | bash`)
- Unclosed HTML comments suppressing subsequent content

**Warning:**
- Credential file references (`~/.ssh/`, `~/.aws/`, etc.) and 30+ sensitive env var patterns
- Hardcoded secrets (AWS keys, GitHub PATs, Slack tokens, JWTs, private key blocks)
- Dangerous command execution (`eval()`, `os.system()`, `subprocess.run()`)
- Prompt injection (instruction overrides, role hijacking, safety bypasses)
- Homoglyph characters (Cyrillic look-alikes that bypass text-based checks)
- Data URIs, JavaScript URIs, and protocol-relative URLs

**Info:**
- Encoded content (base64, hex, URL-encoded payloads)
- LLM delimiter tokens, cross-skill escalation attempts
- Binary files and unreadable files

**Scanner defenses:** Triple-layer symlink protection, fd-based TOCTOU mitigation, 10MB file size limit, ANSI escape stripping, Unicode NFC normalization, continuation line joining for multi-line payloads.

Findings are displayed with severity levels and you choose whether to proceed. See [Security Scanning Reference](docs/SECURITY_SCANNING.md) and [SECURITY.md](SECURITY.md) for full details.

## Installation

### Option 1: One-Liner Install (Recommended)

Auto-detects your installed AI tools and installs to all of them:

```bash
curl -fsSL https://raw.githubusercontent.com/jacob-bd/universal-skills-manager/main/install.sh | sh
```

Or install to specific tools only:

```bash
# Download and run with --tools flag
curl -fsSL https://raw.githubusercontent.com/jacob-bd/universal-skills-manager/main/install.sh -o /tmp/install.sh
sh /tmp/install.sh --tools claude,gemini
```

The installer will:
1. Check for Python 3.8+
2. Auto-detect which AI tools you have installed
3. Download the Universal Skills Manager from GitHub
4. Install to all detected tools (or just the ones you specify)
5. Optionally set up your SkillsMP API key

**Supported `--tools` values:** `claude`, `gemini`, `antigravity`, `opencode`, `openclaw`, `codex`, `goose`, `roo`, `cursor`, `cline`

> **Note:** The installer automatically installs to **all** detected AI tools without prompting for confirmation. If you only want to install to specific tools, use the `--tools` flag to target them explicitly.

### Option 2: Manual Install

```bash
git clone https://github.com/jacob-bd/universal-skills-manager.git
cd universal-skills-manager
```

Copy the `universal-skills-manager` folder to your tool's skills directory:

| Tool | Global Path |
|------|-------------|
| **Claude Code** | `~/.claude/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` |
| **Gemini CLI** | `~/.gemini/skills/` |
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` |
| **Cursor** | `~/.cursor/skills/` |
| **Cline** | `~/.cline/skills/` |
| **Roo Code** | `~/.roo/skills/` |
| **OpenCode** | `~/.config/opencode/skills/` |
| **OpenClaw** | `~/.openclaw/workspace/skills/` |
| **block/goose** | `~/.config/goose/skills/` |
| **claude.ai / Claude Desktop** | `[ZIP upload]` See [instructions below](#claudeai-and-claude-desktop) |

```bash
# Example: Install to Claude Code
cp -r universal-skills-manager ~/.claude/skills/

# Example: Install to Gemini CLI
cp -r universal-skills-manager ~/.gemini/skills/
```

After installing, restart your AI tool to pick up the new skill.

## Quick Start

Once installed, just ask your AI assistant:

```
"Search for a debugging skill"
"Install the humanizer skill"
"Show me my skill report"
"Sync the skill-creator to all my tools"
"What skills do I have in Codex vs Claude?"
```

### Using the Install Script

The skill includes a Python helper script for downloading skills from GitHub:

```bash
# Preview what would be downloaded (dry-run)
python3 path/to/install_skill.py \
  --url "https://github.com/user/repo/tree/main/skill-folder" \
  --dest "~/.codex/skills/my-skill" \
  --dry-run

# Actually install to your preferred tool
python3 path/to/install_skill.py \
  --url "https://github.com/user/repo/tree/main/skill-folder" \
  --dest "~/.gemini/skills/my-skill" \
  --force
```

**Script features:**
- Zero dependencies (Python 3 stdlib only)
- Atomic install (downloads to temp, validates, then copies to destination)
- Safety check prevents accidental targeting of root skills directories
- Compares new vs existing skills before update (shows diff)
- Validates `.py`, `.sh`, `.json`, `.yaml` files
- Supports subdirectories and nested files
- Skip security scan with `--skip-scan` (not recommended)

## Configuration

### API Key Setup

The Universal Skills Manager uses a SkillsMP API key for curated search with AI semantic matching. **The API key is optional** — without it, you can still search SkillHub's open catalog of 173k+ community skills and ClawHub's 5,700+ versioned skills with semantic search.

#### Option 1: Shell Profile (Recommended)

Add the API key to your shell profile to make it available globally across all sessions:

```bash
# For Zsh users (macOS default)
echo 'export SKILLSMP_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc

# For Bash users
echo 'export SKILLSMP_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

This ensures the API key is always available when you use any AI tool.

#### Option 2: .env File in Home Directory

Create a `.env` file in your home directory:

```bash
# Create ~/.env
cat > ~/.env << 'EOF'
SKILLSMP_API_KEY=your_api_key_here
EOF
```

Then load it before using AI tools:

```bash
# Load .env file
source ~/.env

# Or add to your shell profile to auto-load
echo 'source ~/.env' >> ~/.zshrc
```

#### Option 3: Session-based (Temporary)

For temporary use in a single terminal session:

```bash
export SKILLSMP_API_KEY="your_api_key_here"
```

**Note**: This only persists for the current terminal session.

#### Windows Users

For Windows (PowerShell):
```powershell
[System.Environment]::SetEnvironmentVariable('SKILLSMP_API_KEY', 'your_api_key_here', 'User')
```
*Restart your terminal for changes to take effect.*

For Windows (Command Prompt):
```cmd
setx SKILLSMP_API_KEY "your_api_key_here"
```

#### Getting Your API Key

1. Visit [SkillsMP.com](https://skillsmp.com)
2. Navigate to the API section
3. Generate or copy your API key
4. Configure using one of the methods above

#### Verify API Key Setup

After configuration, verify the API key is set correctly:

```bash
# Check if the environment variable is set
echo $SKILLSMP_API_KEY

# Test the API connection
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=test&limit=1" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY"
```

If configured correctly, you should see a JSON response with skill data.

## Usage

Once installed, the skill activates automatically when you:

### Search for Skills

```
"Find a debugging skill"
"Search for React skills"
"Show me skills for testing"
```

The AI will search available sources (SkillsMP, SkillHub, and/or ClawHub) and display relevant skills with:
- Skill name and author
- Description
- Star rating
- GitHub repository link

### Install Skills

After search results appear:

```
"Install the code-debugging skill"
"Install skill #3 from the results"
```

The AI will:
1. Ask whether to install globally or locally
2. Fetch the skill content from GitHub or ClawHub
3. Detect other installed AI tools
4. Offer to sync the skill across all tools
5. Install and confirm success

### Sync Skills

```
"Sync the debugging skill to Cursor"
"Copy this skill to all my AI tools"
```

### Manage Skills

```
"Show my installed skills"
"Update the debugging skill"
"Remove the old React skill"
```

## How It Works

1. **Discovery**: The AI queries multiple sources (SkillsMP.com, SkillHub, and/or ClawHub) using keyword or semantic search
2. **Selection**: You choose which skill to install from the results
3. **Fetching**: The AI fetches the SKILL.md content from GitHub or directly from ClawHub
4. **Installation**: Creates the proper directory structure (`~/.claude/skills/{skill-name}/`)
5. **Synchronization**: Optionally copies to other detected AI tools

## Supported Tools

| AI Tool | Global Path | Local Path |
|---------|-------------|------------|
| **Claude Code** | `~/.claude/skills/` | `./.claude/skills/` |
| **Cursor** | `~/.cursor/skills/` | `./.cursor/skills/` |
| **Gemini CLI** | `~/.gemini/skills/` | `./.gemini/skills/` |
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` | `./.antigravity/extensions/` |
| **OpenCode** | `~/.config/opencode/skills/` | `./.opencode/skills/` |
| **OpenClaw** | `~/.openclaw/workspace/skills/` | `./.openclaw/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `./.codex/skills/` |
| **block/goose** | `~/.config/goose/skills/` | `./.goose/agents/` |
| **Roo Code** | `~/.roo/skills/` | `./.roo/skills/` |
| **Cline** | `~/.cline/skills/` | `./.cline/skills/` |

## claude.ai and Claude Desktop

For use in claude.ai or Claude Desktop (web-based environments), the skill requires special packaging since environment variables are not available.

**Option 1: On-Demand Packaging (Recommended)**

If you have the skill installed in Claude Code, simply ask:

```
"Package this skill for claude.ai"
"Create a ZIP for Claude Desktop"
```

The AI will:
1. Ask for your SkillsMP API key
2. Create a ZIP file with your key embedded
3. Provide upload instructions

**Option 2: Manual Packaging**

1. Copy the skill folder and create `config.json`:
   ```bash
   cp -r universal-skills-manager /tmp/
   echo '{"skillsmp_api_key": "YOUR_KEY_HERE"}' > /tmp/universal-skills-manager/config.json
   ```

2. Create ZIP:
   ```bash
   cd /tmp && zip -r universal-skills-manager.zip universal-skills-manager/
   ```

3. Upload to claude.ai:
   - Go to Settings → Capabilities
   - Click "Upload skill" in the Skills section
   - Select your ZIP file

**Security Note:** The packaged ZIP contains your API key. Do not share it publicly or commit it to version control.

## API Reference

### SkillsMP (Curated, API Key Required)

**Keyword Search**
```bash
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=debugging&limit=20&sortBy=recent" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY"
```

**AI Semantic Search**
```bash
curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q=help+me+debug+code" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY"
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "skills": [
      {
        "id": "skill-id",
        "name": "code-debugging",
        "author": "AuthorName",
        "description": "Systematic debugging methodology...",
        "githubUrl": "https://github.com/user/repo/tree/main/skills/code-debugging",
        "stars": 15,
        "updatedAt": 1768838561
      }
    ]
  }
}
```

### SkillHub (Community, No API Key Required)

**Search Skills**
```bash
curl -X GET "https://skills.palebluedot.live/api/skills?q=debugging&limit=20"
```

**Get Skill Details (required before install)**
```bash
curl -X GET "https://skills.palebluedot.live/api/skills/{id}"
```

**Response Format (Search):**
```json
{
  "skills": [
    {
      "id": "wshobson/agents/debugging-strategies",
      "name": "debugging-strategies",
      "description": "Master systematic debugging...",
      "githubOwner": "wshobson",
      "githubRepo": "agents",
      "githubStars": 27021,
      "securityScore": 100
    }
  ],
  "pagination": { "page": 1, "limit": 20, "total": 1000 }
}
```

### ClawHub (Versioned, Semantic Search, No API Key Required)

**Semantic Search**
```bash
curl -X GET "https://clawhub.ai/api/v1/search?q=debugging&limit=20"
```

**Browse by Stars**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills?limit=20&sort=stars"
```

**Get Skill Details**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/{slug}"
```

**Get Skill File (raw text, NOT JSON)**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/{slug}/file?path=SKILL.md"
```

**Response Format (Search):**
```json
{
  "results": [
    {
      "score": 0.82,
      "slug": "self-improving-agent",
      "displayName": "Self-Improving Agent",
      "summary": "An agent that iteratively improves itself...",
      "version": "1.0.0",
      "updatedAt": "2026-01-15T10:30:00Z"
    }
  ]
}
```

**Key Differences:** ClawHub hosts skill files directly (not on GitHub), uses slug-based identifiers, supports semantic/vector search, and includes explicit version numbers. Rate limit: 120 reads/min per IP.

## Repository Structure

```
universal-skills-manager/
├── install.sh                       # One-liner installer script
├── README.md                        # This file
├── CHANGELOG.md                     # Version history
├── CLAUDE.md                        # Claude Code context file
├── specs.md                         # Technical specification
├── assets/
│   └── mascot.png                   # Project mascot image
├── docs/
│   ├── SECURITY_SCANNING.md         # Security scanner reference
│   ├── scan_skill-security-analysis.md  # Full security analysis of scanner
│   └── remediation-final-code-review.md # Code review of security hardening
├── tests/
│   ├── conftest.py                  # Test fixtures
│   └── test_scan_skill.py           # Scanner test suite (62 tests)
├── SECURITY.md                      # Security policy and vulnerability reporting
└── universal-skills-manager/        # The skill itself
    ├── SKILL.md                     # Skill definition and logic
    ├── config.json                  # API key config template
    └── scripts/
        ├── install_skill.py         # Helper script for downloading skills
        └── scan_skill.py            # Security scanner (20+ detection categories)
```

## Contributing

Skills are sourced from the community via [SkillsMP.com](https://skillsmp.com), [SkillHub](https://skills.palebluedot.live), and [ClawHub](https://clawhub.ai). To contribute:

1. Create your skill with proper YAML frontmatter
2. Host it on GitHub (for SkillsMP/SkillHub) or publish directly to ClawHub
3. Submit to SkillsMP.com for curated indexing, let SkillHub auto-index from GitHub, or publish via ClawHub's platform

## License

MIT License - See repository for details

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/jacob-bd/universal-skills-manager/issues)
- **SkillsMP**: Visit [skillsmp.com](https://skillsmp.com) for curated skill discovery
- **SkillHub**: Visit [skills.palebluedot.live](https://skills.palebluedot.live) for community skills
- **ClawHub**: Visit [clawhub.ai](https://clawhub.ai) for versioned skills with semantic search
- **Documentation**: See `CLAUDE.md` for technical details

---

**Note**: This skill requires an active internet connection to search SkillsMP.com / SkillHub / ClawHub and fetch skill content from GitHub or ClawHub.

## Acknowledgments

This skill was inspired by the [skill-lookup](https://skillsmp.com/skills/f-prompts-chat-plugins-claude-prompts-chat-skills-skill-lookup-skill-md) skill by f-prompts.

Special thanks to [@ben-alkov](https://github.com/ben-alkov) for the comprehensive security analysis and hardening of `scan_skill.py` (PR #2).

