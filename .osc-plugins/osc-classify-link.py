#!/usr/bin/python

import os.path
import sys

# FIXME: read_filemeta could re-use this
def parse_xml(self, path):
    if not os.path.isfile(path):
        raise oscerr.OscBaseError('%s does not exist' % path)

    try:
        xml = ET.parse(path)
    except SyntaxError, e:
        raise oscerr.NoWorkingCopy(
            'When parsing %s, the following error was encountered:\n%s' %
            (path, e))

    return xml

def _contains_branch_element(self, xml):
    patches = xml.find('patches')
    if patches:
        return patches.find('branch') is not None
    return None

def _classify_dir(self, path, use_server):
    if not is_package_dir(path):
        raise oscerr.NoWorkingCopy("'%s' is not a valid working copy." % path)

    aggfile = os.path.join(path, "_aggregate")
    if os.path.isfile(aggfile):
        aggxml = ET.parse(aggfile).getroot()
        target = None
        for node in aggxml.findall('aggregate'):
            target = node.get('project')
        if target:
            return "aggregate -> " + target
        raise RuntimeError("Couldn't find aggregate target in %s" % aggfile)

    pkg = Package(path)
    linkinfo = pkg.linkinfo

    if not linkinfo.islink():
        return 'normal or copypac'

    target = linkinfo.project + '/' + linkinfo.package
    # if linkinfo.isexpanded():
    #     if linkinfo.haserror():
    #         return 'broken link -> ' + target
    #     else:
    #         return 'expanded link -> ' + target

    linkpath = os.path.join(path, store, "_link")
    if os.path.isfile(linkpath):
        xml = self.parse_xml(linkpath)
        if self._contains_branch_element(xml.getroot()):
            return "branch of " + target

    if not linkinfo.baserev:
        # Branches always contain the baserev attribute in <linkinfo>
        # in .osc/_files so if it's missing, that eliminates the
        # possibility it's a branch.  linkpac's don't usually contain
        # baserev in <linkinfo>, but they can.
        return "linkpac -> " + target

    if not use_server:
        # This is our best guess without doing a server round-trip
        return "branch of or linkpac -> %s" % target

    apiurl = self.get_api_url()
    u = makeurl(apiurl, ['source', pkg.prjname, pkg.name, '_link'], query={})
    contents = ''
    for data in streamfile(u):
        contents += data
    xml = ET.fromstring(data)
    if self._contains_branch_element(xml):
        return "branch of " + target

    return "linkpac -> " + target

def _show_classification(self, path, use_server, single):
    classification = self._classify_dir(path, use_server)
    if single:
        print classification
    else:
        if path[0:2] == "./":
            path = path[2:]
        print "%-26s %s" % (path, classification)

@cmdln.option('-s', '--server', action='store_true',
              help='allow server-side checks (slower, improves accuracy)')
def do_classify(self, subcmd, opts, *args):
    """${cmd_name}: Classify projects

    Classify one or more checked out OBS project trees, to distinguish
    between projects which have been branched / linkpac'd / copypac'd /
    aggregatepac'd.
    
    Usage:
        osc classify [OPTIONS] [<PROJECT-DIR | PACKAGE-DIR> ...]

    ${cmd_option_list}
    """

    if len(args) == 0:
        args = [ '.' ]

    for path in args:
        if not os.path.exists(os.path.join(path, store, "_project")):
            print >>sys.stderr, path + \
                " is not associated with a Build Service project; aborting."
            sys.exit(1)

    if len(args) == 1 and os.path.exists(os.path.join(args[0], store, "_package")):
        single = True
    else:
        single = False

    for path in args:
        if os.path.exists(os.path.join(path, store, "_package")):
            self._show_classification(path, opts.server, single)
        else:
            for pkg in sorted(os.listdir(path)):
                if os.path.exists(os.path.join(path, pkg, store, "_package")):
                    self._show_classification(os.path.join(path, pkg),
                                              opts.server, single)
