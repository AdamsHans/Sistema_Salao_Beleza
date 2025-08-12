from django.contrib import admin
from django.http import HttpResponse
from .models import Cliente, Funcionario, Servico, Agendamento, Financeiro
from django import forms

# Form personalizado para usar checkbox múltipla para Serviços no Agendamento
class AgendamentoAdminForm(forms.ModelForm):
    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.filter(ativo=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Serviços'
    )

    class Meta:
        model = Agendamento
        fields = '__all__'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome',)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_com_telefone', 'ativo', 'criado_em', 'atualizado_em')
    search_fields = ('nome', 'telefone')
    list_filter = ('ativo',)
    ordering = ('nome',)

    def nome_com_telefone(self, obj):
        return f"{obj.nome} ({obj.telefone})"
    nome_com_telefone.short_description = 'Funcionário'


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'ativo', 'criado_em', 'atualizado_em')
    search_fields = ('nome',)
    list_filter = ('ativo',)
    ordering = ('nome',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoAdminForm
    autocomplete_fields = ('cliente',)
    list_display = ('cliente', 'funcionario', 'data_hora', 'status', 'mostrar_servicos', 'criado_em')
    list_filter = ('funcionario', 'cliente', 'status', 'servicos')
    search_fields = ('cliente__nome', 'funcionario__nome')
    ordering = ('-data_hora',)

    def mostrar_servicos(self, obj):
        return ", ".join([s.nome for s in obj.servicos.all()])
    mostrar_servicos.short_description = 'Serviços'


@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mostrar_servicos', 'data_hora', 'funcionario', 'valor_total_servicos')
    list_filter = ('data_hora', 'funcionario')
    search_fields = ('cliente__nome', 'funcionario__nome')
    ordering = ('-data_hora',)

    def mostrar_servicos(self, obj):
        return ", ".join([s.nome for s in obj.servicos.all()])
    mostrar_servicos.short_description = 'Serviços'

    def valor_total_servicos(self, obj):
        return sum(s.preco for s in obj.servicos.all())
    valor_total_servicos.short_description = 'Valor Total (R$)'

    actions = ['mostrar_total_selecionados']

    def mostrar_total_selecionados(self, request, queryset):
        total = sum(self.valor_total_servicos(obj) for obj in queryset)
        self.message_user(request, f"Total dos serviços selecionados: R$ {total:.2f}")

    mostrar_total_selecionados.short_description = "Mostrar total dos serviços selecionados"
