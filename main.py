import hashlib
import os
import time
import shutil
import argparse
import logging
from pathlib import Path


def compare_files(file1: Path, file2: Path) -> bool:
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
    

def sync_folders(src_path: Path, repl_path: Path) -> tuple[int, int, int]:
    files_created: int = 0
    files_removed: int = 0
    files_updated: int = 0

    # Remove files in replica folder that no longer exist in source folder
    for (dirpath, _, filenames) in os.walk(repl_path):
        src_dirpath: str = dirpath.replace(str(repl_path), str(src_path))
        for filename in filenames:
            if not Path(src_dirpath, filename).exists():
                logging.info(f'Removing deleted file "{Path(dirpath, filename)}".')
                Path(dirpath, filename).unlink()
                files_removed += 1

    # Synchronize files from source folder to replica folder
    for (dirpath, _, filenames) in os.walk(src_path):
        repl_dirpath: str = dirpath.replace(str(src_path), str(repl_path))
        for filename in filenames:
            src_filepath: Path = Path(dirpath, filename)
            repl_filepath: Path = Path(repl_dirpath, filename)

            if not repl_filepath.exists():
                logging.info(f'Creating new file "{repl_filepath}".')
                os.makedirs(repl_filepath.parent, exist_ok=True) # Create the parent directories
                shutil.copy2(src_filepath, repl_filepath) # Will create a new file since it doesn't exist
                files_created += 1
                continue
    
            if compare_files(src_filepath, repl_filepath):
                logging.info(f'"{repl_filepath}" is up to date.')
                continue

            logging.info(f'Updating file "{repl_filepath}".')
            shutil.copy2(src_filepath, repl_filepath)
            files_updated += 1

    return (files_created, files_removed, files_updated)


def main() -> None:
    src_path: Path = Path(args.src)
    repl_path: Path = Path(args.repl)

    if not os.path.isdir(args.src):
        logging.error(f'Source folder {src_path} does not exist. Aborting program.')
        raise FileNotFoundError()
    
    if not os.path.isdir(repl_path):
        logging.warning(f'Replica folder {repl_path} does not exist. Creating a replica folder in that path.')
        os.makedirs(repl_path)

    logging.debug(f'Syncing started between "{src_path}" and "{repl_path}". Sync interval: {args.sync_time} seconds.')

    while True:
        try:
            logging.info('Syncing in progress...')
            files_created, files_removed, files_updated = sync_folders(src_path, repl_path)
            logging.info((
                f'Syncing complete. {files_created + files_removed + files_updated} total change(s): '
                f'{files_created} file(s) created; '
                f'{files_removed} file(s) removed; '
                f'{files_updated} file(s) updated. '
            ))
            time.sleep(args.sync_time)
        except KeyboardInterrupt:
            logging.warning('Program aborted by keyboard interrupt.')
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='One-way two folder synchronization.')
    parser.add_argument('--src', type=str, default='source', help='Source folder path')
    parser.add_argument('--repl', type=str, default='replica', help='Replica folder path')
    parser.add_argument('--logf', type=str, default='log.txt', help='Log file path')
    parser.add_argument('--sync-time', type=int, default=60, help='Synchronization time interval (in seconds)')
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers= [
            logging.FileHandler(args.logf),
            logging.StreamHandler()
        ]
    )

    main()
