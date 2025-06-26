# --------------IMPORTS--------------
import os  # Importação para funcionar o comando os.system para limpar terminal
import re
import json
from pathlib import Path
# --------------GLOBAIS--------------
ARQUIVO = Path('agenda.json')
Agenda = []
compromissos = []

# --------------FUNÇÕES DE INTERFACE/LAYOUT--------------


def exibir_nome_programa():
    print('闩Ꮆ🝗𝓝ᗪ闩 闩Ꮆ🝗𝓝ᗪ闩爪🝗𝓝〸ㄖ\n')


def exibir_opcoes():
    print('1. Registrar compromisso')
    print('2. Listar compromissos')
    print('3. Editar compromissos')
    print('4. Excluir compromissos')
    print('0. Sair da agenda')


def exibir_subtitulo(texto):
    # Comando para limpar o terminal no windows, para mac/linux usar 'clear'
    os.system('cls')
    linha = '*' * (len(texto) + 4)
    print(linha)
    print(texto)
    print(linha, '\n')


def opcao_invalida():
    print('❌ Opção inválida, escolha uma opção disponível!\n')
    voltar_ao_menu_principal()

# --------------PERSISTÊNCIA--------------


def salvar_agenda():

    try:
        with ARQUIVO.open('w', encoding='utf-8') as f:
            json.dump(compromissos, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f'⚠️ Erro ao salvar arquivo: {e}')


def carregar_agenda():
    # Carrega compromissos se agenda.json existir.
    global compromissos, Agenda
    if ARQUIVO.exists():
        try:
            with ARQUIVO.open(encoding='utf-8') as f:
                compromissos = json.load(f)
            Agenda = [c['nome'] for c in compromissos]  # Matém lista paralela
        except (IOError, json.JSONDecodeError) as e:
            print(f'⚠️ Não foi possível ler {ARQUIVO}: {e}')


# --------------NAVEGAÇÃO NO APP--------------


def voltar_ao_menu_principal():
    input('\n📝 Digite qualquer tecla para retornar ao menu principal')
    main()


def sair_agenda():
    exibir_nome_programa()  # Exibe o Título(nome) do app
    print('🔚 Saindo do app')  # Mensagem informativa de saída do app
    salvar_agenda()  # Garante escrita final antes de sair
    exit()

# --------------UTILITÁRIOS--------------


def ler_horario(prompt='Digite o horário (hh:mm) '):
    """
    Lê do usuário um horário no formato 24 h 'HH:MM'.
    Aceita apenas dígitos e dois pontos. Repete até ser válido.
    """
    padrao = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')
    while True:
        valor = input(prompt).strip()
        if padrao.match(valor):
            return valor
    print('❌ Formato inválido! Digite no formato hh:mm (ex.: 08:30, 17:05).')

# --------------OPERAÇÕES NA AGENDA--------------


def cadastrar_novo_compromisso():
    exibir_subtitulo('Cadastro de novos compromissos')
    nome_do_compromisso = input('Digite o nome do seu compromisso: ')
    horario_do_compromisso = ler_horario()

    Agenda.append(nome_do_compromisso)
    compromissos.append({'nome': nome_do_compromisso,
                        'horario': horario_do_compromisso})
    salvar_agenda()
    print(
        f'💾✅ O compromisso {nome_do_compromisso} foi registrado com sucesso na agenda!')
    voltar_ao_menu_principal()


def listar_compromissos(mostrar_subtitulo=True):
    if mostrar_subtitulo:
        exibir_subtitulo('Listando compromissos')
    if not compromissos:
        print('📭 Nenhum compromisso cadastrado')
    else:
        print(
            f"{'ID'.ljust(3)} | {'nome do compromisso'.ljust(22)} | {'Horário'.ljust(20)}")
        print('-' * 52)
        for idx, c in enumerate(compromissos, 1):
            print(
                f"{str(idx).ljust(3)} | {c['nome'].ljust(22)} | {c['horario'].ljust(20)}")
    if mostrar_subtitulo:
        voltar_ao_menu_principal()


def selecionar_id():
    listar_compromissos(mostrar_subtitulo=False)
    try:
        escolha = int(input('\nDigite o ID do compromisso: '))
        if 1 <= escolha <= len(compromissos):
            return escolha - 1
            print('❌ ID inexistente')
    except:
        ValueError
        print('❌ Digite um ID válido.')
    return None


def editar_compromisso():
    exibir_subtitulo('Editar compromisso')
    idx = selecionar_id()
    if idx is not None:
        c = compromissos[idx]
        novo_nome = input(f'Novo nome [{c["nome"]}]: ') or c['nome']
        novo_horario = input(
            f'Novo horário [{c["horario"]}]: ') or c['horario']
        c['nome'], c['horario'] = novo_nome, novo_horario
        salvar_agenda()
        print('✅ Compromisso editado e atualizado com sucesso!')
    voltar_ao_menu_principal()


def deletar_compromisso():
    exibir_subtitulo('Deletar compromisso')
    idx = selecionar_id()
    if idx is not None:
        removido = compromissos.pop(idx)
        Agenda.remove(removido['nome'])
        salvar_agenda()
        print(f'🗑️  {removido["nome"]} compromisso removido com sucesso!')
    voltar_ao_menu_principal()


# --------------MENU PRINCIPAL--------------
def escolher_opcao():
    try:
        opcao_escolhida = int(input('📥 Escolha uma das opções abaixo: '))
        if opcao_escolhida == 1:
            cadastrar_novo_compromisso()
        elif opcao_escolhida == 2:
            listar_compromissos()
        elif opcao_escolhida == 3:
            editar_compromisso()
        elif opcao_escolhida == 4:
            deletar_compromisso()
        elif opcao_escolhida == 0:
            sair_agenda()
        else:
            opcao_invalida()
    except ValueError:  # Apenas erros de conversão
        opcao_invalida()


# --------------FLUXO PRINCIPAL--------------
def main():
    os.system('cls')
    exibir_nome_programa()
    exibir_opcoes()
    escolher_opcao()


# --------------PONTO DE ENTRADA DO PROGRAMA--------------
if __name__ == '__main__':
    carregar_agenda()
    main()
