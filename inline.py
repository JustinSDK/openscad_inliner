import sys, scad

def main() -> None:
    try:
        src_scad = sys.argv[1]  
        dest_scad = sys.argv[2] 
        scad.inliner(src_scad, dest_scad)
    except IndexError:
        print('Usage:\n\tpython inline.py src.scad dest.scad')

main()