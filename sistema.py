from datetime import datetime
import pytz
from random import randint

class ContaCorrente:
    """
    Cria um objeto ContaCorrente para gerenciar a conta dos clientes.

    Atributos:
        titular (str): Nome do Cliente
        cpf (str): CPF do Cliente
        saldo (int): Saldo na Conta do Cliente
        limite (int): Limite do Cheque Especial do Cliente
        agencia (str): Agencia do Cliente
        numero_conta (str): Número da Conta do Cliente
        transacoes (list): Extrato da Conta do Cliente
    """

    @staticmethod
    def _consultar_data_hora():
        fuso_br = pytz.timezone('Brazil/East')
        return datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M:%S")

    def _gerar_numero_conta():
        return '{}'.format(randint(100000000, 999999999))

    def _gerar_numero_agencia():
        return '{}'.format(randint(1000, 9999))

    def __init__(self, titular, cpf):
        self.titular = titular
        self.cpf = cpf
        self._saldo = 0
        self._limite = None
        self.agencia = ContaCorrente._gerar_numero_agencia()
        self.numero_conta = ContaCorrente._gerar_numero_conta()
        self._transacoes = []
        self.cartoes = []

    def consultar_saldo(self):
        print("Seu saldo atual é de R${:,.2f}".format(self._saldo))

    def depositar_dinheiro(self, valor):
        self._saldo += valor
        self._transacoes.append("Tipo: Depósito - Valor: R${:,.2f} - Novo Saldo: R${:,.2f} - Horário: {}".format(valor, self._saldo, ContaCorrente._consultar_data_hora()))

    def _limite_conta(self):
        self._limite = -1000
        return self._limite

    def consultar_limite_especial(self):
        print("Seu limite de Cheque Especial é de {:,.2f}".format(self._limite_conta()))

    def sacar_dinheiro(self, valor):
        if self._saldo - valor < self._limite_conta():
            print("Você não tem saldo suficiente para sacer esse valor.")
            self.consultar_saldo()
        else:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            self._transacoes.append("Tipo: Saque - Valor: R${:,.2f} - Novo Saldo: R${:,.2f} - Horário: {}".format(valor, self._saldo, ContaCorrente._consultar_data_hora()))
    
    def consultar_transacoes(self):
        print("\nTransações")
        for transacao in self._transacoes:
            print(transacao)
            print('-----------------')

    def transferir(self, valor, conta_destino):
        self._saldo -= valor
        conta_destino._saldo += valor
        self._transacoes.append("Tipo: Enviou Pix - Valor: R${:,.2f} - Novo Saldo: R${:,.2f} - Horário: {}".format(valor, self._saldo, ContaCorrente._consultar_data_hora()))
        conta_destino._transacoes.append("Tipo: Recebeu Pix - Valor: R${:,.2f} - Novo Saldo: R${:,.2f} - Horário: {}".format(valor, conta_destino._saldo, ContaCorrente._consultar_data_hora()))


class CartaoCredito:
    """
    Cria um objeto CartaoCredito e adiciona no objeto ContaCorrente.

    Atributos:
        titular (str): Nome do Titular do Cartão de Crédito
        _numero (str): Número do Cartão de Crédito
        _validade (str): Validade do Cartão de Crédito
        _cod_seguranca (str): Código de Segurança do Cartão de Crédito
        _senha (str): Senha do Cartão de Crédito
        limite (int): Limite do Cartãoo de Crédito
        conta_corrente (obj): Conta Corrente associada ao Cartão de Crédito
    """

    @staticmethod
    def _data_hora():
        fuso_br = pytz.timezone('Brazil/East')
        return datetime.now(fuso_br)
        
    def _gerar_codigo_seguranca():
        return '{}{}{}'.format(randint(0, 9), randint(0, 9), randint(0, 9))

    def _gerar_numero_cartao():
        return '{}'.format(randint(1000000000000000, 9999999999999999))
    
    def _gerar_validade_cartao():
        return '{}/{}'.format(CartaoCredito._data_hora().month, CartaoCredito._data_hora().year + 4)

    def __init__(self, titular, conta_corrente):
        self.titular = titular
        self._numero = CartaoCredito._gerar_numero_cartao()
        self._validade = CartaoCredito._gerar_validade_cartao()
        self._cod_seguranca = CartaoCredito._gerar_codigo_seguranca()
        self._senha = '1234'
        self.limite = 1000
        self.conta_corrente = conta_corrente
        conta_corrente.cartoes.append(self)

    @property
    def senha(self):
        return self.senha
    
    @senha.setter
    def senha(self, nova_senha):
        if len(nova_senha) == 4 and nova_senha.isnumeric():
            self._senha = nova_senha
            print("Senha alterada com sucesso.")
        else:
            print("Não foi possível alterar a senha.")
