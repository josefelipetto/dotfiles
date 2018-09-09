#!/usr/bin/env python3

'''
usage: backupdots.py [-h] -p PLATFORM [-b] [-r] [-c] [-u]

Backup or restore configuration files.

optional arguments:
  -h, --help            show this help message and exit
  -p PLATFORM, --platform PLATFORM
                        specifies which set of files to use (Mac, Linux,
                        Windows)
  -b, --backup          perform a backup based on files in backupdots.json
  -r, --restore         perform a restore based on files in backupdots.json
  -c, --cleanup         removes *.orig files
  -u, --unlink          removes all symlinks for the given platform
'''

import os
import sys
import json
import argparse
import shutil

def perform_backup():
    # Copies files from original location to dotfiles/...
    file_num = 1
    for file in _backup_data:
        orig_file = os.path.join(_backup_data[file][0], file)
        backup_file = os.path.join(_backup_data[file][1], file)

        if not os.path.exists(backup_file.replace("'", "")) and not os.path.islink(orig_file):
            if not os.path.exists(_backup_data[file][1]):
                os.makedirs(_backup_data[file][1], mode=0o755)
            if not os.path.isdir(orig_file):
                backup_type = "file"
                shutil.copy(os.path.join(_backup_data[file][0], file), _backup_data[file][1])
            else:
                backup_type = "directory"
                shutil.copytree(os.path.join(_backup_data[file][0], file), os.path.join(_backup_data[file][1], file))
            print(f'{str(file_num).rjust(3)} Copied {backup_type}: {file} to {_backup_data[file][1]}')
            file_num += 1

    if file_num == 1:
        print("Nothing to backup...")

    if (_args.platform).lower() == "mac":
        print('Dumping installed homebrew packages...')
        os.system(os.path.join(_backup_dir_root, 'Mac/Homebrew/dump.sh'))
        print('...brew bundle dump complete!')

    if (_args.platform).lower() == "linux":
        print('Dumping GNOME Terminal default profile...')
        os.system(os.path.join(_backup_dir_root, 'Linux/GNOMETerminal/dump.sh'))
        print('...profile dump complete!')


def perform_restore():
    # Symlinks files from dotfiles/... to original location.
    file_num = 1
    for file in _backup_data:
        orig_file = os.path.join(_backup_data[file][0], file)
        backup_file = os.path.join(_backup_data[file][1], file)

        # Assume that the program isn't installed or the configuration file is
        # not needed if the original path doesn't exist.
        if os.path.exists(_backup_data[file][0]):
            # Make a backup of the file before creating a symlink.
            if os.path.exists(orig_file) and not os.path.islink(orig_file):
                shutil.move(orig_file, f'{orig_file}.{_backup_file_ext}')
            if not os.path.exists(orig_file):
                try:
                    os.symlink(backup_file, orig_file)
                except PermissionError:
                    if not sudo_command(f'sudo ln -s {backup_file} {orig_file}'):
                        continue
                print(f'{str(file_num).rjust(3)} Linked {"directory" if os.path.isdir(backup_file) else "file"}: {file} to {_backup_data[file][0]}')
                file_num += 1
        else:
            print(f'    WARNING: {_backup_data[file][0]} does not exist, skipping...')

    if file_num == 1:
        print("Nothing to restore...")


def perform_cleanup():
    # Removes all *.{_backup_file_ext} files generated from perform_restore().
    file_num = 1
    for file in _backup_data:
        current_file = os.path.join(_backup_data[file][0], f'{file}.{_backup_file_ext}')

        if os.path.exists(current_file):
            if not os.path.isdir(current_file):
                cleanup_type = "file"
                try:
                    os.remove(current_file)
                except PermissionError:
                    if not sudo_command(f'sudo rm {current_file}'):
                        continue
            else:
                cleanup_type = "directory"
                try:
                    shutil.rmtree(current_file)
                except PermissionError:
                    if not sudo_command(f'sudo rm -rf {current_file}'):
                        continue
            print(f'{str(file_num).rjust(3)} Removed {cleanup_type}: {current_file}')
            file_num += 1

    if file_num == 1:
        print("Nothing to cleanup...")


def perform_unlink():
    # Removes all symlinks for the given platform.
    file_num = 1
    for file in _backup_data:
        is_dir = os.path.isdir(os.path.join(_backup_data[file][1], file))
        current_file = os.path.join(_backup_data[file][0], file)

        if os.path.exists(current_file):
            try:
                os.unlink(current_file)
            except PermissionError:
                if not sudo_command(f'sudo rm {current_file}'):
                    continue
            print(f'{str(file_num).rjust(3)} Unlinked {"directory" if is_dir else "file"}: {current_file}')
            file_num += 1

    if file_num == 1:
        print("Nothing to unlink...")


def sanitized_full_path(dir_location, file_name):
    sanitized_dir_location = dir_location
    sanitized_file_name = file_name

    if dir_location.endswith("/"):
        sanitized_dir_location = dir_location[:-1]

    if file_name.startswith("/"):
        sanitized_file_name = file_name[1:]

    return os.path.join(sanitized_dir_location, sanitized_file_name)


def sudo_command(cmd):
    success = False

    # TODO: Handle permissions error on windows
    if (_args.platform).lower() == "linux" or (_args.platform).lower() == "mac": 
        exit_code = os.system(cmd)
        success = True if exit_code == 0 else False
    else:
        print(f'    WARNING: Unable to symlink {backup_file} to {orig_file}, skipping...')

    return success


if __name__ == "__main__":
    _backup_dir_root = os.path.dirname(os.path.abspath(__file__))
    _backup_config_file = sanitized_full_path(_backup_dir_root, 'backupdots.json')
    _backup_file_ext = "orig"

    arg_parser = argparse.ArgumentParser(description='Backup or restore configuration files.')
    arg_parser.add_argument('-p', '--platform', help='specifies which set of files to use (Mac, Linux, Windows)', required=True)
    arg_parser.add_argument('-b', '--backup', help='perform a backup based on files in backupdots.json', action='store_true')
    arg_parser.add_argument('-r', '--restore', help='perform a restore based on files in backupdots.json', action='store_true')
    arg_parser.add_argument('-c', '--cleanup', help=f'removes *.{_backup_file_ext} files', action='store_true')
    arg_parser.add_argument('-u', '--unlink', help=f'removes all symlinks for the given platform', action='store_true')
    _args = arg_parser.parse_args()

    if not os.path.exists(_backup_config_file):
        print(f'ERROR: Configuration file "{_backup_config_file}" does not exist.')
        sys.exit(1)

    with open(_backup_config_file) as f:
        _backup_data = json.load(f)[(_args.platform).capitalize()]

    if _args.backup:
        perform_backup()
    elif _args.restore:
        perform_restore()
    elif _args.cleanup:
        perform_cleanup()
    elif _args.unlink:
        perform_unlink()
    else:
        perform_backup()
