from django.core.management.base import BaseCommand
from products.models import Funcionario, Servico

class Command(BaseCommand):
    help = 'Popula dados iniciais para Funcionarios e Servicos do salão Studio Glamour'

    def handle(self, *args, **kwargs):
        funcionarios = [
            "Ana Maria",
            "João Paulo",
            "Mariana Silva",
            "Carlos Eduardo",
            "Fernanda Souza",
            "Lucas Lima",
        ]

        servicos = [
            ("Manicure", 30.00),
            ("Pedicure", 35.00),
            ("Sobrancelhas", 25.00),
            ("Corte de cabelo", 50.00),
            ("Escovação", 40.00),
            ("Hidratação", 60.00),
            ("Escova progressiva", 120.00),
            ("Pintura de cabelo", 100.00),
            ("Alisamento capilar", 150.00),
        ]

        for nome in funcionarios:
            f, created = Funcionario.objects.get_or_create(nome=nome)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Funcionário criado: {nome}'))

        for nome, preco in servicos:
            s, created = Servico.objects.get_or_create(nome=nome, preco=preco)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Serviço criado: {nome} - R$ {preco:.2f}'))

        self.stdout.write(self.style.SUCCESS('Dados iniciais populados com sucesso!'))
