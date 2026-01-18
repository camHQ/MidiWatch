# MidiWatch

[![Release](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/camHQ/MidiWatch/releases) [![License](https://img.shields.io/badge/license-GPL--3.0-green)](LICENSE) [![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/) ![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20GNU/Linux-orange)


## Overview

MidiWatch is a desktop application that visualizes incoming MIDI 1.0 messages in real-time from any MIDI source. It displays MIDI data in three formats: Human-readable, Hexadecimal, and Binary allowing you to inspect and understand MIDI data at different levels of abstraction. Captured MIDI data can be exported to CSV format for further analysis.


## Features

- **Multiple Data Formats** — Display MIDI data in Human-readable, Hexadecimal, and Binary formats
- **Message Type Identification** — Clearly identifies the type of each incoming MIDI message
- **Note Display** — Shows note names with octave numbers (e.g., C4, D#5)
- **CSV Export** — Export captured MIDI data to CSV format for analysis and archival

## Installation

### Windows

Download the latest Windows `.exe` installer from the [Releases page](https://github.com/camHQ/MidiWatch/releases) and run it.

> Note: Windows may show a SmartScreen warning because this installer is not digitally signed. This is normal for open-source software. Click "More info" then "Run anyway" to proceed with the installation.

### GNU/Linux

Download the latest GNU/Linux `.deb` package from the [Releases page](https://github.com/camHQ/MidiWatch/releases) and install it:

```shell
sudo apt install ./midiwatch-*-amd64.deb
```

### Install from Source

#### 1. Clone the repository

```shell
git clone https://github.com/camHQ/MidiWatch.git
cd MidiWatch
```

#### 2. Create a virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies

```shell
pip install -r requirements.txt
```

> Note: If the installation fails (often on Python 3.13+), you are missing build tools. Run this command and try again:
>
>```shell
>sudo apt install build-essential python3-dev libasound2-dev libjack-jackd2-dev pkg-config
>```

#### 4. Compile resources

```shell
pyside6-rcc midiwatch/gui/resources/resources.qrc -o midiwatch/gui/resources/resources_rc.py
```

#### 5. Run the application

```shell
python -m midiwatch
```

## Status

This project uses [Semantic Versioning](https://semver.org/).

## Source Code

[https://github.com/camHQ/MidiWatch](https://github.com/camHQ/MidiWatch)

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) file for details


