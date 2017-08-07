# openscad_inliner

There are many modules and functions located in separated .scad file in my [dotSCAD](https://github.com/JustinSDK/dotSCAD). The Thingiverse customize, however, requires all code in a single file. This tool avoids copying and pasting manually if I create something from my library and want to upload it to Thingiverse.

It requires Python 3.6. There's only one command:

    python inline.py src.scad dest.scad