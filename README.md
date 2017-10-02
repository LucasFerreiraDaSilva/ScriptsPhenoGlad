# Script para realização do zoneamento para a cultura do gladíolo #
Script desenvolvido com a linguagem de programação Python, versão 3, para a realização da automação das diversas rodadas do modelo PhenoGlad necessárias para a coleta dos dados de cada região para realização do zoneamento de Gladíolo.
O presente script foi desenvolvido de modo a se obter um desempenho melhorado com relação aos demais scripts de automação do modelo, pois utiliza técnicas de programação paralela para o melhor aproveitamento dos recursos computacionais da máquina onde o mesmo será executado. Quanto mais "*cores*" de processamento houverem, mais rápido o script será executado.

## Instruções para download do repositório: ##
1. Abrir o Terminal do Linux.

2. Entrar na pasta que se deseja ter o script. Para entrar na pasta "Documentos" basta executar o comando:

`cd Documentos`

3. Para fazer o download do repositório basta executar o comando:

 `git clone https://github.com/LucasFerreiraDaSilva/ScriptsPhenoGlad.git`

4. Para acessar o script basta entrar na pasta do repositório com o comando:

 `cd ScriptZoneamento`

5. Para executar o script basta seguir as instruções abaixo.

## Instruções para execução: ##
1. A pasta "*meteorologicFiles*" deve conter os arquivos meteorológicos de cada região que se deseja incluir no zoneamento (os arquivos meteorológicos devem ter nomes DISTINTOS e sem espaços).
2. Os resultados estão todos na pasta "resultados" (criada automaticamente).
3. Dentro da pasta "*resultados*" estão as pastas contendo os resultados da simulação para todas as regiões dos arquivos meteorológicos, separadas por seus respectivos nomes.
4. Na pasta de cada região encontram-se os dados resultantes das execuções do modelo para o período informado e anos de dados meteorológicos (pasta *"files"*), bem como um arquivo com a contagem dos alertas ocorridos no período simulado (arquivo *"alertas.txt"*)

### Exemplo de execução do script em um terminal Linux: ###
`python3 zoneamento.py -ai 1961 -af 2015 -di 1 -df 365 -t 1 -c 1 -v 7 -r 1 -d 1.0`

A explicação de cada argumento pode ser visualizada na tabela abaixo:

Argumento | Descrição                | Valor do exemplo acima
--------- | ------------------------ | ------------------------
 **-ai**  | Ano inicial da simulação | ano de 1961
 **-af**  | Ano final da simulação   | ano de 2015
 **-di**  | Dia inicial da simulação | dia 1 do ano juliano
 **-df**  | Dia final da simulação   | dia 365 do ano juliano
 **-t**   | Tipo da cultivar | cultivar do tipo 1
 **-c**   | Nome da cultivar | cultivar de nome 1
 **-e**   | Habilitar emergência | desabilitada, pois não foi informada
 **-v**   | Coluna a ser buscada nos arquivos de resultado | será buscado os dados na coluna 7 (DVS)
 **-r**   | Coluna a ser retornada da filtragem dos arquivos de resultado | serão retornados os dados da coluna 1 (ano)
 **-d**   | Valor a ser buscado na coluna informada para a filtragem | será buscado o valor 1.0 na coluna 7 (DVS)

 OBS.: Para habilitar a emergência basta adicionar o argumento **-e** na execução do script, conforme o exemplo abaixo:

 `python3 zoneamento.py -ai 1961 -af 2015 -di 1 -df 365 -t 1 -c 1 -v 7 -r 1 -d 1.0 -e`

# Script para a busca de valores nos resultados das simulações #
Este script ("*filter.py*") faz o trabalho de buscar as ocorrências de determinado valor dentre os resultados das simulações. Caso o valor informado por parâmetro pelo usuário não for encontrado, busca-se o valor imediatamente anterior, como por exemplo, se o usuário informar para a busca o valor 303 para ser encontrado e o mesmo não tiver nenhuma ocorrência no ano da simulação, então será utilizado um valor imediatamente menor que 303 que exista na simulação, como o 302.

O script retorna como saída tanto o arquivo contendo os dias de ocorrência em cada ano do valor buscado, como também um arquivo contendo o valor médio dos dias que foram encontrados o valor buscado.

**IMPORTANTE:** Esse script efetua a busca do valor informado sobre os resultados de simulações anteriores, portanto, caso a pasta "*resultados*" contendo as simulações não for encontrada, o script não funcionará.  

## Instruções para execução: ##

1. Para executar o script basta estar na pasta que o mesmo se encontra;
2. Os resultados da busca estarão todos na pasta "busca", criada automaticamente;
3. O arquivo contendo os anos de simulação e os dias que o valor buscado foi encontrado, bem como o arquivo com as médias das ocorrências, se encontra dentro da pasta "*busca*" na pasta contendo o nome da respectiva localidade a qual o script efetuou a procura;

### Exemplo de execução do script em um terminal Linux: ###
`python3 filter.py -a 1961 -v 303`

A explicação de cada argumento pode ser visualizada na tabela abaixo:

Argumento | Descrição                | Valor do exemplo acima
--------- | ------------------------ | ------------------------
 **-a**  | Ano inicial dos arquivos resultantes das simulações | ano de 1961
 **-v**  | Valor a ser buscado   | busca-se o valor 303
