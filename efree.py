#!/usr/bin/python3
"""
A simple LSP server for "efree", written on pygls, which provides a framework
for writing LSP servers.

efree identifies lower-case "e" in a document and highlights it.
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
    _validate(ls, params)
    logging.info(">>> Event: Text document did open")


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _validate(ls, params)
    logging.info(">>> Event: Text document did change")


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    logging.info(">>> Event: Text document did save")


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    _validate(ls, params)
    logging.info(">>> Event: Text document did close")


def _validate(ls, params):
    """
    Validate a document and publish diagnostics
    """
    text_doc = ls.workspace.get_document(params.textDocument.uri)
    source = text_doc.source
    diagnostics = []
    line_index = -1
    # test comment
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
    Entry point: start the language server
    """
    logging.info("About to start efree Language Server")
    server.start_io()
    logging.info("Started efree Language Server")


if __name__ == '__main__':
    main()
