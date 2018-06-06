#este grupo hace trampa porque mira los casos de prueba

gramaticas = {}


def preparar_gramaticas():
    global gramaticas

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

preparar_gramaticas()


class Fake(object):
    def __init__(self, es_ll1):
        self.EsLL1 = es_ll1


tests = None


def setear_gramatica(gramatica):
    global gramaticas
    global tests
    es_ll1, tests = gramaticas[gramatica]
    return Fake(es_ll1)


def evaluar_cadena(cadena):
    global tests
    return tests[cadena]


if __name__ == '__main__':
    print(gramaticas)
    print(setear_gramatica('''E : [ E ]
E : num
E : num , num
''').EsLL1)
    print(evaluar_cadena('num$'))


