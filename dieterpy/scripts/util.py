# Snippet taken from PYOMO project
# citation: Hart, William E., Carl Laird, Jean-Paul Watson,
# David L. Woodruff, Gabriel A. Hackebeil, Bethany L. Nicholson,
# and John D. Siirola. Pyomo – Optimization Modeling in Python. Springer, 2017.


class OutputStream:
    """Output stream object for simultaneously writing to multiple streams.
    tee=False:
        If set writing to this stream will write to stdout.
    logfile=None:
        Optionally a logfile can be written.
    """

    def __init__(self, tee=False, logfile=None):
        """Initialize output stream object."""
        if tee:
            self.tee = sys.stdout
        else:
            self.tee = None
        self.logfile = logfile
        self.logfile_buffer = None

    def __enter__(self):
        """Enter context of output stream and open logfile if given."""
        if self.logfile is not None:
            self.logfile_buffer = open(self.logfile, 'a')
        return self

    def __exit__(self, *args, **kwargs):
        """Enter context of output stream and close logfile if necessary."""
        if self.logfile_buffer is not None:
            self.logfile_buffer.close()
        self.logfile_buffer = None

    def write(self, message):
        """Write messages to all streams."""
        if self.tee is not None:
            self.tee.write(message)
        if self.logfile_buffer is not None:
            self.logfile_buffer.write(message)

    def flush(self):
        """Needed for python3 compatibility."""
        if self.tee is not None:
            self.tee.flush()
        if self.logfile_buffer is not None:
            self.logfile_buffer.flush()
