import os
import re


def was_optimized(line):
    converged_message = '\bOptimization converged\b'

    if re.search(line, converged_message):
        return True

    return False


def job_completed(line):
    completed_message = '\bTotal times  cpu:\b'

    if re.search(line, completed_message):
        return True

    return False


def run_checks(line, status):
    if not status['Optimized']:
        status['Optimized'] = was_optimized(line)
    if not status['Completed']:
        status['Completed'] = job_completed(line)


def print_results(file_name, status):
    is_good = True
    for _, v in status.items():
        is_good = is_good and v

    print('File: {} Good: {}'.format(file_name, is_good))
    if not is_good:
        for k, v in status.items():
            print('  {}? {}'.format(k, v))


if __name__ == '__main__':
    output_dir = 'outputs'

    for output_file in os.listdir(output_dir):
        file_name = os.path.join(output_dir, output_file)

        with open(file_name) as file:
            status = {'Optimized': False, 'Completed': False}

            for line in file:
                run_checks(line, status)

            print_results(file_name, status)
