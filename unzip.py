# Copyright 2018 Colin Girling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import zipfile
import argparse

class Unzip:
    NoError = ""
    FileNotFoundError = "File Not Found"
    BadZipFileError = "Bad Zip File"
    LargeZipFileError = "Large Zip File"

    NoErrorCode = 0
    FileNotFoundErrorCode = 1
    BadZipFileErrorCode = 2
    LargeZipFileErrorCode = 3

    # Construct Unzip object for unzipping a file to a destination.
    # path - full path and filename for extraction.
    # dest - destination path to extract files too.
    #        dest can be "." extract to current folder.
    def __init__(self, path, dest):
        self.path = path
        self.dest = dest
        self.zip_file = None

    # Ensure when the Unzip object is destroyed, any Zip file still open is closed.
    def __del__(self):
        if self.zip_file is not None:
            self.zip_file.close()

    # Unzip a file from path to dest, which is specified in initialization.
    def UnzipFile(self):
        if os.path.exists(self.path):
            try:
                self.zip_file = zipfile.ZipFile(self.path, 'r')
                self.zip_file.extractall(self.dest)
                self.zip_file.close()
                self.zip_file = None

            except zipfile.BadZipfile:
                #Python 2 zipfile library doesn't support every compressed file format.
                return (self.BadZipFileError, self.BadZipFileErrorCode)

            except zipfile.LargeZipFile:
                # if ZIP64 is not enabled, the the zip file has a 32-bit file size limit.
                return (self.LargeZipFileError, self.LargeZipFileErrorCode)
        else:
            return (self.FileNotFoundError, self.FileNotFoundErrorCode)
        return (self.NoError, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unzip file or archive.\nSuppoers .zip, .gz, .tar.gz')
    parser.add_argument('file', help='a path and filename to be decompressed')
    parser.add_argument('dest', help='destination folder to decompress into. If empty, the current folder is used.')
    args = parser.parse_args()

    print "Extracting " + args.file + " to " + args.dest

    unzipper = Unzip(args.file, args.dest)
    error = unzipper.UnzipFile()

    if error[1] > 0:
        print "ERROR: " + error[0]
        sys.exit(error[1])

    sys.exit(unzipper.NoErrorCode)
