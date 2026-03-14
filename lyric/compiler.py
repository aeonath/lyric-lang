# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Lyric-to-Python AST compiler (transpiler).

Translates Lyric AST nodes into Python ast module nodes, then compiles
them with compile() for execution by CPython's bytecode VM.

Phase 1: Core expressions and statements — variables, arithmetic, print,
if/else, while/for loops, functions, importpy, main() invocation.

Phase 2: Collections, strings, type system — arr/map/tup literals, indexing,
slicing, typed declarations with enforcement, multi-declarations, in operator.

Phase 3: Functions with type checking and builtins — parameter/return type
enforcement, all builtin functions, RexNode, range() optimization.

Phase 4: Classes and inheritance — native Python class compilation,
constructor mapping, method compilation with self, extends/super support.

Phase 5: Module system and imports — Lyric module imports, selective importpy,
module namespace binding, stdlib loading.

Phase 6: I/O, exec, and edge cases — file operators, exec chains, try/catch/raise.
"""

import ast as pyast
from lyric.ast_nodes import (
    ProgramNode, FunctionNode, IfNode, LoopNode, AssignNode, CallNode,
    BinaryOpNode, UnaryOpNode, LiteralNode, IdentifierNode, ReturnNode,
    BreakNode, ContinueNode, TypeDeclarationNode, MultiDeclarationNode,
    ImportPyNode, ImportNode, ListLiteralNode, DictLiteralNode, TupleLiteralNode,
    IndexNode, SliceNode, RexNode, ClassNode,
    TryNode, CatchClauseNode, RaiseNode, FileOpNode, ExecChainNode,
)


class LyricCompiler:
    """Compiles Lyric AST to Python ast module nodes."""

    def __init__(self, source_file='<lyric>'):
        self.source_file = source_file
        self._functions_defined = {}  # name -> param count
        self._current_function_return_type = None  # Track return type for current function
        self._module_level_vars = set()  # Variables declared at module level
        self._in_function = False  # Whether we're inside a function body
        self._type_registry = {}  # var_name -> declared_type (for typed reassignment checks)
        self._declared_vars = set()  # All declared variable names (var, int, str, etc.)
        self._in_class_body = False  # Whether we're compiling class member declarations

    def compile(self, program: ProgramNode):
        """Compile a ProgramNode to a Python code object.

        Returns a code object ready for exec().
        """
        module = self.compile_to_ast(program)
        return compile(module, self.source_file, 'exec')

    def compile_to_ast(self, program: ProgramNode) -> pyast.Module:
        """Compile a ProgramNode to a Python ast.Module."""
        body = []

        # import lyric.compiled_runtime as _rt; register builtins
        preamble = self._emit_runtime_import()
        if isinstance(preamble, list):
            body.extend(preamble)
        else:
            body.append(preamble)

        # First pass: collect module-level variable names
        for stmt in program.statements:
            if isinstance(stmt, (AssignNode, TypeDeclarationNode)):
                name = stmt.name
                if '.' not in name:
                    self._module_level_vars.add(name)
            elif isinstance(stmt, MultiDeclarationNode):
                for _, var_name in stmt.declarations:
                    self._module_level_vars.add(var_name)

        # Second pass: compile
        for stmt in program.statements:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                body.extend(compiled)
            else:
                body.append(compiled)

        # If main() was defined, emit a call to it
        if 'main' in self._functions_defined:
            body.append(self._emit_main_call())

        module = pyast.Module(body=body, type_ignores=[])
        pyast.fix_missing_locations(module)
        return module

    # ── Helpers ──────────────────────────────────────────────────────

    def _loc(self, py_node, line=0, col=0):
        """Set source location on a Python AST node."""
        py_node.lineno = line or 1
        py_node.col_offset = col
        py_node.end_lineno = line or 1
        py_node.end_col_offset = col
        return py_node

    def _emit_runtime_import(self):
        """Emit: import lyric.compiled_runtime as _rt; _rt.register_builtins(globals())"""
        return [
            self._loc(pyast.Import(
                names=[pyast.alias(name='lyric.compiled_runtime', asname='_rt')]
            )),
            # _rt.register_builtins(globals()) — injects all builtins into compiled scope
            self._loc(pyast.Expr(value=self._rt_call(
                'register_builtins',
                [self._loc(pyast.Call(
                    func=self._name('globals'),
                    args=[], keywords=[]
                ))]
            ))),
        ]

    def _emit_main_call(self):
        """Emit main() call, passing argc/argv if main accepts parameters."""
        param_count = self._functions_defined.get('main', 0)
        if param_count >= 2:
            # main(argc, argv) — pass CLI args
            # _rt.call_main(main)
            return self._loc(pyast.Expr(
                value=self._rt_call('call_main', [
                    self._name('main'),
                ])
            ))
        else:
            # main() — no parameters
            return self._loc(pyast.Expr(
                value=self._loc(pyast.Call(
                    func=self._name('main'),
                    args=[],
                    keywords=[]
                ))
            ))

    def _name(self, name, ctx=None, line=0, col=0):
        """Create an ast.Name node."""
        if ctx is None:
            ctx = pyast.Load()
        return self._loc(pyast.Name(id=name, ctx=ctx), line, col)

    def _const(self, value, line=0, col=0):
        """Create an ast.Constant node."""
        return self._loc(pyast.Constant(value=value), line, col)

    def _rt_call(self, func_name, args, line=0, col=0):
        """Create a call to _rt.<func_name>(args...)."""
        return self._loc(pyast.Call(
            func=self._loc(pyast.Attribute(
                value=self._name('_rt'),
                attr=func_name,
                ctx=pyast.Load()
            ), line, col),
            args=args,
            keywords=[]
        ), line, col)

    # ── Statement Compilation ────────────────────────────────────────

    def _compile_statement(self, node):
        """Compile a Lyric statement node to Python AST statement(s)."""
        if isinstance(node, FunctionNode):
            return self._compile_function(node)
        elif isinstance(node, ClassNode):
            return self._compile_class(node)
        elif isinstance(node, AssignNode):
            return self._compile_assign(node)
        elif isinstance(node, TypeDeclarationNode):
            return self._compile_type_decl(node)
        elif isinstance(node, MultiDeclarationNode):
            return self._compile_multi_decl(node)
        elif isinstance(node, IfNode):
            return self._compile_if(node)
        elif isinstance(node, LoopNode):
            return self._compile_loop(node)
        elif isinstance(node, ReturnNode):
            return self._compile_return(node)
        elif isinstance(node, BreakNode):
            return self._loc(pyast.Break(), node.line, node.column)
        elif isinstance(node, ContinueNode):
            return self._loc(pyast.Continue(), node.line, node.column)
        elif isinstance(node, ImportPyNode):
            return self._compile_importpy(node)
        elif isinstance(node, ImportNode):
            return self._compile_import(node)
        elif isinstance(node, TryNode):
            return self._compile_try(node)
        elif isinstance(node, RaiseNode):
            return self._compile_raise(node)
        elif isinstance(node, FileOpNode):
            return self._compile_file_op(node)
        elif isinstance(node, ExecChainNode):
            return self._compile_exec_chain(node)
        elif isinstance(node, CallNode):
            return self._loc(pyast.Expr(
                value=self._compile_call(node)
            ), node.line, node.column)
        else:
            # For expressions used as statements
            expr = self._compile_expression(node)
            return self._loc(pyast.Expr(value=expr), getattr(node, 'line', 0), getattr(node, 'column', 0))

    def _compile_function(self, node: FunctionNode):
        """Compile a FunctionNode to a Python function definition.

        No upfront type checking — zero overhead on the happy path.
        The function body is wrapped in try/except TypeError to catch
        type mismatches and translate them into Lyric error messages.
        """
        self._functions_defined[node.name] = len(node.params)

        # Track return type for this function
        prev_return_type = self._current_function_return_type
        self._current_function_return_type = node.return_type
        prev_in_function = self._in_function
        self._in_function = True

        # Save and extend declared vars scope — params are implicitly declared
        prev_declared = self._declared_vars.copy()
        prev_type_reg = self._type_registry.copy()
        self._declared_vars.update(node.params)
        # Register typed params
        if node.param_types:
            for param, ptype in zip(node.params, node.param_types):
                if ptype and ptype != 'var':
                    self._type_registry[param] = ptype

        # Compile the actual function body
        inner_body = []

        # Inject global declarations for module-level variables used in this function
        # This ensures Python's scoping matches Lyric's flat scope model
        if self._module_level_vars:
            # Collect vars that are assigned in this function's body
            assigned_vars = self._collect_assigned_vars(node.body_statements)
            global_vars = assigned_vars & self._module_level_vars
            # Exclude function parameters
            global_vars -= set(node.params)
            if global_vars:
                inner_body.append(self._loc(pyast.Global(
                    names=sorted(global_vars)
                ), node.line, node.column))

        for stmt in node.body_statements:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                inner_body.extend(compiled)
            else:
                inner_body.append(compiled)

        if not inner_body:
            inner_body = [self._loc(pyast.Pass())]

        # Wrap body in try/except TypeError to catch type mismatches
        # and translate them into Lyric error messages.
        # Zero overhead on the happy path — only pays cost on error.
        # except TypeError as _e: _rt.handle_type_error(_e, 'func_name')
        body = [self._loc(pyast.Try(
            body=inner_body,
            handlers=[self._loc(pyast.ExceptHandler(
                type=self._name('TypeError'),
                name='_e',
                body=[self._loc(pyast.Expr(
                    value=self._rt_call('handle_type_error', [
                        self._name('_e'),
                        self._const(node.name),
                    ], node.line, node.column)
                ))]
            ))],
            orelse=[],
            finalbody=[]
        ), node.line, node.column)]

        # Build arguments — all params are plain Python args
        args = pyast.arguments(
            posonlyargs=[],
            args=[self._loc(pyast.arg(arg=p)) for p in node.params],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        )

        # Restore previous context
        self._current_function_return_type = prev_return_type
        self._in_function = prev_in_function
        self._declared_vars = prev_declared
        self._type_registry = prev_type_reg

        func_def = self._loc(pyast.FunctionDef(
            name=node.name,
            args=args,
            body=body,
            decorator_list=[],
            returns=None
        ), node.line, node.column)

        return func_def

    def _compile_assign(self, node: AssignNode):
        """Compile an AssignNode to a Python assignment."""
        value = self._compile_expression(node.expr)

        # Handle indexed assignment: obj[key] = val
        if '[' in node.name and ']' in node.name:
            bracket_start = node.name.index('[')
            bracket_end = node.name.index(']')
            obj_name = node.name[:bracket_start]
            key_str = node.name[bracket_start+1:bracket_end]

            # Build the object reference (may be dotted: self.items[k])
            if '.' in obj_name:
                parts = obj_name.split('.')
                obj = self._name(parts[0], pyast.Load(), node.line, node.column)
                for part in parts[1:]:
                    obj = self._loc(pyast.Attribute(
                        value=obj, attr=part, ctx=pyast.Load()
                    ), node.line, node.column)
            else:
                obj = self._name(obj_name, pyast.Load(), node.line, node.column)

            # Parse the key — could be int literal, variable name, or string key
            # The parser strips quotes, so we need to figure out what it is.
            # Use _rt.resolve_index_key() at runtime to check variable vs string.
            try:
                index_expr = self._const(int(key_str), node.line, node.column)
            except ValueError:
                # Could be a variable name or a bare string key.
                # Emit runtime resolution: tries variable lookup, falls back to string.
                index_expr = self._rt_call('resolve_index_key', [
                    self._const(key_str, node.line, node.column),
                    self._loc(pyast.Call(
                        func=self._name('locals'), args=[], keywords=[]
                    )),
                    self._loc(pyast.Call(
                        func=self._name('globals'), args=[], keywords=[]
                    )),
                ], node.line, node.column)

            target = self._loc(pyast.Subscript(
                value=obj,
                slice=index_expr,
                ctx=pyast.Store()
            ), node.line, node.column)

        # Handle dotted names (obj.attr = val)
        elif '.' in node.name:
            parts = node.name.split('.')
            # Build the attribute chain
            target = self._name(parts[0], pyast.Load(), node.line, node.column)
            for part in parts[1:-1]:
                target = self._loc(pyast.Attribute(
                    value=target, attr=part, ctx=pyast.Load()
                ), node.line, node.column)
            target = self._loc(pyast.Attribute(
                value=target, attr=parts[-1], ctx=pyast.Store()
            ), node.line, node.column)
        else:
            # Check variable is declared (compile-time enforcement)
            # Class body assignments are exempt (class member declarations)
            if node.name not in self._declared_vars and not self._in_class_body:
                from lyric.errors import RuntimeErrorLyric
                raise RuntimeErrorLyric(
                    f"Variable '{node.name}' is not declared. "
                    f"Use a type keyword to declare it first "
                    f"(e.g., var {node.name} = ..., int {node.name} = ..., str {node.name} = ...).",
                    node.line, node.column
                )
            target = self._name(node.name, pyast.Store(), node.line, node.column)

            # Enforce type on reassignment for typed variables (not var)
            if node.name in self._type_registry:
                value = self._rt_call('typed_assign', [
                    self._const(self._type_registry[node.name], node.line, node.column),
                    value,
                    self._const(node.name, node.line, node.column),
                ], node.line, node.column)

        return self._loc(pyast.Assign(
            targets=[target],
            value=value
        ), node.line, node.column)

    def _compile_type_decl(self, node: TypeDeclarationNode):
        """Compile a TypeDeclarationNode to a Python assignment.

        For 'var' type: no checking, just assign.
        For typed declarations: wrap value in _rt.typed_assign() for enforcement.
        """
        # Reject redeclaration of an already-declared variable
        # Class body declarations are exempt (each class has its own namespace)
        if node.name in self._declared_vars and not self._in_class_body:
            from lyric.errors import RuntimeErrorLyric
            raise RuntimeErrorLyric(
                f"Variable '{node.name}' is already declared. "
                f"Use '{node.name} = ...' to reassign, not a new declaration.",
                node.line, node.column
            )

        value = self._compile_expression(node.expr)
        target = self._name(node.name, pyast.Store(), node.line, node.column)

        # Track all declared variables
        self._declared_vars.add(node.name)

        if node.type_name != 'var':
            # Register type for reassignment enforcement
            self._type_registry[node.name] = node.type_name
            # Typed declaration: x = _rt.typed_assign('int', expr, 'x')
            value = self._rt_call('typed_assign', [
                self._const(node.type_name, node.line, node.column),
                value,
                self._const(node.name, node.line, node.column),
            ], node.line, node.column)

        return self._loc(pyast.Assign(
            targets=[target],
            value=value
        ), node.line, node.column)

    def _compile_multi_decl(self, node: MultiDeclarationNode):
        """Compile a MultiDeclarationNode to multiple assignments.

        Typed declarations get appropriate default values so that type
        detection works correctly (e.g., arr variables start as empty ArrObject).
        """
        stmts = []
        # Map Lyric types to default value constructors
        _TYPED_DEFAULTS = {'arr': 'make_arr', 'map': 'make_map', 'tup': 'make_tup'}
        for type_name, var_name in node.declarations:
            self._declared_vars.add(var_name)
            if type_name != 'var':
                self._type_registry[var_name] = type_name
            target = self._name(var_name, pyast.Store(), node.line, node.column)
            if type_name in _TYPED_DEFAULTS:
                # Initialize with empty typed container
                default_val = self._rt_call(_TYPED_DEFAULTS[type_name], [
                    self._loc(pyast.List(elts=[], ctx=pyast.Load()) if type_name != 'map'
                              else pyast.Dict(keys=[], values=[]))
                ], node.line, node.column)
            else:
                default_val = self._const(None, node.line, node.column)
            stmts.append(self._loc(pyast.Assign(
                targets=[target],
                value=default_val
            ), node.line, node.column))
        return stmts

    def _compile_if(self, node: IfNode):
        """Compile an IfNode to a Python if/elif/else."""
        test = self._compile_expression(node.condition)

        # Compile then body
        then_body = []
        for stmt in node.then_body:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                then_body.extend(compiled)
            else:
                then_body.append(compiled)
        if not then_body:
            then_body = [self._loc(pyast.Pass())]

        # Compile else body
        else_body = []
        if node.else_body:
            for stmt in node.else_body:
                compiled = self._compile_statement(stmt)
                if isinstance(compiled, list):
                    else_body.extend(compiled)
                else:
                    else_body.append(compiled)

        # Build elif chain from the inside out
        # Process elifs in reverse to nest them properly
        current_else = else_body if else_body else []
        for elif_cond, elif_body_stmts in reversed(node.elifs):
            elif_test = self._compile_expression(elif_cond)
            elif_body = []
            for stmt in elif_body_stmts:
                compiled = self._compile_statement(stmt)
                if isinstance(compiled, list):
                    elif_body.extend(compiled)
                else:
                    elif_body.append(compiled)
            if not elif_body:
                elif_body = [self._loc(pyast.Pass())]

            current_else = [self._loc(pyast.If(
                test=elif_test,
                body=elif_body,
                orelse=current_else
            ), elif_cond.line if hasattr(elif_cond, 'line') else 0,
               elif_cond.column if hasattr(elif_cond, 'column') else 0)]

        return self._loc(pyast.If(
            test=test,
            body=then_body,
            orelse=current_else
        ), node.line, node.column)

    def _compile_loop(self, node: LoopNode):
        """Compile a LoopNode to Python while or for."""
        # Compile loop body
        body = []
        for stmt in node.body:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                body.extend(compiled)
            else:
                body.append(compiled)
        if not body:
            body = [self._loc(pyast.Pass())]

        if node.loop_kind == 'iterator':
            # given var i in range(10): ... done
            # -> for i in range(10): ...
            iter_var = node.iterator_var or 'item'
            self._declared_vars.add(iter_var)
            if node.iterator_type and node.iterator_type != 'var':
                self._type_registry[iter_var] = node.iterator_type
            target = self._name(
                iter_var,
                pyast.Store(), node.line, node.column
            )
            iter_expr = self._compile_expression(node.condition_or_iter)

            return self._loc(pyast.For(
                target=target,
                iter=iter_expr,
                body=body,
                orelse=[]
            ), node.line, node.column)
        else:
            # given condition: ... done
            # -> while condition: ...
            test = self._compile_expression(node.condition_or_iter)

            return self._loc(pyast.While(
                test=test,
                body=body,
                orelse=[]
            ), node.line, node.column)

    def _compile_return(self, node: ReturnNode):
        """Compile a ReturnNode to a Python return statement."""
        if node.value is not None:
            value = self._compile_expression(node.value)
        else:
            value = None

        return self._loc(pyast.Return(value=value), node.line, node.column)

    def _compile_importpy(self, node: ImportPyNode):
        """Compile importpy to runtime calls.

        importpy time           -> time = _rt.lyric_importpy('time')
        importpy math; sin, cos -> _rt.lyric_importpy_selective('math', ['sin','cos'], globals())
        """
        if node.names:
            # Selective import: importpy math; sin, cos
            # Names are implicitly declared
            for n in node.names:
                self._declared_vars.add(n)
            names_list = self._loc(pyast.List(
                elts=[self._const(n, node.line, node.column) for n in node.names],
                ctx=pyast.Load()
            ), node.line, node.column)
            return self._loc(pyast.Expr(
                value=self._rt_call('lyric_importpy_selective', [
                    self._const(node.module_name, node.line, node.column),
                    names_list,
                    self._loc(pyast.Call(
                        func=self._name('globals'), args=[], keywords=[]
                    )),
                ], node.line, node.column)
            ), node.line, node.column)
        else:
            # Whole-module import
            binding_name = node.module_name.split('.')[-1]
            self._declared_vars.add(binding_name)
            return self._loc(pyast.Assign(
                targets=[self._name(binding_name, pyast.Store(), node.line, node.column)],
                value=self._rt_call('lyric_importpy', [
                    self._const(node.module_name, node.line, node.column)
                ], node.line, node.column)
            ), node.line, node.column)

    def _compile_import(self, node: ImportNode):
        """Compile a Lyric module import to a runtime call.

        import mymodule              -> mymodule = _rt.lyric_import('mymodule', __file__, globals())
        import lyric.math            -> _rt.lyric_import('lyric.math', __file__, globals())
        import lyric.math; sin, cos  -> _rt.lyric_import_selective('lyric.math', [('sin',None),('cos',None)], __file__, globals())
        """
        file_ref = self._name('__file__', pyast.Load(), node.line, node.column)
        globals_call = self._loc(pyast.Call(
            func=self._name('globals'), args=[], keywords=[]
        ))

        if node.symbols:
            # Selective import — register imported names as declared
            for name, alias in node.symbols:
                self._declared_vars.add(alias or name)
            symbols_list = self._loc(pyast.List(
                elts=[
                    self._loc(pyast.Tuple(
                        elts=[
                            self._const(name, node.line, node.column),
                            self._const(alias, node.line, node.column),
                        ],
                        ctx=pyast.Load()
                    ))
                    for name, alias in node.symbols
                ],
                ctx=pyast.Load()
            ), node.line, node.column)
            return self._loc(pyast.Expr(
                value=self._rt_call('lyric_import_selective', [
                    self._const(node.module_name, node.line, node.column),
                    symbols_list,
                    file_ref,
                    globals_call,
                ], node.line, node.column)
            ), node.line, node.column)
        else:
            # Whole-module import — register module name as declared
            self._declared_vars.add(node.module_name.split('.')[-1])
            return self._loc(pyast.Expr(
                value=self._rt_call('lyric_import', [
                    self._const(node.module_name, node.line, node.column),
                    file_ref,
                    globals_call,
                ], node.line, node.column)
            ), node.line, node.column)

    # ── Expression Compilation ───────────────────────────────────────

    def _compile_expression(self, node):
        """Compile a Lyric expression node to a Python AST expression."""
        if isinstance(node, LiteralNode):
            return self._const(node.value, node.line, node.column)

        elif isinstance(node, IdentifierNode):
            if '.' in node.name:
                # Dotted identifier: self.name, obj.attr.sub
                parts = node.name.split('.')
                result = self._name(parts[0], pyast.Load(), node.line, node.column)
                for part in parts[1:]:
                    result = self._loc(pyast.Attribute(
                        value=result, attr=part, ctx=pyast.Load()
                    ), node.line, node.column)
                return result
            return self._name(node.name, pyast.Load(), node.line, node.column)

        elif isinstance(node, BinaryOpNode):
            return self._compile_binary_op(node)

        elif isinstance(node, UnaryOpNode):
            return self._compile_unary_op(node)

        elif isinstance(node, CallNode):
            return self._compile_call(node)

        elif isinstance(node, ListLiteralNode):
            return self._compile_list_literal(node)

        elif isinstance(node, DictLiteralNode):
            return self._compile_dict_literal(node)

        elif isinstance(node, TupleLiteralNode):
            return self._compile_tuple_literal(node)

        elif isinstance(node, IndexNode):
            return self._compile_index(node)

        elif isinstance(node, SliceNode):
            return self._compile_slice(node)

        elif isinstance(node, RexNode):
            return self._compile_rex(node)

        elif isinstance(node, ExecChainNode):
            return self._compile_exec_chain_expr(node)

        else:
            raise NotImplementedError(
                f"Compiler does not yet support expression node: "
                f"{type(node).__name__} (use --interpret fallback)"
            )

    def _compile_binary_op(self, node: BinaryOpNode):
        """Compile a BinaryOpNode to Python AST."""
        left = self._compile_expression(node.left)
        right = self._compile_expression(node.right)
        line = node.line
        col = node.column

        # Comparison operators -> ast.Compare
        cmp_ops = {
            '<': pyast.Lt(), '<=': pyast.LtE(),
            '>': pyast.Gt(), '>=': pyast.GtE(),
            '==': pyast.Eq(), '!=': pyast.NotEq(),
        }
        if node.op in cmp_ops:
            return self._loc(pyast.Compare(
                left=left,
                ops=[cmp_ops[node.op]],
                comparators=[right]
            ), line, col)

        # Boolean operators -> ast.BoolOp
        if node.op == 'and':
            return self._loc(pyast.BoolOp(
                op=pyast.And(),
                values=[left, right]
            ), line, col)
        if node.op == 'or':
            return self._loc(pyast.BoolOp(
                op=pyast.Or(),
                values=[left, right]
            ), line, col)

        # Addition — needs runtime helper for string auto-coercion
        if node.op == '+':
            # Optimization: if both sides are known numeric literals, use direct add
            if (isinstance(node.left, LiteralNode) and isinstance(node.left.value, (int, float))
                    and isinstance(node.right, LiteralNode) and isinstance(node.right.value, (int, float))):
                return self._loc(pyast.BinOp(
                    left=left, op=pyast.Add(), right=right
                ), line, col)
            # Otherwise use runtime helper for string coercion
            return self._rt_call('lyric_add', [left, right], line, col)

        # Other arithmetic — direct Python ops
        arith_ops = {
            '-': pyast.Sub(),
            '*': pyast.Mult(),
            '**': pyast.Pow(),
        }
        if node.op in arith_ops:
            return self._loc(pyast.BinOp(
                left=left, op=arith_ops[node.op], right=right
            ), line, col)

        # Division — use runtime helper for zero-division check
        if node.op == '/':
            return self._rt_call('lyric_div', [left, right], line, col)
        if node.op == '//':
            return self._rt_call('lyric_floordiv', [left, right], line, col)

        # Modulo
        if node.op == '%':
            return self._rt_call('lyric_mod', [left, right], line, col)

        # Membership test
        if node.op == 'in':
            return self._loc(pyast.Compare(
                left=left,
                ops=[pyast.In()],
                comparators=[right]
            ), line, col)

        # Fallback for any unhandled operator
        raise NotImplementedError(
            f"Compiler does not yet support operator: {node.op}"
        )

    def _compile_unary_op(self, node: UnaryOpNode):
        """Compile a UnaryOpNode to Python AST."""
        operand = self._compile_expression(node.operand)

        if node.op == '-':
            op = pyast.USub()
        elif node.op == 'not':
            op = pyast.Not()
        elif node.op == '+':
            op = pyast.UAdd()
        else:
            raise NotImplementedError(f"Unary operator not supported: {node.op}")

        return self._loc(pyast.UnaryOp(op=op, operand=operand), node.line, node.column)

    def _compile_call(self, node: CallNode):
        """Compile a CallNode to a Python function call."""
        args = [self._compile_expression(arg) for arg in node.args]
        line = node.line
        col = node.column

        # Handle dotted function names (obj.method())
        if '.' in node.func_name:
            parts = node.func_name.split('.')
            method_name = parts[-1]

            # .len() → len(obj) — Lyric uses .len() but Python uses len()
            if method_name == 'len' and len(node.args) == 0:
                obj = self._name(parts[0], pyast.Load(), line, col)
                for part in parts[1:-1]:
                    obj = self._loc(pyast.Attribute(
                        value=obj, attr=part, ctx=pyast.Load()
                    ), line, col)
                return self._loc(pyast.Call(
                    func=self._name('len', pyast.Load(), line, col),
                    args=[obj],
                    keywords=[]
                ), line, col)

            func = self._name(parts[0], pyast.Load(), line, col)
            for part in parts[1:]:
                func = self._loc(pyast.Attribute(
                    value=func, attr=part, ctx=pyast.Load()
                ), line, col)
        else:
            # Simple function call
            func = self._name(node.func_name, pyast.Load(), line, col)

        return self._loc(pyast.Call(
            func=func,
            args=args,
            keywords=[]
        ), line, col)


    # ── Phase 4: Class Compilation ────────────────────────────────

    def _compile_class(self, node: ClassNode):
        """Compile a Lyric ClassNode to a native Python class.

        Lyric:
            class Dog extends Animal:
                var breed
                def Dog(str name, str breed) {
                    super(name)
                    self.breed = breed
                }
                def speak() {
                    return self.name + " barks"
                }
            +++

        Python:
            class Dog(Animal):
                def __init__(self, name, breed):
                    super().__init__(name)
                    self.breed = breed
                def speak(self):
                    return self.name + " barks"
        """
        class_body = []

        # Compile member variables (TypeDeclarationNode, AssignNode, MultiDeclarationNode)
        self._in_class_body = True
        for member in node.members_statements:
            if isinstance(member, (AssignNode, TypeDeclarationNode)):
                compiled = self._compile_statement(member)
                if isinstance(compiled, list):
                    class_body.extend(compiled)
                else:
                    class_body.append(compiled)
            elif isinstance(member, MultiDeclarationNode):
                compiled = self._compile_multi_decl(member)
                if isinstance(compiled, list):
                    class_body.extend(compiled)
                else:
                    class_body.append(compiled)
            elif isinstance(member, FunctionNode):
                # Compile method — add 'self' as first parameter
                class_body.append(self._compile_method(member))

        self._in_class_body = False

        # Compile constructor if present
        has_constructor = False
        if node.constructor_method:
            class_body.append(self._compile_constructor(node.constructor_method, node.base_class))
            has_constructor = True

        if not has_constructor:
            # Check for init() method as fallback constructor
            # Remove the init method from class_body (it was compiled as a regular method)
            # and recompile it as __init__
            for member in node.members_statements:
                if isinstance(member, FunctionNode) and member.name == 'init':
                    class_body = [m for m in class_body
                                  if not (isinstance(m, pyast.FunctionDef) and m.name == 'init')]
                    class_body.append(self._compile_constructor(member, node.base_class))
                    break

        if not class_body:
            class_body = [self._loc(pyast.Pass())]

        # Build base classes list
        bases = []
        if node.base_class:
            bases.append(self._name(node.base_class, pyast.Load(), node.line, node.column))

        class_def = self._loc(pyast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=class_body,
            decorator_list=[]
        ), node.line, node.column)

        return class_def

    def _compile_constructor(self, node: FunctionNode, base_class=None):
        """Compile a Lyric constructor to Python __init__.

        Adds 'self' as first param. Does NOT auto-call super().__init__()
        because Lyric constructors typically set all fields directly.
        Return statements with values are converted to bare returns since
        Python's __init__ cannot return a value.
        """
        # Save and extend declared vars scope — params are implicitly declared
        prev_declared = self._declared_vars.copy()
        prev_type_reg = self._type_registry.copy()
        self._declared_vars.update(node.params)

        body = []

        for stmt in node.body_statements:
            # Convert return-with-value to bare return in constructors
            if isinstance(stmt, ReturnNode) and stmt.value is not None:
                body.append(self._loc(pyast.Return(value=None), stmt.line, stmt.column))
                continue
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                body.extend(compiled)
            else:
                body.append(compiled)

        if not body:
            body = [self._loc(pyast.Pass())]

        # Build args with 'self' prepended
        params = ['self'] + list(node.params)
        args = pyast.arguments(
            posonlyargs=[],
            args=[self._loc(pyast.arg(arg=p)) for p in params],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        )

        # Restore scope
        self._declared_vars = prev_declared
        self._type_registry = prev_type_reg

        return self._loc(pyast.FunctionDef(
            name='__init__',
            args=args,
            body=body,
            decorator_list=[],
            returns=None
        ), node.line, node.column)

    def _compile_method(self, node: FunctionNode):
        """Compile a Lyric method to a Python method with 'self' param."""
        # Save and extend declared vars scope — params are implicitly declared
        prev_declared = self._declared_vars.copy()
        prev_type_reg = self._type_registry.copy()
        self._declared_vars.update(node.params)

        body = []
        for stmt in node.body_statements:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                body.extend(compiled)
            else:
                body.append(compiled)

        if not body:
            body = [self._loc(pyast.Pass())]

        # Build args with 'self' prepended
        params = ['self'] + list(node.params)
        args = pyast.arguments(
            posonlyargs=[],
            args=[self._loc(pyast.arg(arg=p)) for p in params],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        )

        # Restore scope
        self._declared_vars = prev_declared
        self._type_registry = prev_type_reg

        return self._loc(pyast.FunctionDef(
            name=node.name,
            args=args,
            body=body,
            decorator_list=[],
            returns=None
        ), node.line, node.column)

    # ── Phase 2: Collection and Index Compilation ─────────────────

    def _compile_list_literal(self, node: ListLiteralNode):
        """Compile [a, b, c] to _rt.make_arr([a, b, c])."""
        elements = [self._compile_expression(e) for e in node.elements]
        return self._rt_call('make_arr', [
            self._loc(pyast.List(elts=elements, ctx=pyast.Load()), node.line, node.column)
        ], node.line, node.column)

    def _compile_dict_literal(self, node: DictLiteralNode):
        """Compile {"a": 1} to _rt.make_map({...})."""
        keys = [self._compile_expression(k) for k, v in node.pairs]
        values = [self._compile_expression(v) for k, v in node.pairs]
        return self._rt_call('make_map', [
            self._loc(pyast.Dict(keys=keys, values=values), node.line, node.column)
        ], node.line, node.column)

    def _compile_tuple_literal(self, node: TupleLiteralNode):
        """Compile (a, b, c) to _rt.make_tup([a, b, c])."""
        elements = [self._compile_expression(e) for e in node.elements]
        return self._rt_call('make_tup', [
            self._loc(pyast.List(elts=elements, ctx=pyast.Load()), node.line, node.column)
        ], node.line, node.column)

    def _compile_index(self, node: IndexNode):
        """Compile obj[index] to a subscript operation."""
        obj = self._compile_expression(node.obj)
        index = self._compile_expression(node.index)
        return self._loc(pyast.Subscript(
            value=obj,
            slice=index,
            ctx=pyast.Load()
        ), node.line, node.column)

    def _compile_slice(self, node: SliceNode):
        """Compile obj[start:end:step] to a slice operation."""
        obj = self._compile_expression(node.obj)
        lower = self._compile_expression(node.start) if node.start else None
        upper = self._compile_expression(node.end) if node.end else None
        step = self._compile_expression(node.step) if node.step else None

        return self._loc(pyast.Subscript(
            value=obj,
            slice=self._loc(pyast.Slice(lower=lower, upper=upper, step=step),
                            node.line, node.column),
            ctx=pyast.Load()
        ), node.line, node.column)


    # ── Phase 6: Try/Catch/Raise, File Ops, Exec Chains ───────────

    def _compile_try(self, node: TryNode):
        """Compile try/catch/finally to Python try/except/finally."""
        # Compile try body
        try_body = self._compile_body(node.try_body)

        # Compile catch clauses -> except handlers
        handlers = []
        for clause in node.catch_clauses:
            handler_body = self._compile_body(clause.body)

            # Map Lyric exception type to Python exception type
            if clause.exception_type:
                exc_type = self._rt_call('get_exception_type', [
                    self._const(clause.exception_type, clause.line, clause.column)
                ], clause.line, clause.column)
            else:
                exc_type = self._name('Exception')

            # Catch variable is implicitly declared
            if clause.variable_name:
                self._declared_vars.add(clause.variable_name)
            handlers.append(self._loc(pyast.ExceptHandler(
                type=exc_type,
                name=clause.variable_name,
                body=handler_body
            ), clause.line, clause.column))

        # Compile finally body
        finalbody = []
        if node.finally_body:
            finalbody = self._compile_body(node.finally_body)

        return self._loc(pyast.Try(
            body=try_body,
            handlers=handlers,
            orelse=[],
            finalbody=finalbody
        ), node.line, node.column)

    def _compile_raise(self, node: RaiseNode):
        """Compile raise statement to Python raise."""
        # _rt.lyric_raise('ExceptionName')
        return self._loc(pyast.Expr(
            value=self._rt_call('lyric_raise', [
                self._const(node.exception_name, node.line, node.column)
            ], node.line, node.column)
        ), node.line, node.column)

    def _compile_file_op(self, node: FileOpNode):
        """Compile file operators (->>, ->, <-) to runtime calls."""
        if node.operator == '<-':
            # Check for exec("cmd") <- input_data
            if isinstance(node.left, CallNode) and node.left.func_name == 'exec':
                cmd = self._compile_expression(node.left.args[0])
                input_data = self._compile_expression(node.right)
                return self._loc(pyast.Expr(
                    value=self._rt_call('lyric_exec_with_input', [
                        cmd, input_data,
                    ], node.line, node.column)
                ), node.line, node.column)

            # Read: variable <- dsk  →  variable = _rt.lyric_file_read(dsk, variable)
            # Pass current value of variable so runtime can detect arr type
            right = self._compile_expression(node.right)
            if isinstance(node.left, IdentifierNode):
                target = self._name(node.left.name, pyast.Store(), node.line, node.column)
                current_val = self._name(node.left.name, pyast.Load(), node.line, node.column)
                return self._loc(pyast.Assign(
                    targets=[target],
                    value=self._rt_call('lyric_file_read', [
                        right,
                        current_val,
                    ], node.line, node.column)
                ), node.line, node.column)

        # Check for print -> file or print ->> file
        if isinstance(node.left, CallNode) and node.left.func_name == 'print':
            # print "text" -> file: write print output to file instead of stdout
            args = [self._compile_expression(arg) for arg in node.left.args]
            right = self._compile_expression(node.right)
            args_list = self._loc(pyast.List(elts=args, ctx=pyast.Load()))
            return self._loc(pyast.Expr(
                value=self._rt_call('lyric_print_to_file', [
                    self._const(node.operator, node.line, node.column),
                    args_list,
                    right,
                ], node.line, node.column)
            ), node.line, node.column)

        # Check for exec() -> var or exec() ->> file
        if isinstance(node.left, CallNode) and node.left.func_name == 'exec':
            left = self._compile_expression(node.left)
            right = self._compile_expression(node.right)
            if node.operator == '->' and isinstance(node.right, IdentifierNode):
                # exec("cmd") -> var: capture output to variable
                target = self._name(node.right.name, pyast.Store(), node.line, node.column)
                return self._loc(pyast.Assign(
                    targets=[target],
                    value=self._rt_call('lyric_exec_capture', [
                        self._compile_expression(node.left.args[0]),
                    ], node.line, node.column)
                ), node.line, node.column)
            else:
                # exec("cmd") ->> file
                return self._loc(pyast.Expr(
                    value=self._rt_call('lyric_exec_to_file', [
                        self._const(node.operator),
                        self._compile_expression(node.left.args[0]),
                        right,
                    ], node.line, node.column)
                ), node.line, node.column)

        # Check for exec chain -> var or exec chain ->> file
        if isinstance(node.left, ExecChainNode):
            # Build a temporary ExecChainNode expression to reuse _compile_exec_chain_expr
            chain_expr = self._compile_exec_chain_expr(node.left)
            if node.operator == '->' and isinstance(node.right, IdentifierNode):
                # exec chain -> var: capture final output to variable
                target = self._name(node.right.name, pyast.Store(), node.line, node.column)
                # Override output_target to True to signal "return output"
                chain_expr.args[3] = self._const(True)
                return self._loc(pyast.Assign(
                    targets=[target],
                    value=chain_expr
                ), node.line, node.column)
            else:
                # exec chain ->> file: set output_target=True to get output string
                chain_expr.args[3] = self._const(True)
                right = self._compile_expression(node.right)
                return self._loc(pyast.Expr(
                    value=self._rt_call('lyric_exec_chain_to_file', [
                        self._const(node.operator),
                        chain_expr,
                        right,
                    ], node.line, node.column)
                ), node.line, node.column)

        # Write/append: expr -> dsk or expr ->> dsk
        left = self._compile_expression(node.left)
        right = self._compile_expression(node.right)

        return self._loc(pyast.Expr(
            value=self._rt_call('lyric_file_op', [
                self._const(node.operator, node.line, node.column),
                left,
                right,
            ], node.line, node.column)
        ), node.line, node.column)

    def _compile_exec_chain(self, node: ExecChainNode):
        """Compile exec chain as a statement."""
        return self._loc(pyast.Expr(
            value=self._compile_exec_chain_expr(node)
        ), getattr(node, 'line', 0), getattr(node, 'column', 0))

    def _compile_exec_chain_expr(self, node: ExecChainNode):
        """Compile exec chain (exec('a') | exec('b')) to runtime call.

        Extract command strings from exec() CallNodes instead of evaluating them,
        since the chain runtime needs to manage subprocess piping itself.
        """
        # Extract command strings from exec() calls
        cmd_elts = []
        for e in node.elements:
            if isinstance(e, CallNode) and e.func_name == 'exec' and e.args:
                # Extract the command argument string
                cmd_elts.append(self._compile_expression(e.args[0]))
            elif isinstance(e, CallNode) and e.func_name == 'print':
                # print in chain — pass as special marker
                cmd_elts.append(self._const('__print__'))
            else:
                cmd_elts.append(self._compile_expression(e))

        elements = self._loc(pyast.List(elts=cmd_elts, ctx=pyast.Load()))
        operators = self._loc(pyast.List(
            elts=[self._const(op) for op in node.operators],
            ctx=pyast.Load()
        ))

        input_src = self._compile_expression(node.input_source) if node.input_source else self._const(None)
        output_tgt = self._compile_expression(node.output_target) if node.output_target else self._const(None)

        return self._rt_call('lyric_exec_chain', [
            elements, operators, input_src, output_tgt
        ], node.line, node.column)

    def _collect_assigned_vars(self, stmts):
        """Recursively collect all variable names that are assigned in a list of statements."""
        assigned = set()
        for stmt in stmts:
            if isinstance(stmt, AssignNode):
                name = stmt.name.split('.')[0]  # Get base name for dotted assigns
                if '.' not in stmt.name:  # Only track simple assigns, not self.x
                    assigned.add(name)
            elif isinstance(stmt, TypeDeclarationNode):
                assigned.add(stmt.name)
            elif isinstance(stmt, IfNode):
                assigned |= self._collect_assigned_vars(stmt.then_body)
                for _, elif_body in stmt.elifs:
                    assigned |= self._collect_assigned_vars(elif_body)
                if stmt.else_body:
                    assigned |= self._collect_assigned_vars(stmt.else_body)
            elif isinstance(stmt, LoopNode):
                assigned |= self._collect_assigned_vars(stmt.body)
                if stmt.iterator_var:
                    assigned.add(stmt.iterator_var)
            elif isinstance(stmt, TryNode):
                assigned |= self._collect_assigned_vars(stmt.try_body)
                for clause in stmt.catch_clauses:
                    assigned |= self._collect_assigned_vars(clause.body)
                if stmt.finally_body:
                    assigned |= self._collect_assigned_vars(stmt.finally_body)
        return assigned

    def _compile_body(self, stmts):
        """Helper to compile a list of statements into a body."""
        body = []
        for stmt in stmts:
            compiled = self._compile_statement(stmt)
            if isinstance(compiled, list):
                body.extend(compiled)
            else:
                body.append(compiled)
        if not body:
            body = [self._loc(pyast.Pass())]
        return body

    # ── Phase 3: Regex Literal ────────────────────────────────────

    def _compile_rex(self, node: RexNode):
        """Compile /pattern/ to _rt.make_rex('pattern')."""
        return self._rt_call('make_rex', [
            self._const(node.pattern, node.line, node.column)
        ], node.line, node.column)


def compile_lyric(program: ProgramNode, source_file='<lyric>'):
    """Convenience function to compile a Lyric AST to a code object."""
    compiler = LyricCompiler(source_file)
    return compiler.compile(program)
