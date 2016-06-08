#  diceware -- passphrases to remember
#  Copyright (C) 2016  Uli Fouquet and contributors
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""logging -- output status and other data.

The `logger` provided in this module is meant to be used by other
components for messages to users.

It is named `"ulif.openoffice"` and can, as a singleton, be retrieved by
calling standard lib `logging.getLogger("ulif.diceware")`.

By default it provides a `logging.NullHandler` as libraries normally
do. Other components might add other handlers.

"""
import logging
try:
    from logging import NullHandler
except ImportError:  # NOQA  # pragma: no cover
    class NullHandler(object):
        """Replacement for `logging.NullHandler` from py3.x standard lib.
        """
        level = None

        def emit(self, record):
            pass

        def handle(self, record):
            pass

        def createLock(self):
            pass


#: Logger that can be used for all diceware related messages.
logger = logging.getLogger("ulif.diceware")
logger.addHandler(NullHandler())


def configure(verbosity=None):
    """Configure global duceware logger.

    `verbosity` sets the diceware logger verbosity. ``0`` enables info
    mode, while all numbes > 2 enable debug mode.
    """
    if verbosity is None:
        return
    logger.setLevel(logging.CRITICAL)
    if verbosity == 1:
        logger.setLevel(logging.INFO)
    elif verbosity > 1:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.debug("Verbose logging enabled")
