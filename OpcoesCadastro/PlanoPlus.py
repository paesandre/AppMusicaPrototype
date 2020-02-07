from OpcoesCadastro.Cadastro import Cadastro

class PlanoPlus(Cadastro):
    def __init__(self, nome, email, telefone, senha, numCartao):
        super().__init__(nome, email, telefone, senha)
        self.numCartao = numCartao