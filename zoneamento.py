import multiprocessing as mp
from shutil import copy, move
from subprocess import call
import argparse
import csv
import os
import timeit

parser = argparse.ArgumentParser(description = 'Script para realização do zonemaneto de gladíolo')

ai = af = di = df = np = t = c = e = v = d = r = None

parser.add_argument('-ai', action='store', dest=ai, required=True, help='Ano inicial')
parser.add_argument('-af', action='store', dest=af, required=True, help='Ano final')
parser.add_argument('-di', action='store', dest=di, required=True, help='Dia inicial')
parser.add_argument('-df', action='store', dest=df, required=True, help='Dia final')

parser.add_argument('-t', action='store', dest=t, required=True, help='Tipo da cultivar')
parser.add_argument('-c', action='store', dest=c, required=True, help='Cultivar')
parser.add_argument('-e', action='store_true', dest=e, help='Emergência')

parser.add_argument('-v', action='store', dest=v, required=True, help='Coluna a ser buscada')
parser.add_argument('-r', action='store', dest=r, required=True, help='Coluna de resultado')
parser.add_argument('-d', action='store', dest=d, required=True, help='Dado a ser buscado')

#parser.add_argument('-np', action='store', dest=np, required=True, help='Número de processos')

arg = parser.parse_args()

anoInicial = str(arg.ai)
anoFinal = str(arg.af)
diaInicial = str(arg.di)
diaFinal = str(arg.df)

#n_proc = int(arg.np)
n_proc = int(mp.cpu_count())

cultivarType = str(arg.t)
cultivar = str(arg.c)
emergence = str(arg.e)
print(emergence)
result_header = int(arg.r)#1
value_header = int(arg.v)#7
data = float(arg.d)#1.0

def phenogladAlert(table, data, column):
    # colunas do arquivo
    tmin = 3
    tmax = 4
    dvs = 7

    # Freezing temperature reached: Crop killed by frost = 3
    c = 0
    for l in table[1:]:
        if ((float(l[tmin-1]) < -2.0) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.0)):
            c+=1
        else:
            c=0
    if ((c > 3) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.0)):
        return ";3"

    # Spike dead by frost = 2
    c = 0
    for l in table[1:]:
        if ((float(l[tmin-1]) > -2.0) and (float(l[tmin-1]) < 3.0) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.64)):
            c+=1
        else:
            c=0

    for l in table[1:]:
        if ((float(l[tmin-1]) <= -2.0) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.64)):
            return ";2"

    if ((c > 3) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.64)):
        return ";2"

    # Risk of severe burning of  florets = 1
    c = 0
    for l in table[1:]:
        if((float(l[tmax-1]) >= 34) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.8) and (float(l[dvs-1]) <= 1.05)):
            c+=1
        else:
            c=0
    if ((c >= 3) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.8) and (float(l[dvs-1]) <= 1.05)):
        return ";1"

    c = 0
    for l in table[1:]:
        if((float(l[tmax-1]) >= 34) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 1.05) and (float(l[dvs-1]) <= 2.9)):
            c+=1
        else:
            c=0
    if ((c >= 3) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 1.05) and (float(l[dvs-1]) <= 2.9)):
        return ";1"

    # Crop killed by heat. = 4
    c = 0
    for l in table[1:]:
        if ((float(l[tmax-1]) > 48) and (float(l[column-1]) <= data) and (float(l[dvs-1]) >= 0.0)):
            return ";4"

    return ""

def executeParallelYears(data):
    filespath = os.path.join(data[2], "files")
    valEmerge = str(emergence).upper()

    param = str(cultivarType)+'\n'+str(cultivar)+'\n'+str(valEmerge)+'\n'+str(data[1])+'\n'+str(data[0])+'\n'
    paramFile = os.path.join(filespath, str(data[1])+"param.txt")
    parameters = open(paramFile, 'w')
    parameters.write(param)
    parameters.close
    parameters = open(paramFile, 'rb')

    os.chdir(data[2])

    call("./PhenoGlad", stdin=parameters)

    os.rename(filespath+'/'+str(data[1])+'result.txt', filespath+'/'+format(data[0], '03')+'/'+str(data[1])+'result.txt')
    os.remove(filespath+'/'+str(data[1])+'param.txt')

def executeSimulations(local):
    filespath = os.path.join(local, "files")
    for dia in range(int(diaInicial), int(diaFinal)+1):
        os.makedirs(filespath+"/"+format(dia, '03'), exist_ok=True)

        dataParam = []
        for ano in range(int(anoInicial), int(anoFinal)+1):
            dataParam.append((dia, ano, local))

        pool = mp.Pool(processes=n_proc)
        pool.map(executeParallelYears, dataParam)
        pool.close()
        pool.join()

def filterResults(local):
    directory = os.path.join(local, "files")
    #simulation = True
    #non_silent = True

    table = []
    resultFilter = []

    dayDirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    dayDirs.sort()

    for day in dayDirs:
        dirDay = os.path.join(directory, day)
        yearFiles = os.listdir(dirDay)
        yearFiles.sort()
        resultYear = []
        resultYear.append(str(day))
        resultYear.append(str(int(day)))

        for yearFile in yearFiles:
            filtered = ""
            table = []
            with open(os.path.join(dirDay, yearFile), "r") as f:
                for line in f:
                    table.append(line.split())

            for l in table[1:]:
                if float(l[value_header-1]) >= data:
                    filtered = str(l[result_header-1])
                    break
            if filtered == "":
                filtered = "NONE"

            resultYear.append(filtered + phenogladAlert(table, data, value_header))

        resultFilter.append(resultYear)

    resultFile = [list(x) for x  in zip(*resultFilter)]

    with open(os.path.join(directory, "filtered.txt"), 'w') as f:
        writer = csv.writer(f, dialect="excel-tab")
        for row in resultFile:
            writer.writerow(row)

def countAlerts(locals):
    for local in locals:
        filteredFile = 'resultados/'+str(local)+'/files/filtered.txt'
        years = []
        with open(filteredFile) as filtered:
            for row in csv.reader(filtered, dialect="excel-tab"):
                years.append(row)
        finalCont = {}
        for day in range(365):
            sum_1 = sum_2 = sum_3 = sum_4 = 0
            for year in years:
                if (';' in year[day]):
                    num = int((year[day].split(';'))[1])
                    if (num == 1):
                        sum_1 += 1
                    elif (num == 2):
                        sum_2 += 1
                    elif (num == 3):
                        sum_3 += 1
                    elif (num == 4):
                        sum_4 += 1

            contDay = []
            contDay.append(sum_1)
            contDay.append(sum_2)
            contDay.append(sum_3)
            contDay.append(sum_4)

            finalCont[str(day+1)] = contDay

        with open("resultados/"+str(local)+"/alertas.txt", 'w') as f:
            writer = csv.writer(f, dialect="excel-tab")
            writer.writerow(["Dia", "Alerta 1", "Alerta 2", "Alerta 3", "Alerta 4"])

            for d in range(365):
                finalCont[str(d+1)].insert(0,(d+1))
                writer.writerow(finalCont[str(d+1)])


def runAutomation():
    locals = list(d.strip('.txt') for d in os.listdir('meteorologicFiles'))
    os.makedirs('resultados', exist_ok=True)
    scriptHome = os.getcwd()
    pathLocals = []

    sum_tsimulation = 0.0

    os.chmod('scripts/PhenoGlad', 0o777);

    for local in locals:
        os.makedirs('resultados/'+str(local), exist_ok=True)
        os.makedirs('resultados/'+str(local)+'/files', exist_ok=True)
        copy('meteorologicFiles/'+str(local)+'.txt', 'resultados/'+str(local)+'/files/meteorologicFile.txt')
        filesPath = 'resultados/'+str(local)+'/'
        copy('scripts/PhenoGlad', filesPath)

        absolutPath = os.path.join(os.getcwd(),filesPath)
        pathLocals.append(absolutPath)

        # Execucao das simulacoes do modelo
        t_start = timeit.default_timer()
        print("Executando simulações...")
        executeSimulations(absolutPath)
        os.remove(os.path.join(absolutPath, 'PhenoGlad'))
        t_finish = timeit.default_timer()
        sum_tsimulation += t_finish - t_start

        os.chdir(scriptHome)

    #print("Tempo de execução das simulações: %f" % (sum_tsimulation))

    # Filtragem dos dados
    tfilter_s = timeit.default_timer()
    print("Filtrando dados...")
    poolFilter = mp.Pool(processes=n_proc)
    poolFilter.map(filterResults, pathLocals)
    poolFilter.close()
    poolFilter.join()
    tfilter_f = timeit.default_timer()
    #print("Tempo de execução da filtragem: %f" % (tfilter_f - tfilter_s))

    # Contagem de alertas
    tcount_s = timeit.default_timer()
    print("Contando alertas...")
    countAlerts(locals)
    tcount_f = timeit.default_timer()
    #print("Tempo de execução da contagem: %f" % (tcount_f - tcount_s))

ttotal_s = timeit.default_timer()
runAutomation()
ttotal_f = timeit.default_timer()

print("Processo finalizado!")

print("Tempo total da execução: %f" % (ttotal_f - ttotal_s))
