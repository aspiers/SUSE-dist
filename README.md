# Adam's SUSE-specific configuration files and utilities

This is my collection of miscellaneous configuration files, utilities
etc. which are specific to SUSE-based distributions.

## Contents

* [plugins](http://en.opensuse.org/openSUSE:OSC_plugins) for [`osc`](http://en.opensuse.org/openSUSE:OSC)
    * [`osc-prdiff.py`](https://github.com/aspiers/SUSE-dist/blob/master/.osc-plugins/osc-prdiff.py) - server-side diff of two projects
    * [`osc-classify-link.py`](https://github.com/aspiers/SUSE-dist/blob/master/.osc-plugins/osc-classify-link.py) - distinguish between projects which have been branched / linkpac'd / copypac'd / aggregatepac'd.
* files to make it easier to inspect files gathered into a [supportconfig](http://www.novell.com/communities/node/2332/supportconfig-linux) tarball.
    *   [`split-supportconfig`](https://github.com/aspiers/SUSE-dist/blob/master/bin/split-supportconfig) - extracts snapshots of any config file / log file etc. which is embedded inside a `.txt` file within the supportconfig.  For example `plugin-susecloud.txt` contains many files such as `var/log/crowbar/install.log`, which will be extracted to `rootfs/var/log/crowbar/install.log`.
    *   [`unpack-supportconfig`](https://github.com/aspiers/SUSE-dist/blob/master/bin/unpack-supportconfig) - a wrapper around `split-supportconfig` which unpacks the tarball, runs `split-supportconfig *.txt`, and optionally deletes the packed tarball.  Requires the [`up`](https://github.com/aspiers/shell-env/blob/master/bin/up) utility for handling the tarball unpacking - so install that somewhere on your `$PATH` before use.
    *   [`supportconfig-tmux`](https://github.com/aspiers/SUSE-dist/blob/master/bin/supportconfig-tmux) - a wrapper around `unpack-supportconfig` which additionally creates a new `tmux` session with a window for viewing each of the log files which you most commonly look at.
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
