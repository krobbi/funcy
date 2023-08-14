"""
Funcy
-----
The SDK for Funcy, a toy functional programming language. The package
provides methods for building Funcy source code and executing Funcy
source code and FVM bytecode, an FVM implementation, and a command line
interface.

Classes
-------
* `FVM` - An implementation of the Funcy Virtual Machine.

Methods
-------
* `funcy.cli(args: list[str]) -> int` - Run the Funcy CLI.
* `funcy.repl() -> None` - Run the Funcy REPL.
* `funcy.build(in_path: str, out_path: str) -> None` - Build Funcy
source code from an input path to FVM bytecode at an output path.
* `funcy.compile(source: str) -> bytes` - Compile Funcy source code to
FVM bytecode.
* `funcy.compile_path(path: str) -> bytes` - Compile Funcy source code
to FVM bytecode from a path.
* `funcy.exec(source: str | bytes) -> int` - Execute Funcy source code
or FVM bytecode and return an exit code.
* `funcy.exec_path(path: str) -> int` - Execute Funcy source code or FVM
bytecode from a path and return an exit code.

Command Line Interface
----------------------
The command line interface is accessed with
`python -m funcy <subcommand>`.

The following subcommands are available:
* `build <in> <out>` - Build to code at <in> to <out>.
* `run <path>` - Run the code at <path>.

License
-------
MIT License

Copyright (c) 2022-2023 Chris Roberts

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from .cli import cli
from .core import build, compile, compile_path, exec, exec_path
from .fvm import FVM
from .repl import repl

__all__: list[str] = [
    "FVM",
    "cli",
    "repl",
    "build",
    "compile",
    "compile_path",
    "exec",
    "exec_path",
]
