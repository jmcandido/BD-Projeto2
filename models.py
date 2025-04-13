# models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Cliente:
    id: int = None
    nome: str = ""
    torce_flamengo: bool = False
    assiste_one_piece: bool = False
    e_de_sousa: bool = False
    # Outros atributos (ex.: email, telefone) podem ser adicionados

@dataclass
class Produto:
    id: int = None
    nome: str = ""
    preco: float = 0.0
    categoria: str = ""
    fabricado_em_mari: bool = False
    estoque: int = 0

@dataclass
class Vendedor:
    id: int = None
    nome: str = ""

@dataclass
class ItemCompra:
    id: int = None
    produto: Produto = None
    quantidade: int = 0

@dataclass
class Compra:
    id: int = None
    cliente: Cliente = None
    vendedor: Vendedor = None
    itens: List[ItemCompra] = field(default_factory=list)
    forma_pagamento: str = ""
    status_pagamento: str = "Pendente"  # Ex: "Pendente", "Confirmado"
# models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Cliente:
    id: int = None
    nome: str = ""
    torce_flamengo: bool = False
    assiste_one_piece: bool = False
    e_de_sousa: bool = False
    # Outros atributos (ex.: email, telefone) podem ser adicionados

@dataclass
class Produto:
    id: int = None
    nome: str = ""
    preco: float = 0.0
    categoria: str = ""
    fabricado_em_mari: bool = False
    estoque: int = 0

@dataclass
class Vendedor:
    id: int = None
    nome: str = ""

@dataclass
class ItemCompra:
    id: int = None
    produto: Produto = None
    quantidade: int = 0

@dataclass
class Compra:
    id: int = None
    cliente: Cliente = None
    vendedor: Vendedor = None
    itens: List[ItemCompra] = field(default_factory=list)
    forma_pagamento: str = ""
    status_pagamento: str = "Pendente"  # Ex: "Pendente", "Confirmado"
