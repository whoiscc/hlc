from contextlib import contextmanager


class Function:
    def __init__(self, identifier, return_ty):
        self.id = identifier
        self.return_ty = return_ty
        self.params = []
        self.block = Block()

    def declare_param(self, var):
        self.params.append(var)

    # utils
    def __iadd__(self, var):
        self.declare_param(var)
        return self


class Block:
    def __init__(self):
        self.stmts = []
        self.vars = []

    def declare(self, var):
        self.vars.append(var)
        self.stmts.append(Declare(var))

    def append(self, stmt):
        self.stmts.append(stmt)

    # utils
    def __ilshift__(self, stmt):
        self.append(stmt)
        return self

    def __iadd__(self, var):
        self.declare(var)
        return self

    @contextmanager
    def loop(self, check):
        block = Block()
        try:
            yield block
        finally:
            self.append(Loop(check, block))

    def cases(self):
        return Cases(self)


class Cases:
    def __init__(self, block):
        self.block = block
        self.branch = None

    @contextmanager
    def when(self, check):
        if self.branch is not None:
            self.block = self.branch.neg
            self.branch = None
        branch = Branch(check, Block(), Block())
        try:
            yield branch.pos
        finally:
            self.branch = branch
            self.block.append(branch)

    @contextmanager
    def otherwise(self):
        assert self.branch is not None
        yield self.branch.neg


class Variable:
    def __init__(self, ty):
        self.ty = ty


class Declare:
    def __init__(self, var):
        self.var = var


class Loop:
    def __init__(self, check, block):
        self.check = check
        self.block = block


class Branch:
    def __init__(self, check, pos, neg):
        self.check = check
        self.pos = pos
        self.neg = neg


class Literal:
    def __init__(self, value):
        self.value = value


class Op:
    def __init__(self, operator, exprs):
        self.operator = operator
        self.exprs = exprs


# def write(term, writer):
#     pass
