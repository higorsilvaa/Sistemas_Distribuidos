<h1> Sistemas_Distribuidos </h1>
<h2> Benchmark de MongoDB </h2>

<p> Antes de prosseguir, verifique o modelo do seu Ubuntu(focal, bionic, etc) e substitua a palavra "focal"(linha 6, coluna 8) pelo seu modelo. </p>

<p>
   Para começar, instale as dependências com: <br />
  <em> chmod +x config.sh && ./config.sh </em>
</p>

<p>
  Depois de instalada as dependências pode-se usar o comando make para compilar. <br />
  Ele utiliza o arquivo "Entrada.entry" como fonte de comandos. <br />
  Pode-se criar outro arquivo com os comandos ou entrar com eles manualmente em tempo de execução.
</p.

<p>
  Para definir um arquivo com as entradas deve-se ficar atento com a sequência das entradas. <br />
  Elas devem ser escritas separadamente, uma em cada linha.
</p>

<ol>
  <li> Número de hosts desejado;</li>
  <li> Tempo(em minutos) desejado para cada comando;</li>
  <li> Apartir dessa linha pode-se entrar com os comandos. <br />
  Possíveis comandos:
    <ul>
      <li> <strong>insert</strong>: insere registros no banco por x minutos;</li>
    <li> <strong>delete</strong>: deleta registros no banco por x minutos;</li>
    <li> <strong>update</strong>: atualiza registros no banco por x minutos;</li>
    <li> <strong>find</strong>: lê registros no banco por x minutos;</li>
    <li> <strong>exit</strong>: encerra programa.</li>
    </ul>
    </li>
 Deve-se encerrar o programa como o comando <strong>exit</strong>.
  </ol>

<p>
  Caso dê algum problema e os servidores continuem executando após o encerramento do programa, pode-se usar: <br />
  <em> make kill </em> <br />
  Isso irá matá-los.
</p>

<p>
  Para limpar tudo, deixando a pasta somente com os arquivos originais padrão, usa-se o comando: <br />
  <em> make clean </em>
</p>
