# One-way Two Folder Synchronization

This program performs a one-way synchronization between a source folder and a replica folder.


## Features
- Periodic synchronization with a customizable time interval.
- Changes (file creation/update/removal) performed during the synchronization are shown in the console and logged into a log file.
- Source folder, replica folder and the log file paths can also be specified through command line arguments.


## Requirements
- Python 3.x
- The following Python libraries:
    - hashlib
    - os
    - time
    - shutil
    - argparse
    - logging
    - pathlib


## Instructions

### Installation
1. Ensure Python 3.x is installed in your system.
2. Download or clone this repository to your local machine.

### Usage
```
python main.py [-h] [--src SRC] [--repl REPL] [--logf LOGF] [--sync-time SYNC_TIME]
```
- `--src`: Path to the source folder to be synchronized (default: "source").
- `--repl`: Path to the replica folder to be updated to match the source folder (default: "replica").
- `--logf`: Path to the log file (default: "log.txt").
- `--sync-time`: Synchronization interval in seconds (default: 60).

### Example
To synchronize a folder named "foo" with a replica folder named "bar" every 90 seconds, and log the synchronization process to "sync_log.txt", run the following command:
```
python main.py --src "foo" --repl "bar" --logf "sync_log.txt" --sync-time 90
```


## Notes
- The script compares files via a computed MD5 hash of their contents in order to determine if there should be a file update in the replica folder.
- Empty directories under the source folder aren't synchronized over to the replica. A file must exist under a directory for it to be synchronized. (Git like behavior)
- If the source folder doesn't exist, the program will crash.
- If the replica folder doesn't exist, the program will create it at the specified path and perform the periodic synchronization normally.
- To stop the script manually, use the keyboard interrupt `CTRL+C`.