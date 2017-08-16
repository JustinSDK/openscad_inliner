import sys, os, argparse
import scad
from typing import List

def do_inline(src, dest, scad_paths):
    try:
        scad.inliner(src, dest, scad_paths)
    except FileNotFoundError as e:
        print(e)
        print('Try to use the -op argument or set up the OPENSCADPATH environment variable')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="the source")
    parser.add_argument("dest", help="the destination")
    parser.add_argument("-op", "--openscadpath", help="specify where to find user scad files")

    if(len(sys.argv) == 1):
        parser.print_help()
    else:
        args = parser.parse_args()

        scad_paths: List[str] = (
            args.openscadpath 
                if args.openscadpath else os.environ['OPENSCADPATH']
        ).split(';')

        do_inline(args.src, args.dest, scad_paths)

main()