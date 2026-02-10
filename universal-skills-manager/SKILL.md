---
name: universal-skills-manager
description: The master coordinator for AI skills. Discovers skills from multiple sources (SkillsMP.com and SkillHub), manages installation, and synchronization across Claude Code, Gemini CLI, Google Anti-Gravity, OpenCode, and other AI tools. Handles User-level (Global) and Project-level (Local) scopes.
---

<!-- Version: 1.3.0 -->

# Universal Skills Manager

This skill empowers the agent to act as a centralized package manager for AI capabilities. It discovers skills from multiple sources — SkillsMP.com (curated, AI semantic search) and SkillHub (173k+ community skills, no API key required) — and unifies skill management across multiple AI tools (Claude Code, Gemini, Anti-Gravity, OpenCode, Cursor, etc.), ensuring consistency and synchronization.

## When to Use This Skill

Activate this skill when the user:
- Wants to **find or search** for new skills.
- Wants to **install** a skill (from a search result or local file).
- Wants to **sync** skills between different AI tools (e.g., "Copy this Gemini skill to OpenCode").
- Asks to **move or copy** skills between scopes (User vs. Project).
- Mentions "Google Anti-Gravity", "OpenCode", or "Gemini" in the context of skills/extensions.
- Wants to **package this skill for claude.ai or Claude Desktop** (ZIP upload).

## Supported Ecosystem

This skill manages the following tools and scopes. Always verify these paths exist before acting.

| Tool | User Scope (Global) | Project Scope (Local) |
| :--- | :--- | :--- |
| **Gemini CLI** | `~/.gemini/skills/` | `./.gemini/skills/` |
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` | `./.antigravity/extensions/` |
| **OpenCode** | `~/.config/opencode/skills/` | `./.opencode/skills/` |
| **OpenClaw** | `~/.openclaw/workspace/skills/` | `./.openclaw/skills/` |
| **Claude Code** | `~/.claude/skills/` | `./.claude/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `./.codex/skills/` |
| **block/goose** | `~/.config/goose/skills/` | `./.goose/agents/` |
| **Roo Code** | `~/.roo/skills/` | `./.roo/skills/` |
| **Cursor** | `~/.cursor/extensions/` | `./.cursor/extensions/` |

**claude.ai / Claude Desktop (ZIP Upload Required):**

| Platform | Installation Method |
| :--- | :--- |
| **claude.ai** | Upload ZIP via Settings → Capabilities → Upload Skill |
| **Claude Desktop** | Upload ZIP via Settings → Capabilities → Upload Skill |

*Note: claude.ai and Claude Desktop don't have access to local environment variables. Use the "Package for claude.ai/Desktop" capability (Section 5) to embed your API key in the ZIP.*

**IMPORTANT - Universal Skills Manager Platform Limitations:**

This skill (Universal Skills Manager) requires network access to call the SkillsMP API, SkillHub API, and GitHub. Handle these scenarios:

- **If user asks to package/ZIP the Universal Skills Manager itself for claude.ai:**
  Tell the user: "The Universal Skills Manager won't work on claude.ai because it requires network access to call the SkillsMP API, SkillHub API, and GitHub APIs. claude.ai's code execution environment doesn't allow outbound network requests. However, I can package OTHER skills for claude.ai upload - those will work as long as they don't require network access."

- **If user wants to try the Universal Skills Manager on Claude Desktop with Coworker:**
  Tell the user: "Claude Desktop with Coworker has network access capabilities. To use the Universal Skills Manager there, you may need to extend network access to these domains in your Cowork settings:
  - `skillsmp.com` (for SkillsMP skill searches)
  - `skills.palebluedot.live` (for SkillHub skill searches)
  - `api.github.com` and `raw.githubusercontent.com` (for skill downloads)
  
  This is experimental - Cowork's default network access is restricted. Check your Cowork network egress settings."

*(Note: If a tool uses a different directory structure, ask the user to confirm the path, then remember it using `save_memory`.)*

## Core Capabilities

### 1. Smart Installation & Synchronization
**Trigger:** User asks to install a skill (e.g., "Install the debugging skill" or "Install skill ID xyz").

**Procedure:**
1.  **Identify Source:**
    *   If from SkillsMP search result: Use the `githubUrl` from the API response
    *   If from SkillHub search result: Fetch skill details via `/api/skills/{id}` to get `skillPath` and `branch`, then construct GitHub tree URL
    *   If from skill name/ID: Search available sources (SkillsMP and/or SkillHub) to find the skill
    *   If local: Identify the source path
2.  **Verify Repository Structure (CRITICAL):**
    *   Before downloading, browse the GitHub repo to confirm the skill folder location
    *   Use GitHub API to list directory contents: `GET /repos/{owner}/{repo}/contents?ref={branch}`
    *   Look for folders containing `SKILL.md` - this is the actual skill directory
    *   Common patterns: `skill/`, `skills/{name}/`, root level, or custom folder names
    *   Confirm the correct path before generating the download URL
3.  **Download Using Helper Script:**
    *   Use `install_skill.py` (located in this skill's `scripts/` folder):
    ```bash
    python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
      --url "https://github.com/{owner}/{repo}/tree/{branch}/{skill-folder}" \
      --dest "{target-path}" \
      --dry-run  # Preview first, then remove flag to install
    ```
    *   The script handles: atomic install, validation, subdirectories, safety checks
    *   **Safety feature**: Script will abort (exit code 4) if destination is a root skills directory
    *   **Update detection**: If skill exists, shows diff and prompts for confirmation
    *   **Security scan**: The install script automatically scans downloaded skills for security threats (invisible characters, data exfiltration, prompt injection). Review any findings before proceeding.
4.  **Determine Primary Target:**
    *   Ask: "Should this be installed Globally (User) or Locally (Project)?"
    *   Determine the primary tool (e.g., if user is in Claude Code, Claude is primary)
5.  **The "Sync Check" (CRITICAL):**
    *   **Scan:** Check if other supported tools are installed on the system (look for their config folders)
    *   **Propose:** "I see you also have OpenCode and Cursor installed. Do you want to sync this skill to them as well?"
6.  **Execute:**
    *   Run the install script for each target location
    *   Ensure the standard structure is maintained
7.  **Report Success:**
    *   Show installed skill name, author, and location(s)
    *   Display GitHub URL and stars count for reference

### 2. The "Updates & Consistency" Check
**Trigger:** User modifies a skill or asks to "sync" skills.

**Procedure:**
1.  **Compare:** Check the modification times or content of the skill across all installed locations.
2.  **Report:** "The 'code-review' skill in Gemini is newer than the one in OpenCode."
3.  **Action:** Offer to overwrite older versions with the newer version to ensure consistency.

### 3. Skill Discovery (Multi-Source)
**Trigger:** User searches for skills (e.g., "Find a debugging skill" or "Search for React skills").

**Procedure:**
1.  **Discover API Key and Select Source:**
    *   **Step 1 - Environment Variable:** Check `$SKILLSMP_API_KEY`
        ```bash
        echo $SKILLSMP_API_KEY
        ```
        If set and non-empty, use SkillsMP as the primary search source.

    *   **Step 2 - Config File:** Check for `config.json` in this skill's directory
        ```bash
        # Look for config.json in skill directory (path varies by tool)
        cat ~/.claude/skills/universal-skills-manager/config.json 2>/dev/null
        ```
        If `skillsmp_api_key` field has a non-empty value, use SkillsMP as primary source.

    *   **Step 3 - Source Selection:** If no API key found, present the user with a choice:
        > "I don't see a SkillsMP API key configured. You have two options:
        >
        > A) Provide your SkillsMP API key (get one at skillsmp.com) — this gives you access to curated skills with AI semantic search
        >
        > B) Search SkillHub's open catalog instead — 173k+ community skills, no API key needed
        >
        > Which would you prefer?"

        -   If user chooses **A**: Collect key, store in memory for this session, proceed with SkillsMP
        -   If user chooses **B**: Proceed with SkillHub search (no key needed)

    *   **Security:** Never log, display, or echo the full API key value.

    **Note for claude.ai/Desktop users:** Environment variables are not available. Use the "Package for claude.ai/Desktop" capability (Section 5) to create a ZIP with your API key embedded, or provide your key when prompted.

2.  **Execute Search Based on Selected Source:**

    **If using SkillsMP (primary, curated):**
    -   **Choose method:**
        -   **Keyword Search** (`/api/v1/skills/search`): For specific terms, exact matches
        -   **AI Semantic Search** (`/api/v1/skills/ai-search`): For natural language queries (e.g., "help me debug code")
    -   **Execute:**
        ```bash
        # Keyword Search
        curl -X GET "https://skillsmp.com/api/v1/skills/search?q={query}&limit=20&sortBy=recent" \
          -H "Authorization: Bearer $SKILLSMP_API_KEY"

        # AI Semantic Search (for natural language queries)
        curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q={query}" \
          -H "Authorization: Bearer $SKILLSMP_API_KEY"
        ```
    -   **Parse:** Extract from `data.skills[]` (keyword) or `data.data[]` (AI search)
    -   Available fields: `id`, `name`, `author`, `description`, `githubUrl`, `skillUrl`, `stars`, `updatedAt`

    **If using SkillHub (open catalog, no auth):**
    -   **Execute:**
        ```bash
        # SkillHub Search (no authentication required)
        curl -X GET "https://skills.palebluedot.live/api/skills?q={query}&limit=20"
        ```
    -   **Parse:** Extract from `skills[]` array
    -   Available fields: `id`, `name`, `description`, `githubOwner`, `githubRepo`, `githubStars`, `downloadCount`, `securityScore`
    -   **Note:** SkillHub does not have an AI semantic search — keyword search only

3.  **Display Results (Unified Format):**
    Display results in a consistent table format regardless of source. Include the **Source** column to indicate origin:

    ```
    | # | Skill | Author | Stars | Source | Description |
    |---|-------|--------|-------|--------|-------------|
    | 1 | debugging-strategies | wshobson | 27,021 | SkillHub | Master systematic debugging... |
    | 2 | code-debugging | AuthorX | 15 | SkillsMP | Systematic debugging methodology... |
    ```

    -   For SkillsMP AI search: Also show relevance score
    -   For SkillHub: Show `securityScore` if available
    -   Limit to top 10-15 results for readability

4.  **Search More Sources (For SkillsMP Users):**
    When the user has a SkillsMP API key and searched SkillsMP first, offer to expand the search:

    > "Want to also search SkillHub's community catalog for more results?"

    If yes:
    -   Query SkillHub API with the same search terms
    -   **Deduplicate:** Compare results by full skill ID (`{owner}/{repo}/{path}`) to avoid showing the same skill from both sources
    -   Append unique SkillHub results to the display, labeled with `[SkillHub]` source

5.  **Offer Installation:**
    -   After displaying results, ask: "Which skill would you like to install?"
    -   For SkillsMP results: Note the skill's `githubUrl` for content fetching
    -   For SkillHub results: Note the skill's `id` for detail fetching (needed to get `skillPath` and `branch`)

### 4. Skill Matrix Report
**Trigger:** User asks for skill report/overview (e.g., "Show my skills", "What skills do I have?", "Skill report", "Compare my tools").

**Procedure:**
1.  **Detect Installed Tools:**
    Check which AI tools are installed by verifying their user-level skills directories exist:
    ```bash
    # Check each tool's skills directory
    ls -d ~/.claude/skills 2>/dev/null && echo "Claude: ✓"
    ls -d ~/.codex/skills 2>/dev/null && echo "Codex: ✓"
    ls -d ~/.gemini/skills 2>/dev/null && echo "Gemini: ✓"
    ls -d ~/.gemini/antigravity/skills 2>/dev/null && echo "Antigravity: ✓"
    ls -d ~/.openclaw/workspace/skills 2>/dev/null && echo "OpenClaw: ✓"
    ls -d ~/.cursor/extensions 2>/dev/null && echo "Cursor: ✓"
    ls -d ~/.config/opencode/skills 2>/dev/null && echo "OpenCode: ✓"
    ls -d ~/.roo/skills 2>/dev/null && echo "Roo: ✓"
    ls -d ~/.config/goose/skills 2>/dev/null && echo "Goose: ✓"
    ```

2.  **Collect All Skills:**
    For each detected tool, list skill folders:
    ```bash
    find ~/.{claude,codex,gemini,gemini/antigravity,openclaw/workspace,config/opencode,config/goose,roo}/skills -maxdepth 1 -type d 2>/dev/null | \
      xargs -I{} basename {} | sort -u
    ```

3.  **Generate Matrix Table:**
    Create a markdown table where:
    - **Rows** = skill names (deduplicated across all tools)
    - **Columns** = only tools that are installed on the system
    - **Cells** = ✅ (installed) or ❌ (not installed)

    Example output:
    ```
    | Skill | Claude | Codex | Gemini |
    |-------|--------|-------|--------|
    | humanizer | ✅ | ❌ | ✅ |
    | skill-creator | ❌ | ✅ | ❌ |
    | using-superpowers | ✅ | ✅ | ✅ |
    ```

4.  **Show Summary:**
    - Total skills across all tools
    - Skills unique to one tool
    - Skills installed everywhere

### 5. Package for claude.ai / Claude Desktop

**Trigger:** User wants to use this skill in claude.ai or Claude Desktop (e.g., "Package this for claude.ai", "Create a ZIP for Claude Desktop", "I want to upload this skill to claude.ai", "Prepare skill for web upload").

**Procedure:**
1.  **Explain the Process:**
    "I'll create a ZIP file with this skill ready for upload to claude.ai or Claude Desktop. Since cloud environments don't have access to your local environment variables, I'll embed your API key in the package."

2.  **Collect API Key:**
    *   Ask: "Please provide your SkillsMP API key. You can get one at https://skillsmp.com"
    *   Wait for user to provide the key
    *   **Security:** Do not echo or display the key back to the user

3.  **Create Package Contents:**
    *   Create a temporary directory structure:
        ```
        universal-skills-manager/
        ├── SKILL.md          # Copy from current skill
        ├── config.json       # Create with embedded API key
        └── scripts/
            └── install_skill.py  # Copy from current skill
        ```
    *   Generate `config.json` with the user's API key:
        ```json
        {
          "skillsmp_api_key": "USER_PROVIDED_KEY_HERE"
        }
        ```

4.  **Create ZIP File:**
    *   Use Python to create the ZIP:
        ```python
        import zipfile
        import json
        import tempfile
        from pathlib import Path
        
        # Create ZIP in user's Downloads or current directory
        zip_path = Path.home() / "Downloads" / "universal-skills-manager.zip"
        skill_dir = Path("~/.claude/skills/universal-skills-manager").expanduser()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy skill files
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file() and file_path.name != 'config.json':
                    rel_path = file_path.relative_to(skill_dir)
                    dest = temp_path / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(file_path.read_bytes())
            
            # Create config.json with API key
            config = {"skillsmp_api_key": "USER_API_KEY"}
            (temp_path / "config.json").write_text(json.dumps(config, indent=2))
            
            # Create ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = f"universal-skills-manager/{file_path.relative_to(temp_path)}"
                        zf.write(file_path, arcname)
        ```
    *   Alternatively, provide the ZIP as a downloadable artifact

5.  **Provide Upload Instructions:**
    *   "Your skill package is ready! To use it:"
    *   "1. Download the ZIP file: `universal-skills-manager.zip`"
    *   "2. Go to claude.ai → Settings → Capabilities"
    *   "3. Scroll to Skills section and click 'Upload skill'"
    *   "4. Select the ZIP file and upload"
    *   "5. Enable the skill and start using it!"

6.  **Security Reminder:**
    *   "Note: This ZIP contains your API key. Do not share it publicly or commit it to version control."

## Operational Rules

1.  **Structure Integrity:** When installing, always ensure the skill has its own folder (e.g., `.../skills/my-skill/`). Do not dump loose files into the root skills directory.
2.  **Conflict Safety:** If a skill already exists at a target location, **always** ask before overwriting, unless the user explicitly requested a "Force Sync."
3.  **OpenClaw Note:** OpenClaw may require a restart to pick up new skills if `skills.load.watch` is not enabled in `openclaw.json`. Warn the user of this after installation.
4.  **Cross-Platform Adaptation:**
    *   Gemini uses `SKILL.md`.
    *   If OpenCode or Anti-Gravity require a specific manifest (e.g., `manifest.json`), generate a basic one based on the `SKILL.md` frontmatter during installation.

## Available Tools
- `bash` (curl): Make API calls to SkillsMP.com and SkillHub (skills.palebluedot.live), fetch skill content from GitHub.
- `web_fetch`: Fetch skill content from GitHub raw URLs or SkillHub API (alternative to curl).
- `read_file` / `write_file`: Manage local skill files.
- `glob`: Find existing skills in local directories.

## Implementation Details

### Skill Structure
Skills typically contain:
- **SKILL.md** (required): Main instructions with frontmatter.
- **Reference docs**: Additional documentation files.
- **Scripts**: Helper scripts (Python, shell, etc.).
- **Config files**: JSON, YAML configurations.

### Installation Logic

#### A. Installing from SkillsMP API
1.  **Fetch Skill Content:**
    -   Convert `githubUrl` to raw content URL:
        ```
        Input:  https://github.com/{user}/{repo}/tree/{branch}/{path}
        Output: https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}/SKILL.md
        ```
    -   Fetch the SKILL.md content using curl or web_fetch

2.  **Create Directory:**
    -   Use skill `name` from API response for directory: `.../skills/{skill-name}/`
    -   Example: `.../skills/code-debugging/`

3.  **Save SKILL.md:**
    -   Write the fetched content to `SKILL.md` in the new directory
    -   Preserve the original YAML frontmatter and content

4.  **Handle Additional Files (Optional):**
    -   Check if GitHub repo has additional files (reference docs, scripts)
    -   Optionally fetch and save them to maintain complete skill package

5.  **Confirm:**
    -   Report: "Installed '{name}' by {author} to {path}"
    -   Show GitHub URL and stars count
    -   Offer sync to other AI tools

#### B. Installing from SkillHub
1.  **Fetch Skill Details:**
    -   Use the skill's `id` from the search result to get full details:
        ```bash
        curl -X GET "https://skills.palebluedot.live/api/skills/{id}"
        ```
    -   **IMPORTANT:** The `id` field (e.g., `wshobson/agents/debugging-strategies`) does NOT map to the file path within the repo. You MUST use the detail endpoint to get the actual `skillPath` and `branch`.
    -   Extract from response: `githubOwner`, `githubRepo`, `branch`, `skillPath`

2.  **Construct GitHub URL:**
    -   Build the GitHub tree URL from the detail response:
        ```
        https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}
        ```
    -   Example: `https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`

3.  **Download Using Helper Script:**
    -   From this point, the flow is identical to SkillsMP installation:
        ```bash
        python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
          --url "https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}" \
          --dest "{target-path}"
        ```

4.  **Confirm:**
    -   Report: "Installed '{name}' from SkillHub to {path}"
    -   Show GitHub URL and stars count
    -   Offer sync to other AI tools

#### C. Installing from Local Source (Sync/Copy)
1.  **Retrieve:** Read all files from the source directory.
2.  **Create Directory:** Create the target directory `.../skills/{slug}/`.
3.  **Save Files:** Copy all files to the new location, preserving filenames.

### SkillsMP API Configuration

**Base URL:** `https://skillsmp.com/api/v1`

**Authentication:**
```bash
Authorization: Bearer $SKILLSMP_API_KEY
```

**Available Endpoints:**
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}`
- `GET /api/v1/skills/ai-search?q={query}`

**Response Format (Keyword Search):**
```json
{
  "success": true,
  "data": {
    "skills": [
      {
        "id": "...",
        "name": "skill-name",
        "author": "AuthorName",
        "description": "...",
        "githubUrl": "https://github.com/user/repo/tree/main/path",
        "skillUrl": "https://skillsmp.com/skills/...",
        "stars": 10,
        "updatedAt": 1768838561
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 3601,
      "totalPages": 1801,
      "hasNext": true
    }
  }
}
```

**Response Format (AI Search):**
```json
{
  "success": true,
  "data": {
    "search_query": "...",
    "data": [
      {
        "file_id": "...",
        "filename": "...",
        "score": 0.656,
        "skill": {
          "id": "...",
          "name": "...",
          "author": "...",
          "description": "...",
          "githubUrl": "...",
          "skillUrl": "...",
          "stars": 0,
          "updatedAt": 1769542668
        }
      }
    ]
  }
}
```

**Error Handling:**
- `401`: Invalid or missing API key
- `400`: Missing required query parameter
- `500`: Internal server error

### SkillHub API Configuration

**Base URL:** `https://skills.palebluedot.live/api`

**Authentication:** None required (open API)

**Available Endpoints:**
- `GET /api/skills?q={query}&limit={20}` — Search skills by keyword
- `GET /api/skills/{id}` — Get full skill details (includes `skillPath`, `branch`, `rawContent`)
- `GET /api/categories` — List skill categories
- `GET /api/health` — Health check

**Search Response Format:**
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
      "downloadCount": 0,
      "securityScore": 100,
      "securityStatus": null,
      "rating": 0,
      "isVerified": false,
      "compatibility": { "platforms": [] }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000,
    "totalPages": 50
  },
  "searchEngine": "meilisearch",
  "processingTimeMs": 10
}
```

**Detail Response Format (GET /api/skills/{id}):**
```json
{
  "id": "wshobson/agents/debugging-strategies",
  "name": "debugging-strategies",
  "description": "...",
  "githubOwner": "wshobson",
  "githubRepo": "agents",
  "skillPath": "plugins/developer-essentials/skills/debugging-strategies",
  "branch": "main",
  "githubStars": 27021,
  "rawContent": "---\nname: debugging-strategies\n..."
}
```

**Key Fields for Installation:**
- `skillPath`: The actual directory path within the GitHub repo (CRITICAL — the `id` does NOT match the file path)
- `branch`: The branch name (e.g., `main`)
- `githubOwner` + `githubRepo`: Used to construct the GitHub URL
- `rawContent`: Full SKILL.md content (can be used as fallback if GitHub is unreachable)

**Error Handling:**
- `404`: Skill not found
- `500`: Internal server error

### Guidelines
-   **Multi-Source Search:** Use SkillsMP as the primary source when an API key is available. Offer SkillHub as an alternative or additional source.
-   **Prefer AI Search:** For natural language queries with SkillsMP, use `/ai-search` for better relevance. SkillHub only supports keyword search.
-   **Source Labeling:** Always label results with their source (`[SkillsMP]` or `[SkillHub]`) so users can distinguish curated from community skills.
-   **SkillHub Detail Lookup:** When installing from SkillHub, always fetch the detail endpoint first to get the correct `skillPath` and `branch`. Never try to parse the `id` field as a file path.
-   **Deduplication:** When showing results from both sources, deduplicate by the full skill ID (`{owner}/{repo}/{path}`) to avoid showing the same skill twice.
-   **Verify Content:** After fetching from GitHub, verify the SKILL.md has valid YAML frontmatter.
-   **Structure Integrity:** Maintain the `.../skills/{skill-name}/SKILL.md` structure.
-   **Syncing:** After installing a skill, offer to sync (copy) it to other detected AI tools.
-   **GitHub URLs:** Always convert tree URLs to raw.githubusercontent.com URLs for content fetching.
-   **Security:** Security scanning runs on all installs regardless of source (SkillsMP or SkillHub). SkillHub's `securityScore` is informational only — our own scan at install time is authoritative.