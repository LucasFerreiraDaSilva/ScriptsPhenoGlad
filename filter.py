import argparse
import csv
import os

parser = argparse.ArgumentParser(description = "Script para busca de valores de simulação")
a = v = None
parser.add_argument('-a', action='store', dest=a, required=True, help='Ano inicial das simulações')
parser.add_argument('-v', action='store', dest=v, required=True, help='valor a ser buscado')

arg = parser.parse_args()

val = int(arg.v)
simulationYear = int(arg.a)

# Verifica se existe as rodadas
if os.path.exists("resultados"):
    resultsDir = [d for d in os.listdir("resultados") if os.path.isdir(os.path.join("resultados", d))]
    os.makedirs("busca", exist_ok=True)

    for directory in resultsDir:
        # Leitura do arquivo
        simulationYear = int(arg.a)
        years = []
        with open("resultados/"+ directory +"/files/filtered.txt") as filtered:
            for row in csv.reader(filtered, dialect="excel-tab"):
                years.append(row)

        results = []
        for year in years[2:]:
            # Separa simulacao e dano
            daysAux = []
            for day in year:
                aux = day.split(';')
                if aux[0].isdigit():
                    aux[0] = int(aux[0])
                daysAux.append(aux)

            # Adiciona o dia juliano
            i = 1
            for day in daysAux:
                day.insert(0, i)
                i += 1

            # Remove as simulacoes que resultaram "NONE"
            days = []
            for day in daysAux:
                if day[1] != "NONE":
                    days.append(day)

            # Ordena os valores
            days.sort(key=lambda x: x[1])
            i = 0
            found = []

            # Laco que busca se existe o valor desejado
            previous = None
            while days[i][1] <= val:
                if days[i][1] < val:
                    previous = days[i][1]
                    i += 1
                    continue

                if days[i][1] == val:
                    if len(days[i]) > 2:
                        found.append(str(days[i][0]) + ";" + str(days[i][2]))
                    else:
                        found.append(str(days[i][0]))
                i += 1

            # Se o valor buscado nao foi encontrado utiliza-se o imediatamente menor
            if not found:
                i = 0
                while days[i][1] <= previous:
                    if days[i][1] == previous:
                        if len(days[i]) > 2:
                            found.append(str(days[i][0]) + ";" + str(days[i][2]))
                        else:
                            found.append(str(days[i][0]))
                    i += 1

            found.insert(0, simulationYear)
            results.append(found)
            simulationYear += 1

        # Calculo das medias
        averageResults = []

        for result in results:
            daysAux = []
            average = None

            for day in result[1:]:
                aux = day.split(';')
                daysAux.append(int(aux[0]))

            sum = 0
            count = len(daysAux)

            for day in daysAux:
                sum += day

            average = sum / count
            avg = []
            avg.append(result[0])
            avg.append(format(average, '.3f'))
            averageResults.append(avg)

        # Escrita dos resultados nos arquivos de saida
        os.makedirs("busca/"+ directory, exist_ok=True)

        with open("busca/"+ directory + "/dia_" + str(val) + ".txt", 'w') as f:
            writer = csv.writer(f, dialect="excel-tab")
            for r in results:
                writer.writerow(r)

        with open("busca/"+ directory + "/dia_" + str(val) + "_medias.txt", 'w') as f:
            writer = csv.writer(f, dialect="excel-tab")
            for ar in averageResults:
                writer.writerow(ar)
else:
    print("Pasta de resultados não encontrada!")

print("Processo concluído!")