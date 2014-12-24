#! /usr/bin/env python
'''
Copyright (C) 2014 Brett Graham (hahahaha @ hahaha.org)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import gettext
import re
import sys

import inkex
import simplepath
#import simplestyle

debug = False

error = lambda msg: inkex.errormsg(gettext.gettext(msg))
if debug:
    stderr = lambda msg: sys.stderr.write(msg + '\n')
else:
    stderr = lambda msg: None


def resolve_path(node, transform=False):
    path = simplepath.parsePath(node.attrib['d'])
    if transform and 'transform' in node.attrib:
        transforms = re.findall(
            "([a-z,A-Z]+)\(([0-9,\s,.,-]*)\)",
            node.attrib['transform'])
        for k, vs in transforms:
            sc = ' '
            if ',' in vs:
                sc = ','
            args = map(lambda v: float(v.strip()), vs.split(sc))
            if k == 'translate':
                simplepath.translatePath(path, *args)
            elif k == 'scale':
                simplepath.scalePath(path, *args)
            elif k == 'rotate':
                simplepath.rotatePath(path, *args)
            else:
                error(
                    "Invalid path data: contains unsupported transform %s" % k)
    return path


class KerfCorrection(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option(
            "-k", "--kerf",
            action="store", type="float",
            dest="kerf", default=3.,
            help="Kerf (pixels, - inside, + outside)")
        self.OptionParser.add_option(
            "-o", "--original",
            action="store", type="inkbool",
            dest="original", default=False,
            help="Keep original paths")

    def effect(self):
        stderr("options: %s" % self.options)
        kerf = self.options.kerf
        stderr("kerf: %s" % kerf)

        # get selected path(s)
        if len(self.selected) == 0:
            error("No selection found")
            return

        stderr("selected: %s" % self.selected)
        path = inkex.addNS("path", "svg")
        paths = {}
        for nid in self.selected:
            if self.selected[nid].tag == path:
                paths[nid] = self.selected[nid]
                stderr("path: %s" % paths[nid])

        if len(paths) == 0:
            error("No paths found")
            return

        parent = self.current_layer
        for nid in paths:
            path = paths[nid]
            stderr("path: %s" % path)
            attrs = {}
            raw_path = resolve_path(path)
            attrs[inkex.addNS('original', 'inkscape')] = simplepath.formatPath(
                raw_path)
            # TODO resolve and add d?
            attrs[inkex.addNS('radius', 'inkscape')] = str(kerf)
            attrs[inkex.addNS('type', 'sodipodi')] = 'inkscape:offset'
            # TODO copy over other attributes?
            for name in ('style', 'transform'):
                if name in path.attrib:
                    attrs[name] = path.attrib[name]
            stderr("adding path: %s" % attrs)
            inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), attrs)

        if not self.options.original:
            for nid in paths:
                stderr("dir(%s): %s" % (paths[nid], dir(paths[nid])))
                paths[nid].getparent().remove(paths[nid])


if __name__ == '__main__':
    e = KerfCorrection()
    e.affect()
