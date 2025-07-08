import os
import re


def was_optimized(line):
    converged_message = '\bOptimization converged\b'

    if re.search(line, converged_message):
        return True

    return False


def job_completed(file):
    completed_message = '\bTotal times  cpu:\b'

    for line in file:
        if re.search(line, completed_message):
            return True

    return False


if __name__ == '__main__':
    output_dir = 'outputs'

    for output_file in os.listdir(output_dir):
        file_name = os.path.join(output_dir, output_file)

        with open(file_name) as file:
            optimized = False
            completed = False

            for line in file:
                if not optimized:
                    optimized = was_optimized(line)
                if not completed:
                    completed = job_completed(line)

            msg = 'File: {} Optimized?: {} Completed? {}'
            print(msg.format(file_name, optimized, completed))
