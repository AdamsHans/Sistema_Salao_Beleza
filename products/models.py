from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Funcionário'

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Serviço')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'

    def __str__(self):
        return f'{self.nome} ({self.telefone})'


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='agendamentos')
    data_hora = models.DateTimeField(verbose_name='Data e Hora')
    servicos = models.ManyToManyField(Servico, verbose_name='Serviços')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='agendado')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Agendamento'

    def __str__(self):
        return f'Agendamento de {self.cliente.nome} com {self.funcionario.nome} em {self.data_hora.strftime("%d/%m/%Y %H:%M")}'

from django.db import models
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome do Produto')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço Unitário')
    quantidade_estoque = models.PositiveIntegerField(default=0, verbose_name='Quantidade em Estoque')
    ativo = models.BooleanField(default=True, verbose_name='Produto Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Venda(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    funcionario = models.ForeignKey('Funcionario', on_delete=models.SET_NULL, null=True, blank=True)
    data_hora = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f'Venda #{self.id} - {self.data_hora.strftime("%d/%m/%Y %H:%M")}'

    def atualizar_total(self):
        total = sum(item.subtotal() for item in self.itens.all())
        self.total = total
        self.save()


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'


class Pagamento(models.Model):
    venda = models.ForeignKey(Venda, related_name='pagamentos', on_delete=models.CASCADE)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('dinheiro', 'Dinheiro'),
            ('cartao', 'Cartão'),
            ('pix', 'PIX'),
            ('transferencia', 'Transferência Bancária'),
        ],
        default='dinheiro'
    )
    confirmado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento de R$ {self.valor:.2f} em {self.forma_pagamento}'
