import sys, argparse 
import scad

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="the source scad")
    parser.add_argument("dest", help="the destination scad")

    if(len(sys.argv) == 1):
        parser.print_help()
    else:
        scad.inliner(args.src, args.dest)

main()