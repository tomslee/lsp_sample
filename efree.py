#!/usr/bin/python3
"""
"""

# -------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------
import logging
# import argparse
from pygls.server import LanguageServer
from pygls.features import (TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE,
                            TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE)
from pygls.types import (Diagnostic, DidChangeTextDocumentParams,
                         DidSaveTextDocumentParams, DidCloseTextDocumentParams,
                         DidOpenTextDocumentParams, Position, Range)

# -------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------
logging.basicConfig(filename="logfree.log",
                    filemode="w",
                    format='%(asctime)-15s %(levelname)-8s%(message)s',
                    level=logging.INFO)
server = LanguageServer()


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------
@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """ Text document did open notification."""
    ls.show_message("LS Text Document Did Open")
    _validate(ls, params)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    ls.show_message("LS Text Document Did Change")
    _validate(ls, params)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls, params: DidSaveTextDocumentParams):
    """Text document did change notification."""
    ls.show_message("LS Text Document Did Save")
    _validate(ls, params)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    logging.info("Text document did close")


def _validate(ls, params):
    """
    Validate a document and publish diagnostics
    """
    text_doc = ls.workspace.get_document(params.textDocument.uri)
    source = text_doc.source
    ls.show_message_log('*** Validating document %s...', text_doc)
    diagnostics = []
    line_index = -1
    for line in source.splitlines():
        logging.debug("*** %s", line)
        line_index += 1
        col_index = -1
        while True:
            if col_index == -1:
                col_index = str.find(line, "e")
            else:
                col_index = str.find(line, "e", col_index + 1)
            if col_index == -1:
                logging.debug("The remainder of line %s is efree", line_index)
                break
            msg = "Character e at column {}".format(col_index)
            d = Diagnostic(Range(Position(line_index, col_index),
                                 Position(line_index, col_index + 1)),
                           msg,
                           source=type(server).__name__)
            diagnostics.append(d)
            logging.debug("e at line %s, col %s", line_index, col_index)
    ls.publish_diagnostics(text_doc.uri, diagnostics)


def main():
    """
    Entry point.
    """
    # start_server(8080)
    # server.start_tcp('localhost', 8080)
    logging.info("About to start efree Language Server")
    server.start_io()
    logging.info("Started efree Language Server")
    _validate("what the hell is going on?")


if __name__ == '__main__':
    main()
