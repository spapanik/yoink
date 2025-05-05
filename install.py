#!/usr/bin/env python
import json
from pathlib import Path

base_dir = Path(__file__).parent
package_path = base_dir.joinpath("data", "packages.json")
install_path = base_dir.joinpath("out", "install.sh")

packages = json.load(package_path.open())
aur = " ".join(packages["aur"])
pacman = " ".join(packages["pacman"])
uv = "\n".join(f"uv tool install --python 3.13 {package}" for package in packages["uv"])

script = f"""#!/usr/bin/env bash

echo "Updating keyring..."
sudo pacman -Sy --needed archlinux-keyring

echo "Installing system packages..."
sudo pacman -Syu --needed {pacman}

echo "Installing AUR packages..."
yay -Syu --needed {aur}

echo "Installing pipx packages..."
{uv}

echo "Adding user to docker group..."
sudo usermod -aG docker $USER
"""

install_path.parent.mkdir(exist_ok=True)
install_path.write_text(script)
install_path.chmod(0o755)
