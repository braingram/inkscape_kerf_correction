Inkscape extension to kerf correcting paths

Install
---

copy kerf_correction.py and kerf_correction.inx to ~/.config/inkscape/extensions/

Use
---

Select a path (or paths) to kerf correct.
Use menu Extensions -> Modify Path -> Kerf Correction
Enter the kerf value (in pixels).
Use + values to outset the path (for cutting shapes)
Use - values to inset the path (for cutting pockets)
Save result as a plain svg (see below)

Notes
---

This script is almost the same as using dynamic offset on each path
and setting the inkscape:radius attribute to the kerf value

This extension generates paths that do not have a "d" attribute. It is
probably a good idea to save them as "Plain svg" so inkscape generates
a correct "d" for the paths.
