import ast
from rbnf.core.Tokenizer import Tokenizer
from rbnf.std.common import recover_codes
import typing as t


class Node(ast.expr):
    col_offset = 1
    lineno = 1


class ClauseC(Node):
    begin_sign: Tokenizer
    clause: str

    def __init__(self, begin_sign: Tokenizer, clause: t.List[Tokenizer]):
        super().__init__()
        self.begin_sign = begin_sign
        self.clause = recover_codes(clause)
        self.lineno = begin_sign.lineno
        self.col_offset = begin_sign.colno

    _fields = ('begin_sign', 'clause')


class LexerC(Node):
    name: str
    lexers: t.Optional[t.List[str]]
    is_const: bool

    def __init__(self, name: Tokenizer, lexers, is_const):
        super().__init__()
        self.lineno = name.lineno
        self.col_offset = name.colno
        self.name = name.value
        self.lexers = [each.valuue for each in lexers] if isinstance(
            lexers, list) else None
        self.is_const = is_const

    _fields = ('name', 'lexers', 'is_const')


class ParserC(Node):
    name: str
    impl: Node

    def __init__(self, name: Tokenizer, impl):
        super().__init__()
        self.lineno = name.lineno
        self.col_offset = name.colno
        self.name = name.value
        self.impl = impl

    _fields = ('name', 'impl')


class OrParser(Node):
    brs: t.List[Node]

    def __init__(self, brs: t.List[Node]):
        super().__init__()
        self.brs = brs

    _fields = ('brs', )


class AndParser(Node):
    pats: t.List[Node]

    def __init__(self, pats: t.List[Node]):
        super().__init__()
        self.pats = pats

    _fields = ('pats', )


class RepC(Node):
    least: int
    most: int
    expr: Node

    def __init__(self, pat: t.List[Tokenizer], expr):
        super().__init__()
        if len(pat) is 1:
            self.least = int(pat[0].value)
            self.most = -1
        else:
            self.least, self.most = map(lambda _: int(_.value), pat)
        self.expr = expr

    _fields = ('least', 'most', 'expr')


class OptionalC(Node):

    expr: Node

    def __init__(self, expr: Node):
        super().__init__()
        self.expr = expr

    _fields = ('expr', )


class StarC(Node):

    expr: Node

    def __init__(self, expr: Node):
        super().__init__()
        self.expr = expr

    _fields = ('expr', )


class PlusC(Node):

    expr: Node

    def __init__(self, expr: Node):
        super().__init__()
        self.expr = expr

    _fields = ('expr', )


class RewriteC(Node):
    rewrite: str
    expr: Node

    def __init__(self, rewrite: Tokenizer, expr: Node):
        super().__init__()
        self.lineno = rewrite.lineno
        self.col_offset = rewrite.colno
        self.rewrite = rewrite.value
        self.expr = expr

    _fields = ('expr', 'rewrite')


class PredicateC(Node):
    predicate: str
    expr: Node

    def __init__(self, predicate: Tokenizer, expr: Node):
        super().__init__()
        self.lineno = predicate.lineno
        self.col_offset = predicate.colno
        self.predicate = predicate.value
        self.expr = expr

    _fields = ('expr', 'predicate')


class BindC(Node):
    bind_name: str
    expr: Node

    def __init__(self, predicate: Tokenizer, expr: Node):
        super().__init__()
        self.lineno = predicate.lineno
        self.col_offset = predicate.colno
        self.bind_name = predicate.value
        self.expr = expr

    _fields = ('expr', 'bind_name')


class PushC(Node):
    bind_name: str
    expr: Node

    def __init__(self, predicate: Tokenizer, expr: Node):
        super().__init__()
        self.lineno = predicate.lineno
        self.col_offset = predicate.colno
        self.bind_name = predicate.value
        self.expr = expr

    _fields = ('expr', 'bind_name')


class RefC(Node):

    sym: str

    def __init__(self, sym: Tokenizer):
        super().__init__()
        self.sym = sym.value
        self.lineno = sym.lineno
        self.col_offset = sym.colno

    _fields = ('sym', )


class LiteralC(Node):
    prefix: str
    value: str

    def __init__(self, lit: Tokenizer):
        super().__init__()
        self.lineno = lit.lineno
        self.col_offset = lit.colno
        value: str = lit.value
        if value.startswith('\''):
            self.value = value[1:-1]
            self.prefix = None
        else:
            self.value = value[2:-1]
            self.prefix = value[0]

    _fields = ('prefix', 'value')