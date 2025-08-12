from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome Completo')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Funcionário'

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

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

# Proxy model para relatórios financeiros no admin
class Financeiro(Agendamento):
    class Meta:
        proxy = True
        verbose_name = 'Financeiro'
        verbose_name_plural = 'Financeiros'
