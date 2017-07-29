import sys, re, os

regex = re.compile(r'<(.*)>')
OPENSCADPATH = os.environ['OPENSCADPATH']
library_declation = '''
    
/**
 * The dotSCAD library
 * @copyright Justin Lin, 2017
 * @license https://opensource.org/licenses/lgpl-3.0.html
 *
 * @see https://github.com/JustinSDK/dotSCAD
*/

'''

def included_scads_in(scad):
    with open(scad) as src:
        return {
            os.path.join(OPENSCADPATH, regex.findall(line)[0])
                for line in src if line.startswith('include')
        }

def all_scads_from(main_scad):
    def dig_all_scads(undug_scads):
        if not undug_scads:
            return set()
        else:
            sub_scads = {
                    sub_scad for undug_scad in undug_scads
                        for sub_scad in included_scads_in(undug_scad)
            }
            return undug_scads | dig_all_scads(sub_scads - undug_scads)

    scads_in_main = included_scads_in(main_scad)
    return {scad for scad in dig_all_scads(scads_in_main)}

def code_in(scad):
    with open(scad) as f:
        return [line for line in f if not line.startswith('include')]

def inliner(src_scad, dest_scad):
    with open(dest_scad, mode = 'w') as f:
        f.writelines(code_in(src_scad))
        f.write(library_declation)

        for scad in all_scads_from(src_scad):
            f.writelines(code_in(scad))
            f.write('\n\n')   

def main():
    try:
        src_scad = sys.argv[1]
        dest_scad = sys.argv[2]
        inliner(src_scad, dest_scad)
    except IndexError:
        print('Usage:\n\tpython inline.py src.scad dest.scad')

main()