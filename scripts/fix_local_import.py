"""Połącz lokalny pakiet ze środowiskiem .venv bez plików .pth."""

import sysconfig
from pathlib import Path

root = Path(__file__).resolve().parents[1]
site_packages = Path(sysconfig.get_path("purelib"))
if root / ".venv" not in site_packages.parents:
    raise SystemExit("Uruchom: .venv/bin/python scripts/fix_local_import.py")
link = site_packages / "graph_cli"
target = root / "src" / "graph_cli"
if link.is_symlink():
    link.unlink()
elif link.exists():
    raise SystemExit(f"Istniejący katalog wymaga sprawdzenia: {link}")
link.symlink_to(target, target_is_directory=True)
print(f"Połączono: {link} -> {target}")
