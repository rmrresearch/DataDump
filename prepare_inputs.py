import os
import tarfile


def sort_files(tarfile_name):
    '''Reads the files from tarfile_name and sorts them by number of atoms.

       return: A list of pairs such that the 1-st element of each pair is the 
               name of an XYZ file and the 0-th element is the number of atoms
               in that file.
    '''
    rv = []

    with tarfile.open(tarfile_name, mode='r:gz') as tar:
        for member in tar.getnames():
            filename_parts = os.path.splitext(member)
            file_base = filename_parts[0]
            extension = filename_parts[1]

            if file_base.count('.') or extension != '.xyz':
                continue

            f = tar.extractfile(member)
            n_atoms = int(f.readline().decode('utf-8'))
            rv.append((n_atoms, file_base))

    rv.sort()
    return rv


def grab_geom(tarfile_name, file):
    geom = []
    with tarfile.open(tarfile_name, mode='r:gz') as tar:
        f = tar.extractfile(file)
        f.readline()
        f.readline()
        for line in f:
            atom = [x for x in line.decode('utf-8').split()[:4]]
            geom.append(atom)
    return geom


def stringify_coordinates(geom):
    contents = ''
    for atom in geom:
        contents += '{} {} {} {}\n'.format(atom[0], atom[1], atom[2], atom[3])
    return contents


def generate_input(geom):
    output = 'geometry\n'
    output += geom
    output += 'end\n\n'
    output += 'basis\n'
    output += '  * library cc-pvdz\n'
    output += 'end\n\n'
    output += 'dft\n'
    output += '  xc b3lyp\n'
    output += 'end\n\n'
    output += 'task dft optimize\n'
    output += 'task dft freq'
    return output


def write_input(geom, output_file):
    with open(output_file, 'w') as f:
        f.write(geom)


if __name__ == '__main__':
    tarfile_name = 'no_solvent.tar.gz'
    xyz_dir = 'xyz'
    input_dir = 'inputs'

    files = sort_files(tarfile_name)

    for _, filename in files[:1]:
        geom = grab_geom(tarfile_name, filename + '.xyz')
        geom_str = stringify_coordinates(geom)
        input = generate_input(geom_str)

        no_xyz_dir = os.path.split(filename)[1]
        input_path = os.path.join(input_dir, no_xyz_dir + '.in')

        if not os.path.exists(input_dir):
            os.makedirs(input_dir)

        write_input(input, input_path)
