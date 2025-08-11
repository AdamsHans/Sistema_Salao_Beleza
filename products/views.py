from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Agendamento, Cliente, Funcionario, Servico
from products.models import Produto, Venda, Pagamento, ItemVenda
from .forms import AgendamentoForm
from products.forms import ProdutoForm, VendaForm, PagamentoForm

# --- Agendamentos ---
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all().order_by('-data_hora')
    return render(request, 'app/lista_agendamentos.html', {'agendamentos': agendamentos})

def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_agendamentos')
    else:
        form = AgendamentoForm()
    return render(request, 'app/form_agendamento.html', {'form': form})

# --- Produtos ---
def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'products/lista_produtos.html', {'produtos': produtos})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'products/form_produto.html', {'form': form})

# --- Vendas ---
def criar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save()
            return redirect('detalhe_venda', venda_id=venda.id)
    else:
        form = VendaForm()
    return render(request, 'products/form_venda.html', {'form': form})

def detalhe_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    itens = venda.itens.all()
    return render(request, 'products/detalhe_venda.html', {'venda': venda, 'itens': itens})

# --- Pagamentos ---
def registrar_pagamento(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.venda = venda
            pagamento.save()
            return redirect('detalhe_venda', venda_id=venda.id)
    else:
        form = PagamentoForm()
    return render(request, 'products/form_pagamento.html', {'form': form, 'venda': venda})
