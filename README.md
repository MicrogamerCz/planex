# Planex

A simple flatpak installer built for Plasma.

## Features

- An addon for Plasma desktop
- DE-agnostic (requires wlr layer shell protocol)
- Runs application after installing
- Can be collapsed into a notification for less distraction

## Installation

**Dependencies**: `pyside6 python-gobject, flatpak, appstream, libplasma, layer-shell-qt kirigami qt6-declarative`

**Arch**: `yay -S planex-git`

## TODOs

- KCM for cache reload config
- Python → C++ rewrite (better long-term maintanence, performance, less deps)
- Custom icon
- Blocking sleep when flatpak is installed (or even cache reloaded)
