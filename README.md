# zsmtool

Command line tool to analyze and edit ZSound ZSM files

You can use this tool to decompile ZSound `.zsm` files to `.yml` format for inspection.  Edits can be made to the `.yml` files and `zsmtool` can compile the `.yml` back into `.zsm`.

## Synopsis

```
usage: zsmtool [-h] [-i input.zsm | -c input.yml] [-o output.zsm | -d output.yml]

options:
  -h, --help     show this help message and exit
  -i input.zsm   Input ZSM file
  -c input.yml   Compile structured text to ZSM
  -o output.zsm  Output ZSM file
  -d output.yml  Decompile a ZSM to structured text
```
## Requirements
* Python 3.8 or later
* ruamel.yaml - most Linux distributions have this module in their package repos
    * Ubuntu/Debian: `sudo apt install python3-ruamel.yaml`
    * RHEL/Rocky/Fedora: `sudo dnf install python3-ruamel-yaml`
    * Gentoo: `sudo emerge -av dev-python/ruamel-yaml`
    * Arch: `sudo pacman -S python-ruamel-yaml`