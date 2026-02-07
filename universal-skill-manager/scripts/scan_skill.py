#!/usr/bin/env python3
"""
Universal Skill Scanner

A zero-dependency security scanner for AI skill packages. Analyzes SKILL.md
files and supporting scripts for potential security risks including prompt
injection, credential exfiltration, invisible unicode, and other threats.

Usage:
    python3 scan_skill.py <path>            # Scan a skill directory or file
    python3 scan_skill.py --pretty <path>   # Pretty-print the JSON report
    python3 scan_skill.py --version         # Print version and exit

Exit codes:
    0 - Clean (no findings)
    1 - Info-level findings only
    2 - Warning-level findings present
    3 - Critical-level findings present

Output:
    JSON report to stdout with fields:
        skill_path, files_scanned, scan_timestamp,
        summary (critical, warning, info counts),
        findings (list of finding objects)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"


class Finding:
    """Represents a single security finding from the scan."""

    def __init__(self, severity, category, file, line, description, matched_text, recommendation):
        self.severity = severity
        self.category = category
        self.file = file
        self.line = line
        self.description = description
        self.matched_text = matched_text
        self.recommendation = recommendation

    def to_dict(self):
        return {
            "severity": self.severity,
            "category": self.category,
            "file": self.file,
            "line": self.line,
            "description": self.description,
            "matched_text": self.matched_text,
            "recommendation": self.recommendation,
        }


class SkillScanner:
    """Scans skill directories and files for security issues."""

    def __init__(self):
        self.findings = []
        self.files_scanned = []

    def scan_path(self, path):
        """Scan a file or directory and return a JSON-serializable report dict."""
        path = Path(path).resolve()

        if path.is_file():
            self._scan_file(path, path.parent)
        elif path.is_dir():
            for root, _dirs, files in os.walk(path):
                for fname in sorted(files):
                    file_path = Path(root) / fname
                    self._scan_file(file_path, path)
        else:
            print(f"Error: path does not exist: {path}", file=sys.stderr)
            sys.exit(1)

        return self._build_report(str(path))

    def _scan_file(self, file_path, base_path):
        """Read a file, determine its type, and call appropriate check methods."""
        file_path = Path(file_path)
        relative = str(file_path.relative_to(base_path))

        # Skip binary files and hidden files
        if file_path.name.startswith("."):
            return

        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError, OSError):
            return

        self.files_scanned.append(relative)
        lines = content.splitlines()
        suffix = file_path.suffix.lower()

        # All files: invisible unicode check
        self._check_invisible_unicode(lines, relative)

        # Markdown files: all categories
        if suffix == ".md":
            self._check_all_categories(lines, relative)

        # Script files: subset of checks
        elif suffix in (".py", ".sh", ".bash"):
            self._check_exfiltration_urls(lines, relative)
            self._check_credential_references(lines, relative)
            self._check_command_execution(lines, relative)
            self._check_shell_pipe_execution(lines, relative)
            self._check_encoded_content(lines, relative)

        # Config files: subset of checks
        elif suffix in (".json", ".yaml", ".yml"):
            self._check_exfiltration_urls(lines, relative)
            self._check_credential_references(lines, relative)
            self._check_encoded_content(lines, relative)

    def _check_all_categories(self, lines, file):
        """Run all check categories against the given lines (used for .md files)."""
        self._check_exfiltration_urls(lines, file)
        self._check_shell_pipe_execution(lines, file)
        self._check_credential_references(lines, file)
        self._check_external_url_references(lines, file)
        self._check_command_execution(lines, file)
        self._check_instruction_override(lines, file)
        self._check_role_hijacking(lines, file)
        self._check_safety_bypass(lines, file)
        self._check_html_comments(lines, file)
        self._check_encoded_content(lines, file)
        self._check_prompt_extraction(lines, file)
        self._check_delimiter_injection(lines, file)
        self._check_cross_skill_escalation(lines, file)

    def _check_invisible_unicode(self, lines, file):
        """Check for invisible or zero-width unicode characters."""
        pass

    def _check_exfiltration_urls(self, lines, file):
        """Check for URLs that may exfiltrate data to external servers."""
        pass

    def _check_shell_pipe_execution(self, lines, file):
        """Check for shell commands piped from remote sources."""
        pass

    def _check_credential_references(self, lines, file):
        """Check for references to credentials, tokens, or API keys."""
        pass

    def _check_external_url_references(self, lines, file):
        """Check for external URL references that may fetch untrusted content."""
        pass

    def _check_command_execution(self, lines, file):
        """Check for dangerous command execution patterns."""
        pass

    def _check_instruction_override(self, lines, file):
        """Check for attempts to override system instructions."""
        pass

    def _check_role_hijacking(self, lines, file):
        """Check for role/persona hijacking attempts."""
        pass

    def _check_safety_bypass(self, lines, file):
        """Check for attempts to bypass safety measures."""
        pass

    def _check_html_comments(self, lines, file):
        """Check for hidden instructions in HTML comments."""
        pass

    def _check_encoded_content(self, lines, file):
        """Check for base64 or other encoded content that may hide payloads."""
        pass

    def _check_prompt_extraction(self, lines, file):
        """Check for attempts to extract system prompts or instructions."""
        pass

    def _check_delimiter_injection(self, lines, file):
        """Check for delimiter injection attacks."""
        pass

    def _check_cross_skill_escalation(self, lines, file):
        """Check for attempts to escalate privileges across skills."""
        pass

    def _add_finding(self, severity, category, file, line, description, matched_text, recommendation):
        """Add a finding to the findings list."""
        finding = Finding(
            severity=severity,
            category=category,
            file=file,
            line=line,
            description=description,
            matched_text=matched_text,
            recommendation=recommendation,
        )
        self.findings.append(finding)

    def _build_report(self, skill_path):
        """Build and return the JSON report dict."""
        critical_count = sum(1 for f in self.findings if f.severity == "critical")
        warning_count = sum(1 for f in self.findings if f.severity == "warning")
        info_count = sum(1 for f in self.findings if f.severity == "info")

        return {
            "skill_path": skill_path,
            "files_scanned": list(self.files_scanned),
            "scan_timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "critical": critical_count,
                "warning": warning_count,
                "info": info_count,
            },
            "findings": [f.to_dict() for f in self.findings],
        }


def exit_code_from_report(report):
    """Determine the exit code based on the report summary."""
    summary = report["summary"]
    if summary["critical"] > 0:
        return 3
    if summary["warning"] > 0:
        return 2
    if summary["info"] > 0:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Scan AI skill packages for security issues."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to a skill directory or file to scan",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output with indentation",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit",
    )

    args = parser.parse_args()

    if args.version:
        print(f"scan_skill.py {VERSION}")
        sys.exit(0)

    if not args.path:
        parser.error("the following arguments are required: path")

    scanner = SkillScanner()
    report = scanner.scan_path(args.path)

    indent = 2 if args.pretty else None
    print(json.dumps(report, indent=indent))

    sys.exit(exit_code_from_report(report))


if __name__ == "__main__":
    main()
