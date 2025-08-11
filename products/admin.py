import csv
from datetime import datetime, time
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Count, Sum
from django import forms
from .models import Cliente, Funcionario, Servico, Agendamento
from .forms import AgendamentoForm  # caso use algum custom, senão pode remover

# Form customizado para o Admin do Agendamento
class AgendamentoAdminForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'servicos': forms.SelectMultiple(attrs={'size': '10'}),  # lista múltipla clássica
            'funcionario': forms.Select(),  # dropdown normal, sem autocomplete
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra só funcionários ativos para aparecerem no dropdown
        self.fields['funcionario'].queryset = Funcionario.objects.filter(ativo=True).order_by('nome')


# Admin Cliente (com busca)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome',)


# Admin Funcionário (sem autocomplete, só lista)
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'criado_em', 'atualizado_em')
    search_fields = ('nome',)
    list_filter = ('ativo',)
    ordering = ('nome',)


# Admin Serviço
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'ativo', 'criado_em', 'atualizado_em')
    search_fields = ('nome',)
    list_filter = ('ativo',)
    ordering = ('nome',)


# Filtro customizado para status do agendamento
class StatusFilter(admin.SimpleListFilter):
    title = 'Status do Agendamento'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('agendado', 'Agendado'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


# Admin Agendamento usando o form customizado e configurando autocomplete só para cliente
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoAdminForm
    autocomplete_fields = ('cliente',)  # Só cliente tem autocomplete e ícones
    list_display = ('cliente', 'funcionario', 'data_hora', 'status', 'mostrar_servicos', 'criado_em')
    list_filter = ('funcionario', 'cliente', StatusFilter, 'servicos')
    search_fields = ('cliente__nome', 'funcionario__nome')
    ordering = ('-data_hora',)

    def mostrar_servicos(self, obj):
        return ", ".join([s.nome for s in obj.servicos.all()])
    mostrar_servicos.short_description = 'Serviços'

    # Exporta agendamentos selecionados para CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="agendamentos.csv"'
        writer = csv.writer(response)
        writer.writerow(['Cliente', 'Funcionário', 'Data e Hora', 'Status', 'Serviços', 'Criado em'])
        for agendamento in queryset:
            servicos = ", ".join([s.nome for s in agendamento.servicos.all()])
            writer.writerow([
                agendamento.cliente.nome,
                agendamento.funcionario.nome,
                agendamento.data_hora.strftime("%d/%m/%Y %H:%M"),
                agendamento.status,
                servicos,
                agendamento.criado_em.strftime("%d/%m/%Y %H:%M"),
            ])
        return response
    export_to_csv.short_description = 'Exportar Selecionados (CSV)'

    # Exporta resumo de serviços concluídos com filtro por período
    def exportar_concluidos_csv(self, request, queryset):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        dados_filtrados = queryset.filter(status='concluido')

        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
                data_inicio_dt = datetime.combine(data_inicio_dt.date(), time.min)
                dados_filtrados = dados_filtrados.filter(data_hora__gte=data_inicio_dt)
            except ValueError:
                pass

        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
                data_fim_dt = datetime.combine(data_fim_dt.date(), time.max)
                dados_filtrados = dados_filtrados.filter(data_hora__lte=data_fim_dt)
            except ValueError:
                pass

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_servicos_concluidos.csv"'
        writer = csv.writer(response)
        writer.writerow(['Funcionário', 'Total Serviços', 'Faturamento Estimado'])

        dados = (
            dados_filtrados
            .values('funcionario__nome')
            .annotate(
                total=Count('id'),
                faturamento=Sum('servicos__preco')
            )
            .order_by('-total')
        )

        for item in dados:
            writer.writerow([
                item['funcionario__nome'],
                item['total'],
                f"R$ {item['faturamento']:.2f}" if item['faturamento'] else "R$ 0,00"
            ])
        return response
    exportar_concluidos_csv.short_description = 'Exportar Concluídos (CSV com Período)'

    actions = [export_to_csv, exportar_concluidos_csv]
