# zsmtool

Command line tool to analyze and edit ZSound ZSM files

You can use this tool to decompile ZSound `.zsm` files to `.yml` format for inspection.  Edits can be made to the `.yml` files and `zsmtool` can compile the `.yml` back into `.zsm`.

Additionally, zsmtool can convert standard MIDI files to ZSM MIDI event data.  This does not convert the MIDI data to YM2151 or PSG events, but rather the MIDI events are embedded in EXTCMD blocks that ZSMKit can play on a Commander X16 with a MIDI or wavetable card.

## Synopsis

```
usage: zsmtool [-h] [-m input.mid | -i input.zsm | -c input.yaml] [-o output.zsm | -d output.yaml]

options:
  -h, --help      show this help message and exit
  -m input.mid    Input MIDI file
  -i input.zsm    Input ZSM file
  -c input.yaml   Input YAML file
  -o output.zsm   Output ZSM file
  -d output.yaml  Output YAML file
```
## Requirements
* Python 3.8 or later
* `ruamel.yaml` and `mido` - most Linux distributions have these modules in their package repos
    * Ubuntu/Debian: `sudo apt install python3-ruamel.yaml python3-mido`
    * RHEL/Rocky/Fedora: `sudo dnf install python3-ruamel-yaml python3-mido`
    * Gentoo: `sudo emerge -av dev-python/ruamel-yaml dev-python/mido`
    * Arch: `sudo pacman -S python-ruamel-yaml python-mido`
    * MSYS2 and Linux distros which are missing either of ruamel-yaml or mido
      * MSYS2 does not depend on python being installed, so you may have to explicitly install it.
        * `pacman -S python` &lt;- for MSYS2
      * Create a virtualenv, and install the modules within the venv, like this:
        * `mkdir zsmtoolvenv`
        * `cd zsmtoolvenv`
        * `python -mvenv .`
        * `. ./bin/activate`
        * `pip3 install mido ruamel-yaml`
      * `zsmtool` will run as long as you're in a shell that has had the `activate` file sourced using the `.` operator as above.
