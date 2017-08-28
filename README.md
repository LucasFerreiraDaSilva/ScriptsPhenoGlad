# Script para realização do zoneamento para a cultura do gladíolo #

## Instruções: ##
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
