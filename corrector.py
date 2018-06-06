import importlib
import os


def preparar_gramaticas():
    gramaticas = {}

    lines = open('casos.test', 'r').readlines()

    lineas_gramatica = []
    es_ll1 = None
    leyendo_gramatica = False
    tests = {}

    for line in lines:
        if line.startswith("#") or line.strip() == '':
            continue

        if line.startswith(">gramatica"):
            if len(lineas_gramatica) > 0:
                g = ''.join(lineas_gramatica)
                gramaticas[g] = (es_ll1, tests)

            lineas_gramatica = []
            tests = {}
            es_ll1 = "True" in line
            leyendo_gramatica = True

        elif line.startswith(">tests"):
            leyendo_gramatica = False

        elif leyendo_gramatica:
            lineas_gramatica.append(line)

        else:
            test, res = line.split('>>')
            res = 'True' in res
            test = test.strip()
            tests[test] = res

    if len(lineas_gramatica) > 0:
        g = ''.join(lineas_gramatica)
        gramaticas[g] = (es_ll1, tests)
    return gramaticas


def testear_grupo(gramaticas, grupo):
    print('=================================================================')
    print('TEST Grupo:', grupo)
    print('=================================================================')
    g = importlib.import_module(grupo)
    for gramatica, resultados in gramaticas.items():
        print('*' * 10, 'Gramatica', '*' * 10)
        print(gramatica)
        es_ll1, tests = resultados
        print('Reconoce bien si es o no LL1:',  \
                                es_ll1 == g.setear_gramatica(gramatica).EsLL1)
        for test, res in tests.items():
            ok = 'ok' if res == g.evaluar_cadena(test) else 'fail'
            print('Probando cadena %s : %s' % (test, ok))
        print('*' * 30)
        print('')
    print('=================================================================')


def buscar_grupos():
    res = []
    for f in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if f.startswith('grupo') and f[-2:] == 'py':
            res.append(f[:-3])
    return res

if __name__ == '__main__':
    grupos = buscar_grupos()
    gramaticas = preparar_gramaticas()
    for grupo in grupos:
        testear_grupo(gramaticas, grupo)
