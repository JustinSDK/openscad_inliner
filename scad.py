import re, os
from typing import List, Set, Pattern

regex = re.compile(r'<(.*)>')             # type: Pattern[str]
library_declation = '''
    
/**
 * The dotSCAD library
 * @copyright Justin Lin, 2017
 * @license https://opensource.org/licenses/lgpl-3.0.html
 *
 * @see https://github.com/JustinSDK/dotSCAD
*/

'''

def scad_file_fullname(scad_paths: List[str], scad_name: str) -> str:
    for path in scad_paths:
        f = os.path.join(path, scad_name)
        if os.path.isfile(f):
            return f

    raise FileNotFoundError('scad not found: {}'.format(scad_name))

def included_scads_in(scad: str, scad_paths: List[str] = None) -> Set[str]:
    scads = None
    with open(scad) as src:
        scads = {
            regex.findall(line)[0]
                for line in src if (line.startswith('include') or line.startswith('use'))
        }

    if scad_paths:
        return {scad_file_fullname(scad_paths, scad) for scad in scads}
    else: # find scads in the current folder
        return scads

def all_scads_from(main_scad: str, scad_paths: List[str] = None) -> Set[str]:
    def dig_all_scads(undug_scads: Set[str]) -> Set[str]:
        if not undug_scads:
            return set()
        else:
            sub_scads = {
                    sub_scad for undug_scad in undug_scads
                        for sub_scad in included_scads_in(undug_scad, scad_paths)
            }
            return undug_scads | dig_all_scads(sub_scads - undug_scads)

    scads_in_main = included_scads_in(main_scad, scad_paths)
    
    return {scad for scad in dig_all_scads(scads_in_main)}

def code_in(scad: str) -> List[str]:
    with open(scad) as f:
        return [line for line in f if not (line.startswith('include') or line.startswith('use'))]

def inliner(src_scad: str, dest_scad: str, scad_paths: List[str] = None) -> None:
    with open(dest_scad, mode = 'w') as f:
        f.writelines(code_in(src_scad))
        f.write(library_declation)
        for scad in all_scads_from(src_scad, scad_paths):
            f.writelines(code_in(scad))
            f.write('\n\n')   
