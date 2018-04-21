"""
    Wviews: Worldview Solver for Epistemic Logic Programs
        Build 1.0 - Port from C++ -> Python.
    Copyright (C) 2014  Michael Kelly

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
from wview import WorldViews


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('programpath', type=str, help='Path to Epistemic Logic Program')
    argparser.add_argument('-d', '--dlvpath', type=str, help='Path to DLV binary')

    args = argparser.parse_args()
    WORLD_VIEW_SESSION = WorldViews(args.programpath, args.dlvpath)

    WORLDVIEWS = []
    args
    for worldview in WORLD_VIEW_SESSION.generate_worldview():
        WORLDVIEWS.append(worldview)

    print WORLDVIEWS


#     files = os.listdir('worldviews')
#     session = WorldViews('worldviews\\interview.txt')
#     worldview_grounder = grounder.grounding(session)
#     countString = []
#     length = 5
#     base = 4
#
#     for count in range(0, length):
#         countString.append(0)
#
#     while 1:
#         countString = worldview_grounder.incString(countString, base, length)
