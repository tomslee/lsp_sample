@echo off
set _EFREE_HOME=%HOME%\src\lsp_sample
@echo %_EFREE_HOME%
pushd %_EFREE_HOME%
set _CMD=python efree.py
echo %_CMD%
%_CMD%
popd
