__author__ = ["Daniel F. S. Machado", "Sandro F. de Brito"]
__credits__ = ["LMSC - Laboratório de Modelagem de Sistema Complexo"]
__date__ = "Setembro 2022"
__version__ = "1.0.0"


import collections
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import seaborn as sns


def csv_para_dat():
    '''
    Essa função encontra os arquivos *.csv no diretório corrente. Extrai as
    respostas dos estudantes e adiciona em um novo arquivo *.dat.
    '''
    arquivos = glob('*.csv')

    #Vamos tratar o/os arquivos *.csv.
    lixo = slice(0, 29)
    regiao_adm = slice(31, 41)
    virgula1 = slice(29, 30)
    virgula2 = slice(42, 43)
    inter = 3

    for arquivo in arquivos:
        with open(arquivo, encoding="utf8") as file:
            lista_arq = file.readlines()[1:]

        respostas = []
        for info in lista_arq:
            nome_arq = ''.join(info[regiao_adm].split()) + '.dat'
            comprimento = len(info[lixo]) + len(info[regiao_adm]) + len(info[virgula1]) + len(info[virgula2]) + inter
            resposta = info[comprimento:]
            resposta = resposta[0:-2]
            respostas.append(resposta)
        with open(nome_arq, 'w') as f:
            for resposta in respostas:
                print(resposta, end='\n', file=f)


def texto():
    '''
    Essa função lê arquivos *.dat com as respostas dos estudantes e retorna
    uma string com as sem as palavras que estão armazenadas no arquivo
    stopwords.txt.

    Observação
    ----------

    Caso queira retirar palavras que são muito comuns e foram digitadas pelos
    estudantes você deve atualizar o arquivo stopwords.txt. O arquivo
    stopwords.txt deve conter apenas uma palavra em cada linha.
    '''
    arq_tratados = glob('*.dat')
    palavrao = ""
    for arquivo in arq_tratados:
        with open(arquivo, encoding="utf8") as file:
            palavra = file.read()
        palavrao = palavrao + palavra

    return palavrao


def conta_palavras(texto):
    '''
    A função conta a quantidade de palavras do arquivo de entrada. Retornando
    um dicionário cuja chave é a palavra e o valor é o número de vezes que a
    palavra apareceu no texto.
    '''

    stopwords = set(line.strip() for line in open('stopwords.txt'))
    stopwords = stopwords.union(set(['alguém','inovação','um','dois','três']))
    # adicionar ao dicionario caso nao exista. Se existir, aumenta a contagem.
    wordcount = {}
    # Para eliminar duplicados, dividir a pontuacao usando delimitadores.
    novo_texto = texto.lower().split()
    for palavra in novo_texto:
        palavra = palavra.replace(".","")
        palavra = palavra.replace(",","")
        palavra = palavra.replace(":","")
        palavra = palavra.replace("\"","")
        palavra = palavra.replace("!","")
        palavra = palavra.replace("â€œ","")
        palavra = palavra.replace("â€˜","")
        palavra = palavra.replace("*","")
        if palavra not in stopwords:
            if palavra not in wordcount:
                wordcount[palavra] = 1
            else:
                wordcount[palavra] += 1

    return wordcount


def plotando_palavras(cp, np):
    '''
    Parametros de input:
    --------------------
    cp: é um dicionário contendo uma chave formada por palavras e o valor
    sendo o número de vezes que essa palavra apareceu.
    np: é o número palavras que o usuário deseja investigar.

    A função retorna um gráfico de barras com o número de palavras que o
    usuário deseja analisar.
    '''

    conta_palavras = collections.Counter(cp)
    lst = conta_palavras.most_common(np)
    df = pd.DataFrame(lst, columns = ['Palavra', 'Contagem'])
    x = df['Palavra'].values
    y = df['Contagem'].values
    xv = range(len(x))
    #sns.set(style="ticks")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar = ax.bar(xv, y, width=0.6, color='teal', edgecolor='darkslategrey', linewidth=2)
    ax.set_xticks(xv)
    ax.set_xticklabels(x, rotation=30, size=10)
    ax.set_ylabel('Ocorrências', fontsize=16, fontweight='bold')
    for b in bar:
        ax.text(b.get_x()+0.3, b.get_height(),'{:.0f}'.format(b.get_height()),
                ha='center',
                va='bottom',
                fontweight='bold',
                color='teal')
    #plt.savefig('Teste.png',dpi=400,transparent=True)
    plt.show()


if __name__ == '__main__':
        while True:
            try:
                # Escolhe o numero de palavras mais frequentes
                numero_palavras = int(input("Quantas palavras deseja imprimir? "))
                csv_para_dat()
                texto = texto()
                conta_palavras = conta_palavras(texto)
                plotando_palavras(conta_palavras, numero_palavras)

                print(f"\nOK. As {numero_palavras} palavras mais comuns são:\n")
                palavras = collections.Counter(conta_palavras)
                print(f' Palavras\tQuantidade')
                print('-'*40)
                for palavra, quantidade in palavras.most_common(numero_palavras):
                    print(f'  {palavra:10s}    {quantidade:6d}')
                break
            except Exception:
                print('Não existe possibilidade de Plotar esse dado.\n')
                print('Informe um valor Inteiro ao programa.\n')
