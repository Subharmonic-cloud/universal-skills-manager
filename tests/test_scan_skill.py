from scan_skill import SkillScanner


def test_scanner_empty_dir(scanner, tmp_skill):
    """Scanning an empty directory produces a clean report."""
    report = scanner.scan_path(tmp_skill.base)
    assert report["summary"]["critical"] == 0
    assert report["summary"]["warning"] == 0
    assert report["summary"]["info"] == 0
    assert report["findings"] == []
