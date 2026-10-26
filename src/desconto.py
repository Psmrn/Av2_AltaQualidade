"""Exemplo didático de desconto aplicando os princípios L, I e D do SOLID (Aula 06)."""

import abc


# ----------------------------------------------------------------------
# Abstração principal (contrato) de desconto
# ----------------------------------------------------------------------
class IDesconto(abc.ABC):
    """Contrato: todo desconto sabe calcular o valor a ser descontado."""

    @abc.abstractmethod
    def calcular(self, valor: float) -> float:
        raise NotImplementedError


# ----------------------------------------------------------------------
# LSP: qualquer filha pode substituir IDesconto sem quebrar o programa
# ----------------------------------------------------------------------
class DescontoNormal(IDesconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.1


class DescontoPremium(IDesconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.3


def aplicar_desconto(desconto: IDesconto, valor: float) -> float:
    """Funciona com qualquer implementação de IDesconto (LSP)."""
    return desconto.calcular(valor)


# ----------------------------------------------------------------------
# ISP: interfaces pequenas e específicas, em vez de uma interface "gorda"
# ----------------------------------------------------------------------
class ICupom(abc.ABC):
    @abc.abstractmethod
    def aplicar_cupom(self, codigo: str) -> bool:
        raise NotImplementedError


class IVIP(abc.ABC):
    @abc.abstractmethod
    def validar_usuario_vip(self, usuario: str) -> bool:
        raise NotImplementedError


class DescontoVIP(IDesconto, ICupom, IVIP):
    """Só o desconto VIP implementa cupom e validação VIP; DescontoNormal não é obrigado a isso."""

    def calcular(self, valor: float) -> float:
        return valor * 0.2

    def aplicar_cupom(self, codigo: str) -> bool:
        return True

    def validar_usuario_vip(self, usuario: str) -> bool:
        return usuario == "vip"


def aplicar_cupom(cupom: ICupom, codigo: str) -> bool:
    """Depende apenas da interface de cupom (ISP)."""
    return cupom.aplicar_cupom(codigo)


# ----------------------------------------------------------------------
# DIP: Pedido depende da abstração IDesconto, não de uma classe concreta
# ----------------------------------------------------------------------
class Pedido:
    def __init__(self, desconto: IDesconto) -> None:
        self.desconto = desconto  # A implementação é injetada de fora

    def total(self, valor: float) -> float:
        return valor - self.desconto.calcular(valor)


if __name__ == "__main__":  # pragma: no cover
    valor = 100

    # LSP
    print("Normal:", aplicar_desconto(DescontoNormal(), valor))
    print("VIP:", aplicar_desconto(DescontoVIP(), valor))
    print("Premium:", aplicar_desconto(DescontoPremium(), valor))

    # ISP
    vip = DescontoVIP()
    print("Cupom VIP:", aplicar_cupom(vip, "DESC10"))

    # DIP
    pedido_normal = Pedido(DescontoNormal())
    pedido_vip = Pedido(DescontoVIP())
    pedido_premium = Pedido(DescontoPremium())
    print("Total normal:", pedido_normal.total(valor))
    print("Total VIP:", pedido_vip.total(valor))
    print("Total premium:", pedido_premium.total(valor))