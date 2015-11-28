#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Nicolas Iooss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Run pep8 on all python files

@author: Nicolas Iooss
@license: MIT
"""
import errno
import os
import os.path
import subprocess


def test():
    """Run pep8 on all python files

    Returns:
        0 on success
        1 on failure
        2 if pep8 is not installed
    """
    # pep8 option to use lines with more than 80 characters
    maxline_option = '--max-line-length=120'
    try:
        pep8_helptext = subprocess.check_output(['pep8', '--help'])
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            print("pep8 not found, aborting test.")
            return 2
        raise
    except subprocess.CalledProcessError:
        print("pep8 on an empty stream exited with error")
        return 1
    else:
        # Old versions of pep8 does not support --max-line-length
        if b'--max-line-length' not in pep8_helptext:
            maxline_option = '--ignore=E501'

    retval = 0
    basedir = os.path.join(os.path.dirname(__file__), os.path.pardir)
    for dirpath, _, files in os.walk(basedir):
        # Ignore files in .git directory
        if '/.git' in dirpath:
            continue

        for filename in files:
            filepath = os.path.join(dirpath, filename)

            # If there is no extension, the first line is used to find
            # python scripts
            if '.' not in filename:
                with open(filepath, 'r') as cur_file:
                    firstline = cur_file.readline().rstrip()
                if 'python' not in firstline:
                    continue
            elif not filename.lower().endswith('.py'):
                continue

            try:
                subprocess.check_output(['pep8', maxline_option,
                                         filepath])
            except subprocess.CalledProcessError as exc:
                print(exc.output.decode('utf-8').rstrip())
                retval = 1
    return retval


if __name__ == '__main__':
    import sys
    sys.exit(test())