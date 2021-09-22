# Sistemas_Distribuidos
Benchmark de MongoDB

Antes de prosseguir, verifique o modelo do seu Ubuntu(focal, bionic, etc) e substitua a palavra "focal"(linha 6, coluna 8) pelo seu modelo.

Para começar, instale as dependências com:
chmod +x config.sh && ./config.sh

Depois de instalada as dependências pode-se usar o comando make para compilar.
Ele utiliza o arquivo "Entrada.entry" como fonte de comandos.
Pode-se criar outro arquivo com os comandos ou entrar com eles manualmente em tempo de execução.

Para definir um arquivo com as entradas deve-se ficar atento com a sequência das entradas:\
Linha 1: Número de hosts desejado;\
Linha 2: Tempo(em minutos) desejado para cada comando;\
Linha 3 a N-1: Comandos desejados.\
  Possíveis comandos:\
    insert: insere registros no banco por x minutos;\
    delete: deleta registros no banco por x minutos;\
    update: atualiza registros no banco por x minutos;\
    find: lê registros no banco por x minutos;\
    exit: encerra programa.\
Linha N: exit

Como vemos acima, mas fisando aqui, deve-se encerrar o programa como o comando exit.

Caso dê algum problema e os servidores continuem executando após o encerramento do programa, pode-se usar "make kill" para matá-los.

"make clean" limpa tudo, deixando a pasta somente com os arquivos originais padrão.
