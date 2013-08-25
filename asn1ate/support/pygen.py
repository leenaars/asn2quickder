# Copyright (c) 2013, Schneider Electric Buildings AB
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Schneider Electric Buildings AB nor the
#       names of contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

try:
    # Python 2
    from cStringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

from datetime import datetime


def auto_generated_header(source_filename=None):
    prefix = '# Auto-generated'
    if source_filename:
        prefix += ' from %s' % source_filename

    return '%s by asn1ate on %s' % (prefix, datetime.now())


class NullBackend(object):
    """ Code generator to create an empty file.
    Used to create __init__.py files.
    """
    def __init__(self, *args):
        pass

    def generate_code(self, *args):
        pass


class PythonWriter(object):
    """ Indentation-aware text stream. """
    def __init__(self, out_stream, indent_size=4):
        self.out = out_stream
        self.indent_size = indent_size
        self.current_indent = 0

    def push_indent(self):
        self.current_indent += self.indent_size

    def pop_indent(self):
        self.current_indent -= self.indent_size

    def write_line(self, line):
        if line is not None:
            line = self._indent(line) if line else line
            self.out.write('%s\n' % line)

    def write_blanks(self, count=1):
        for i in range(0, count):
            self.out.write('\n')

    def write_block(self, block):
        """ Reindents after every line break. """
        block = block.rstrip()
        for line in block.split('\n'):
            self.write_line(line)

    def write_enumeration(self, items):
        self.write_block(',\n'.join(items))

    def get_fragment(self):
        return PythonFragment(self.indent_size)

    def _indent(self, line):
        return ' ' * self.current_indent + line


class PythonFragment(PythonWriter):
    """ A buffering python writer, useful for nested structures.
    """
    def __init__(self, indent_size=4):
        self.buf = StringIO()
        super(PythonFragment, self).__init__(self.buf, indent_size)

    def __str__(self):
        return self.buf.getvalue()
