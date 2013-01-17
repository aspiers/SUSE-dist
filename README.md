# Adam's SUSE-specific configuration files and utilities

This is my collection of miscellaneous configuration files, utilities
etc. which are specific to SUSE-based distributions.

## Contents

* [plugins](http://en.opensuse.org/openSUSE:OSC_plugins) for [`osc`](http://en.opensuse.org/openSUSE:OSC)
    * [`osc-prdiff.py`](https://github.com/aspiers/SUSE-dist/blob/master/.osc-plugins/osc-prdiff.py) - server-side diff of two projects
    * [`osc-classify-link.py`](https://github.com/aspiers/SUSE-dist/blob/master/.osc-plugins/osc-classify-link.py) - distinguish between projects which have been branched / linkpac'd / copypac'd / aggregatepac'd.

* other stuff I haven't listed yet :)

## <a name="install">INSTALLATION</a>

This repository is designed to be [stowed](http://www.gnu.org/software/stow/)
directly into your home directory:

    git clone git://github.com/aspiers/SUSE-dist.git
    stow -d . -t ~ SUSE-dist

However if you only want to cherry-pick bits and pieces then you can
easily just copy or symlink them in manually.

## LICENSE

The software in this repository is free software: except where noted
otherwise, you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any
later version.

This software is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
