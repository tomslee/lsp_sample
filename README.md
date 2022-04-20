# A minimal Language Server Protocol demo

This shows how to build a minimal language server, consumed by vim using an LSP client plugin.

The language server is called on text files. Called "efree" it flags an error wherever it finds the character lowercase "e" in the document. The vim plugin responds to these errors by highlighting the occurrences of the letter "e" wherever it occurs.

## The LSP server

The demo uses the "pygls" library, which provides a generic framework for writing your own language servers.

The file /efree.py/ implements the necessary interfaces.

## The LSP client

In vim, I use an LSP client (natebosch/vim-lsc), and call efree.py whenever a python file is loaded.

## Demo

The file void.md includes text from "A Void". The 300-page book "La Disparition" by Georges Perec avoids the letter "e". "A Void" is the translation into English by Gilbert Adair, which also avoids the letter "e".

You can try adding text to see what happens.
