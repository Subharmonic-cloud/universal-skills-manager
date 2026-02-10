from scan_skill import SkillScanner


def test_scanner_empty_dir(scanner, tmp_skill):
    """Scanning an empty directory produces a clean report."""
    report = scanner.scan_path(tmp_skill.base)
    assert report["summary"]["critical"] == 0
    assert report["summary"]["warning"] == 0
    assert report["summary"]["info"] == 0
    assert report["findings"] == []


# --- Task 1.2: Symlink protection (C1) ---


def test_symlink_file_is_skipped(scanner, tmp_skill):
    """Symlinked files must not be scanned."""
    real = tmp_skill.add_file("real.md", "safe content")
    tmp_skill.add_symlink("link.md", real)
    report = scanner.scan_path(tmp_skill.base)
    assert "link.md" not in report["files_scanned"]


def test_symlink_directory_not_followed(scanner, tmp_path):
    """Symlinked directories must not be traversed."""
    # Create skill dir and outside dir as siblings under tmp_path
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_text("secret data", encoding="utf-8")

    # Symlink from inside skill dir to outside dir
    (skill_dir / "sneaky").symlink_to(outside)

    report = scanner.scan_path(skill_dir)
    assert not any("secret" in f for f in report["files_scanned"])


def test_path_escape_blocked(scanner, tmp_skill, tmp_path):
    """Files resolving outside base_path must not be scanned."""
    outside_file = tmp_path / "outside.md"
    outside_file.write_text("outside content", encoding="utf-8")
    tmp_skill.add_symlink("escape.md", outside_file)

    report = scanner.scan_path(tmp_skill.base)
    assert "escape.md" not in report["files_scanned"]
