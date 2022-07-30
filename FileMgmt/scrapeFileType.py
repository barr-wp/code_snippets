import os
import shutil


def check_create_dir(dir_path):
    if os.path.exists(dir_path):
        return
    else:
        os.mkdir(dir_path)


def scrapeFileType(rootdir, outdir, extension, parent=True):
    """
    Recursively iterates over rootdir. Copies files of specified type to outdir. Exports log file with original paths
    :param rootdir: Where files will be copied from
    :param outdir: Where files will be copied to
    :param extnesion: eg. ".py"
    :param parent: Wheather to copy matched files to a folder named after the file parent directory
    """
    src_log = ''
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(extension):
                parent_folder = os.path.basename(subdir)
                if parent:
                    dst_folder = os.path.join(outdir, parent_folder)
                    check_create_dir(dst_folder)
                else:
                    dst_folder = outdir
                src = os.path.join(subdir, file)
                dst = os.path.join(dst_folder, file)
                shutil.copyfile(src, dst)
                src_log += f'{parent_folder},{src}\n'
                print((src, dst))

    with open(os.path.join(outdir, 'src_log.csv'), 'w') as file:
        file.write(src_log)