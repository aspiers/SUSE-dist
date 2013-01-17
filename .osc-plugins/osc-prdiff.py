#!/usr/bin/env python

import re
import subprocess
import sys

def _get_branch_parent(self, prj):
    m = re.match('^home:[^:]+:branches:(.+)', prj)
    # OBS_Maintained is a special case
    if m and prj.find(':branches:OBS_Maintained:') == -1:
        return m.group(1)
    return None

def _get_project_packages(self, apiurl, project):
    return meta_get_packagelist(apiurl, project)

def _prdiff_skip_package(self, opts, pkg):
    if opts.exclude and re.search(opts.exclude, pkg):
        return True

    if opts.include and not re.search(opts.include, pkg):
        return True

    return False

def _prdiff_output_diff(self, opts, rdiff):
    if opts.diffstat:
        print
        p = subprocess.Popen("diffstat",
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             close_fds=True)
        p.stdin.write(rdiff)
        p.stdin.close()
        diffstat = "".join(p.stdout.readlines())
        print diffstat
    elif opts.unified:
        print
        print rdiff
        #run_pager(rdiff)

def _prdiff_output_matching_requests(self, opts, requests,
                                     srcprj, pkg):
    """
    Search through the given list of requests and output any
    submitrequests which target pkg and originate from srcprj.
    """
    for req in requests:
        for action in req.get_actions():
            if action.type != 'submit':
                continue

            if action.src_project != srcprj:
                continue

            if action.tgt_package != pkg:
                continue

            print
            print req.list_view()
            break

@cmdln.alias('projectdiff')
@cmdln.alias('projdiff')
@cmdln.option('-r', '--requests', action='store_true',
              help='show open requests for any packages with differences')
@cmdln.option('-e', '--exclude',  metavar='REGEXP', dest='exclude',
              help='skip packages matching REGEXP')
@cmdln.option('-i', '--include',  metavar='REGEXP', dest='include',
              help='only consider packages matching REGEXP')
@cmdln.option('-n', '--new-only', action='store_true',
              help='show packages only in the new project')
@cmdln.option('-o', '--old-only', action='store_true',
              help='show packages only in the old project')
@cmdln.option('-u', '--unified',  action='store_true',
              help='show full unified diffs of differences')
@cmdln.option('-d', '--diffstat', action='store_true',
              help='show diffstat of differences')

def do_prdiff(self, subcmd, opts, *args):
    """${cmd_name}: Server-side diff of two projects

    Compares two projects and either summarises or outputs the
    differences in full.  In the second form, a project is compared
    with one of its branches inside a home:$USER project (the branch
    is treated as NEWPRJ).  The home branch is optional if the current
    working directory is a checked out copy of it.

    Usage:
        osc prdiff [OPTIONS] OLDPRJ NEWPRJ
        osc prdiff [OPTIONS] [home:$USER:branch:$PRJ]

    ${cmd_option_list}
    """

    if len(args) > 2:
        raise oscerr.WrongArgs('Too many arguments.')

    if len(args) == 0:
        if os.path.exists(os.path.join(store, '_project')):
            newprj = Project('.', getPackageList=False).name
            oldprj = self._get_branch_parent(newprj)
            if oldprj is None:
                raise oscerr.WrongArgs('Current directory is not a valid home branch.')
        else:
            raise oscerr.WrongArgs('Current directory is not a project.')
    elif len(args) == 1:
        newprj = args[0]
        oldprj = self._get_branch_parent(newprj)
        if oldprj is None:
            raise oscerr.WrongArgs('Single-argument form must be for a home branch.')
    elif len(args) == 2:
        oldprj, newprj = args
    else:
        raise RuntimeError('BUG in argument parsing, please report.\n'
                           'args: ' + repr(args))

    if opts.diffstat and opts.unified:
        print >>sys.stderr, 'error - cannot specify both --diffstat and --unified'
        sys.exit(1)

    apiurl = self.get_api_url()
    conf.get_config()

    new_packages = self._get_project_packages(apiurl, newprj)
    old_packages = self._get_project_packages(apiurl, oldprj)

    if opts.requests:
        requests = get_request_list(apiurl, project=oldprj,
                                    req_state=('new', 'review'))

    for pkg in old_packages:
        if self._prdiff_skip_package(opts, pkg):
            continue

        if pkg not in new_packages:
            if opts.old_only:
                print "old only:  %s" % pkg
            continue

        rdiff = server_diff_noex(
            apiurl,
            oldprj, pkg, None,
            newprj, pkg, None,
            unified=True, missingok=False, meta=False, expand=True
            )

        if rdiff:
            print "differs:   %s" % pkg
            self._prdiff_output_diff(opts, rdiff)

            if opts.requests:
                self._prdiff_output_matching_requests(opts, requests,
                                                      newprj, pkg)
        else:
            print "identical: %s" % pkg

    for pkg in new_packages:
        if self._prdiff_skip_package(opts, pkg):
            continue

        if pkg not in old_packages:
            if opts.new_only:
                print "new only:  %s" % pkg
