@echo off
set _EFREE_HOME=%HOME%\src\lsp\efree
@echo %_EFREE_HOME%
pushd %_EFREE_HOME%
set _CMD=python efree.py
echo %_CMD%
%_CMD%
popd
