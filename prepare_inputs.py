import os
import tarfile


def sort_files(tarfile_name):
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
    output += '  * library def2-TZVPD\n'
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
    tarfile_name = 'xyz.tar.gz'
    xyz_dir = 'xyz'
    input_dir = 'inputs'

    files = sort_files(tarfile_name)
    filename = files[0][1]
    geom = grab_geom(tarfile_name, filename + '.xyz')
    geom_str = stringify_coordinates(geom)
    input = generate_input(geom_str)
    input_path = os.path.join(input_dir, filename + '.in')
    write_input(input, input_path)
