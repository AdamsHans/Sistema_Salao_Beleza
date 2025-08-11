from django import forms
from .models import Agendamento, Servico

class AgendamentoForm(forms.ModelForm):
    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.filter(ativo=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Serviços'
    )

    class Meta:
        model = Agendamento
        fields = ['cliente', 'funcionario', 'data_hora', 'status', 'servicos']
