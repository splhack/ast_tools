import ast
import typing as tp
import warnings

import astor

from . import Pass
from . import _PASS_ARGS_T
from ast_tools.stack import SymbolTable

class debug(Pass):
    def __init__(self,
            dump_ast: bool = False,
            dump_src: bool = False,
            dump_env: bool = False,
            file: tp.Optional[str] = None,
            append: tp.Optional[bool] = None,
            ) -> _PASS_ARGS_T:
        self.dump_ast = dump_ast
        self.dump_src = dump_src
        self.dump_env = dump_env
        if append is not None and file is None:
            warnings.warn('Option append has no effect when file is None', stacklevel=2)
        self.file = file
        self.append = append

    def rewrite(self,
            tree: ast.AST,
            env: SymbolTable,
            ) -> _PASS_ARGS_T:

        def _do_dumps(dumps, dump_writer):
            for dump in dumps:
                dump_writer(f'BEGIN {dump[0]}\n')
                dump_writer(dump[1].strip())
                dump_writer(f'\nEND {dump[0]}\n\n')

        dumps = []
        if self.dump_ast:
            dumps.append(('AST', astor.dump_tree(tree)))
        if self.dump_src:
            dumps.append(('SRC', astor.to_source(tree)))
        if self.dump_env:
            dumps.append(('ENV', repr(env)))

        if self.file is not None:
            if self.append:
                mode = 'wa'
            else:
                mode = 'w'
            with open(self.dump_file, mode) as fp:
                _do_dumps(dumps, fp.write)
        else:
            def _print(*args, **kwargs): print(*args, end='', **kwargs)
            _do_dumps(dumps, _print)

        return tree, env
