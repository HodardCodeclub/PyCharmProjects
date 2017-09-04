import Queue
import hashlib
import os
import re
import subprocess
from operator import itemgetter
from optparse import OptionParser

options = {}
pattern = None
directories = []
directory_checksums = []
files_checksums = []
duplicate_files = []
duplicate_directories = []


def parseParams():
    global options
    global pattern
    global directories

    parser = OptionParser(usage="usage: duplicates.py < -c <command> | -p > [-f | -d] [\"...\"] [<dir1> <dir2> ..]",
                          version="duplicates 1.0")

    parser.add_option("-c", "--command",
                      action='store',
                      dest="command",
                      default=None,
                      help="give a command")

    parser.add_option("-p", "--print",
                      action='store_true',
                      dest="print_flag",
                      default=False,
                      help="print duplicates")

    parser.add_option("-f", "--files",
                      action='store_true',
                      dest="files_flag",
                      default=False,
                      help="look duplicate files")

    parser.add_option("-d", "--directories",
                      action='store_true',
                      dest="directories_flag",
                      default=False,
                      help="look duplicate directories")

    (options, args) = parser.parse_args()

    if len(args) > 0:
        pattern = args[0]
        if pattern != "":
            pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    if len(args) > 1:
        directories = args[1:]

    if options.command == None and options.print_flag == False:
        options.print_flag = True

    if options.directories_flag == False and options.files_flag == False:
        options.files_flag = True

    if len(directories) == 0:
        directories.append(os.getcwd())


def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def controlDirDup(path, fullsha, matched_list):
    for (pth, sha) in directory_checksums:
        if pth != path and sha == fullsha and (pth in matched_list) and (path in matched_list):
            duplicate_directories.append((pth, path))


def controlFileDup(path, fullsha, matched_list):
    for (pth, sha) in files_checksums:
        if pth != path and sha == fullsha and (pth in matched_list) and (path in matched_list):
            duplicate_files.append((pth, path))


def traverseDFS_DirDup(path, upper_match):
    global directory_checksums

    if os.path.exists(path):
        curlist = os.listdir(path)
        curlist.sort()
        checksum_list_pair = []
        # match = []
        if pattern != "":
            match = filter(pattern.search, curlist)
        else:
            match = curlist
        for item in curlist:
            item_path = path + "/" + item
            idx = item_path.index("//")
            if os.path.isfile(item_path):
                item_path = item_path[0:idx] + item_path[idx + 1:]
                checksum_list_pair.append((item_path, sha256_checksum(item_path)))
            elif os.path.isdir(item_path):
                idx = item_path.index("//")
                item_path = item_path[0:idx] + item_path[idx + 1:] + "/"
                try:
                    itemIdx = match.index(item)
                    match[itemIdx] = item_path
                    sub_checksum = traverseDFS_DirDup(item_path, match)
                    checksum_list_pair.append((item_path, sub_checksum))
                except ValueError as e:
                    sub_checksum = traverseDFS_DirDup(item_path, match)
                    checksum_list_pair.append((item_path, sub_checksum))

        checksum_list_pair = sorted(checksum_list_pair, key=itemgetter(1))
        checksum_list = map(itemgetter(1), checksum_list_pair)
        checksum_list.sort()

        if len(checksum_list) == 0:
            checksum_list.append("NULL")
        fullsha = ''.join(checksum_list) + "SUBDIR"
        directory_checksums.append((path, fullsha))
        if path in upper_match:
            directory_checksums = sorted(directory_checksums, key=itemgetter(1))
            matched_list = map(itemgetter(0), directory_checksums)
            controlDirDup(path, fullsha, matched_list)

        return fullsha


def traverseBFS_FileDup(rootDir):
    global duplicate_files
    global files_checksums

    dirlist = Queue.Queue()
    dirlist.put(rootDir)
    while not dirlist.empty():
        fullpathname = dirlist.get()
        if os.path.exists(fullpathname):
            curlist = os.listdir(fullpathname)
            curlist.sort()
            ss = ''.join(curlist)
            # match = []
            if pattern != "":
                match = filter(pattern.search, curlist)
            else:
                match = curlist
            for fdname in curlist:
                item_path = fullpathname + "/" + fdname
                if os.path.isfile(item_path):
                    idx = item_path.index("//")
                    item_path = item_path[0:idx] + item_path[idx + 1:]
                    try:
                        itemIdx = match.index(fdname)
                        match[itemIdx] = item_path
                        checksum = sha256_checksum(item_path)
                        files_checksums.append((item_path, checksum))
                        files_checksums = sorted(files_checksums, key=itemgetter(1))
                        matched_list = map(itemgetter(0), files_checksums)
                        controlFileDup(item_path, checksum, matched_list)
                    except ValueError as e:
                        # print e.message
                        pass
                elif os.path.isdir(item_path):
                    try:
                        idx = item_path.index("//")
                        item_path = item_path[0:idx] + item_path[idx + 1:] + "/"
                    except ValueError as e:
                        # print e.message
                        pass
                    dirlist.put(item_path)


if __name__ == '__main__':

    parseParams()

    if options.files_flag:

        for directory in directories:
            traverseBFS_FileDup(directory)

        duplicate_files = list(set(duplicate_files))

        if len(duplicate_files) == 0:
            print "(no duplicates)"
            exit(1)

        if options.command != None and options.print_flag == False:
            for (file1, file2) in duplicate_files:
                if os.path.exists(file1):
                    cmd = options.command + " " + file1
                    subprocess.call(cmd, shell=True)
                if os.path.exists(file2):
                    cmd = options.command + " " + file2
                    subprocess.call(cmd, shell=True)
        else:
            for (file1, file2) in duplicate_files:
                if os.path.exists(file1) and os.path.exists(file2):
                    print "{} {}".format(file1, file2)

    elif options.directories_flag:

        for directory in directories:
            traverseDFS_DirDup(directory, [])

        duplicate_directories = list(set(duplicate_directories))
        if len(duplicate_directories) == 0:
            print "(no duplicates)"

        if options.command != None and options.print_flag == False:
            for (dir1, dir2) in duplicate_directories:
                if os.path.exists(dir1):
                    cmd = options.command + " " + dir1
                    subprocess.call(cmd, shell=True)
                if os.path.exists(dir2):
                    cmd = options.command + " " + dir2
                    subprocess.call(cmd, shell=True)
        else:
            for (dir1, dir2) in duplicate_directories:
                if os.path.exists(dir1) and os.path.exists(dir2):
                    print "{} {}".format(dir1, dir2)
