# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn

# This snippet taken from PYOMO project
# citation: Hart, William E., Carl Laird, Jean-Paul Watson, David L. Woodruff,
# Gabriel A. Hackebeil, Bethany L. Nicholson, and John D. Siirola.
# Pyomo – Optimization Modeling in Python. Springer, 2017.
"""

"""
import sys


class OutputStream:
    """Output stream object for simultaneously writing to multiple streams.

    Returns:
        [type]: [description]
    """

    def __init__(self, tee=False, logfile=None):
        """Initialize output stream object.

        Args:
            tee (bool, optional): This stream will write to stdout. Defaults to False.
            logfile ([type], optional): A logfile can be written. Defaults to None.
        """
        if tee:
            self.tee = sys.stdout
        else:
            self.tee = None
        self.logfile = logfile
        self.logfile_buffer = None

    def __enter__(self):
        """Enter context of output stream and open logfile if given."""
        if self.logfile is not None:
            self.logfile_buffer = open(self.logfile, "a")
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
