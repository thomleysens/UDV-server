import argparse
import os
import lxml.etree as ET

def ParseCommandLine():
    # arg parse
    descr = '''A small utility that extracts all the buildings from a 
               set of CityGML (XML) files folder, blends them and 
               serializes the result in a new CityGML (XML) file.'''
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--inputFiles',
                        nargs='+',
                        type=str,
                        help='CityGML input files')
    parser.add_argument('--inputFolder',
                        nargs='+',
                        type=str,
                        help='Input folder holding CityGML files')
    parser.add_argument('--output',
                        nargs='+',
                        default='output.gml',
                        type=str,
                        help='Resulting file.')
    return parser.parse_args()


def parse_and_simplify(file_path_name, name_space):
    parser = ET.XMLParser(remove_comments=True)
    result = ET.parse(file_path_name, parser)
    # Remove textures coordinates (currently not used by our
    # algorithms)
    appearance = result.find("//app:appearanceMember",
                             namespaces=name_space)
    if appearance is not None:
        appearance.getparent().remove(appearance)
    return result

if __name__ == '__main__':
    cli_args = ParseCommandLine()
    name_space = {None: 'http://www.opengis.net/citygml/1.0',
                  'app': 'http://www.opengis.net/citygml/appearance/1.0'}
    # Parse and simplify inputFiles
    inputs = [parse_and_simplify(filename, name_space)
              for filename in cli_args.inputFiles]
    # Get gml files from input folder
    # r = root, d = directories, f = files
    input_folder = cli_args.inputFolder[0]
    input_folder_files = []
    for r, d, f in os.walk(input_folder):
        for filename in f:
            if filename.endswith('.gml'):
                input_folder_files.append(input_folder + filename)

    inputs = inputs + [parse_and_simplify(filename, name_space)
                       for filename in input_folder_files]
    # We recycle the first parsed input to become the output
    output = inputs[0]

    for city_object_member in inputs[1].findall(".//cityObjectMember",
                                                namespaces=name_space):
        output.getroot().append(city_object_member)
    output.write(cli_args.output[0])

