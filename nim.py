"""
@authors: 
    Matheus Lucas Silva Meirelles Reis - 17.1.8048
    Lucas Horta Monteiro de Castro     - 16.1.8073
"""


"""

Código feito para demonstrar como o algorítmo MinMax se comporta 
utilizando como heurística o algoritmo de corte Alpha-beta para o jogo Nim
"""

import platform
from math import inf as infinity
from os import system
from time import sleep, time


HUMANO = -1
COMP = +1
tabuleiro = []


def avaliacao(estado):

    """
    Função feita para avaliar para avaliacao heuristica do estado.
    params:
        estado -> list: o estado atual do tabuleiro
    return: 
        placar -> int: retorna +1 caso a IA vença, -1 caso o humano vença 
                        e 0 caso ainda não tenha um vencedor 
    """
    if vitoria(estado) and len(estado) % 2 == 1:
        placar = +1
    elif vitoria(estado) and len(estado) % 2 == 0:
        placar = -1
    else:
        placar = 0
    return placar


def vitoria(estado):

    """
    Função para avaliar a condição de vitória
    params: 
        estado -> list: lista com o estado atual do jogo
    return:
        vitoria -> boolean: retorna se o estado é vitorioso ou não
    """
    
    if  all(elemento == 1 or elemento == 2 for elemento in estado):
        vitoria = True
    else:
        vitoria = False
    return vitoria


def desenha_tabuleiro(tabuleiro):

    """
    Um procedimento para desenhar o tabuleiro do jogo
    params: 
        tabuleiro -> list: lista com o tabuleiro atual do jogo
    """
    limpa_console()
    for count, palito in enumerate(tabuleiro):
        print(f'{count}  => {palito * "|"} : numero de palitos => {palito}')


def movimento_valido(posicao_jogada,palitos_retirados):

    validacao_divisivel = (palitos_retirados != tabuleiro[posicao_jogada]/2)
    validacao_maior_zero= (palitos_retirados > 0)
    validacao_menor_len_tabuleiro = (palitos_retirados < tabuleiro[posicao_jogada])                    
    if (validacao_divisivel or tabuleiro[posicao_jogada] == 3) and validacao_maior_zero and validacao_menor_len_tabuleiro:
        return True
    else:
        return False


def movimento_valido_estado(posicao_jogada,palitos_retirados,estado):

    validacao_divisivel = (palitos_retirados != estado[posicao_jogada]/2)
    validacao_maior_zero= (palitos_retirados > 0)
    validacao_menor_len_estado = (palitos_retirados < estado[posicao_jogada])                    
    if (validacao_divisivel ) and validacao_maior_zero and validacao_menor_len_estado:
        palito_atual = estado[posicao_jogada]
        estado.pop(posicao_jogada)
        estado.insert(posicao_jogada, palito_atual - palitos_retirados )
        estado.insert(posicao_jogada + 1, palitos_retirados)
    return estado


def percorrer_estado(estado):

    retorno = []

    for posicao_jogada, palitos in enumerate(estado):
        for palitos_retirados in range(palitos):
            validacao_divisivel = (palitos_retirados != estado[posicao_jogada]/2)
            validacao_maior_zero= (palitos_retirados > 0)
            validacao_menor_len_estado = (palitos_retirados < estado[posicao_jogada]) 
            if (validacao_divisivel or estado[posicao_jogada] == 3) and validacao_maior_zero and validacao_menor_len_estado:
                retorno.append([posicao_jogada, palitos_retirados])
    return retorno


def calcula_profundidade(estado):
    profundidade = 0
    for palitos in estado:
        if palitos > 2:
            profundidade += 1
    return profundidade


def retorna_estado_original(estado, posicao_jogada):
    valor_1 = estado[posicao_jogada]
    valor_2 = estado[posicao_jogada+1]
    estado.pop(posicao_jogada+1)
    estado.pop(posicao_jogada)
    estado.insert(posicao_jogada, (valor_1+valor_2))
    return estado


def minimax(estado, profundidade, alfa, beta, jogador):

    if profundidade == 0 or vitoria(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]
    
    if jogador == COMP:
        melhor = -infinity
        
        possibilidade_jogadas = percorrer_estado(estado)
        estado_primario = tabuleiro
        for jogadas in possibilidade_jogadas:
            posicao_jogada, palitos_retirados = jogadas[0], jogadas[1]
            estado = movimento_valido_estado(posicao_jogada, palitos_retirados, estado_primario)
            profundidade = calcula_profundidade(estado)
            placar = minimax(estado, profundidade, alfa, beta, - jogador )
            melhor = max(melhor, placar[2])
            estado = retorna_estado_original(estado, posicao_jogada)
            alfa = max(alfa, placar[2])
            if beta <= alfa:
                break
        return [posicao_jogada, palitos_retirados, melhor]


    else:
        melhor = +infinity
        
        possibilidade_jogadas = percorrer_estado(estado)
        estado_primario = tabuleiro
        for jogadas in possibilidade_jogadas:
            posicao_jogada, palitos_retirados = jogadas[0], jogadas[1]
            estado = movimento_valido_estado(posicao_jogada, palitos_retirados, estado_primario)
            profundidade = calcula_profundidade(estado)
            placar = minimax(estado, (profundidade -1), alfa, beta, - jogador )
            melhor = min(melhor, placar[2])
            estado = retorna_estado_original(estado, posicao_jogada)
            beta = min(beta, placar[2])
            if beta <= alfa:
                break
        return [posicao_jogada, palitos_retirados, melhor]

def limpa_console():

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')
    pass


def jogada_IA():

    profundidade = calcula_profundidade(tabuleiro)
    if profundidade == 0:
        return
    
    limpa_console()
    print("Vez do Computador!")

    sleep(1)
    desenha_tabuleiro(tabuleiro)
    if profundidade == 1 and len(tabuleiro) == 1:
        posicao_jogada = 0
        for palitos in tabuleiro:
            if palitos > 2:
                posicao_jogada = tabuleiro.index(palitos)
                palitos_retirados = tabuleiro[posicao_jogada] - 1
                break
    else:
        movimento = minimax(tabuleiro, profundidade, -infinity, +infinity,COMP)
        posicao_jogada, palitos_retirados = movimento[0], movimento[1]
        print(f'posição jogada => {posicao_jogada},palitos retirados => {palitos_retirados}')
    if movimento_valido(posicao_jogada, palitos_retirados):
        palito_atual = tabuleiro[posicao_jogada]
        tabuleiro.pop(posicao_jogada)
        tabuleiro.insert(posicao_jogada, palito_atual - palitos_retirados )
        tabuleiro.insert(posicao_jogada, palitos_retirados)


def jogada_humano():
    print("Vez do Humano!")
    sleep(1)
    while(True):
        try:
            limpa_console()
            desenha_tabuleiro(tabuleiro)
            posicao_jogada = int(input('Digite a posição a ser jogada: '))

            if posicao_jogada >= 0 and posicao_jogada < len(tabuleiro):
                palitos_retirados = int(input('Digite a quantidade de palitos a ser retirado: '))
                if movimento_valido(posicao_jogada, palitos_retirados):
                    palito_atual = tabuleiro[posicao_jogada]
                    tabuleiro.pop(posicao_jogada)
                    tabuleiro.insert(posicao_jogada, palito_atual - palitos_retirados )
                    tabuleiro.insert(posicao_jogada + 1, palitos_retirados)
                    break

                else:
                    print('Jogada não permitida!')
                    sleep(2)
                    limpa_console()
            else:
                print('Jogada inválida!')
                sleep(2)
                limpa_console()
        except ValueError:
            print('Entrada deve ser um dígito')
            sleep(2)
            limpa_console()
        except KeyboardInterrupt:
            print('\nJogo encerrado!')
            exit()
        

def main():

    input_token = ''

    while(True):
        try:
            input_token = int(input('Escolha o número de palitos: '))
            BiggerThenTwo = input_token >= 2
            if BiggerThenTwo:
                break
            elif BiggerThenTwo:
                print("O número deve ser maior que dois")
                sleep(2)
                limpa_console()
        except ValueError:
            print("A entrada deve ser um número!")
            sleep(2)
            limpa_console()
        except KeyboardInterrupt:
            print('\nJogo encerrado!')
            exit()
        except:
            print('\nEscolha errada!')
            sleep(2)
            limpa_console()
    
    tabuleiro.append(int(input_token))
    while(vitoria(tabuleiro) is False):
        posicao_jogada = ''
        palitos_retirados = ''
        start = time()
        jogada_IA()
        end = time()
        print(f'Tempo demorado pra IA jogar  => {end - start}')
        sleep(3)
        if(vitoria(tabuleiro)):
            sleep(1)
            limpa_console()
            desenha_tabuleiro(tabuleiro)
            print('IA venceu!')
            break
        jogada_humano() 
        if(vitoria(tabuleiro)):
            sleep(1)
            limpa_console()
            desenha_tabuleiro(tabuleiro)
            print('Humano venceu!')
            break
        
             
if __name__ == '__main__':
    main()

    