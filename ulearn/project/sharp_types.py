from dataclasses import dataclass


@dataclass
class CSharpClass:
    modifiers: list[str]
    name: str
    body: list  #: list[CSharpVar | CSharpMethod]
    generic_types: list  # CSharpClass

    @property
    def just_typename(self):
        typename = self.name
        if self.generic_types:
            typename+= f"<{', '.join(self.generic_types)}>"
        return typename
    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + ' '
        signature += f"class {self.name}"
        if self.generic_types:
            signature += f"<{', '.join(self.generic_types)}>"
        signature += " {\n"
        for thing in self.body:
            thing: CSharpVar | CSharpMethod
            signature += " " * 4 + str(thing) + '\n'
        signature += "}"
        return signature


@dataclass
class CSharpVar:
    modifiers: list[str]
    var_type: CSharpClass
    name: str

    @property
    def as_param(self):
        return f"{self.var_type.just_typename} {self.name}"
    def __repr__(self):
        return f"{' '.join(self.modifiers)} {self.var_type.just_typename} {self.name};"


@dataclass
class CSharpMethod:
    modifiers: list[str]
    return_type: CSharpClass
    name: str
    arguments: list[CSharpVar]

    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + " "
        signature += str(self.return_type.just_typename) + " "
        signature += self.name+" "
        signature += " (" + ', '.join(x.as_param for x in self.arguments) +")"
        return signature+";"
