#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from subprocess import Popen, PIPE, run, TimeoutExpired
import subprocess as sp
from tabulate import tabulate
import time

l_max = lambda n: (n*(n-1))/2

# tamaños de las redes a generar
ns = [5000, 10000]
# algoritmos pathfinder a ejecutar
algs = ["./Pathfinder_src/OriginalPathfinder/pathfinder", "./Pathfinder_src/BinaryPathfinder/binary-pathfinder", 
        "./Pathfinder_src/Fast-Pathfinder/fast-pathfinder", "./Pathfinder_src/MST-Pathfinder/mst-pathfinder_the",
        "./Pathfinder_src/MST-Pathfinder/mst-pathfinder_pract"]

def mean(numbers):
    return [float(sum(numbers)) / max(len(numbers), 1)]

# realizamos las ejecuciones. Todas serán con r=infty y q=n-1
table_row = []
for n in ns:
    tiempos_poda = [n]
    lista_enlaces = []
    lista_densidad = []
    # generamos la red
    # Usage:
    
    with open('prueba'+str(n)+'.txt','a') as out:
        fichero = sp.run(['./RandomNets2014/create-mod',   # ./create-mod
            str(n),                    # <size>
            '1',                       # <symmetry>
            '0',                       # <diagonal-value>
            '0',                       # <weight-type>
            '500',                     # <min>
            '5000',                    # <max>
            '0.5'],                    # <edge-prob>
                         stdout=out)
#        print(fichero.stdout, file=out)

    for a in algs:
        # la podamos midiendo el tiempo que tardamos con un limite de una hora
        try:
            antes = time.time()
            proc = sp.run([a, "prueba"+str(n)+".txt", str(n-1)], timeout=1800, stdout=sp.PIPE)
            despues = time.time()
            tiempos_poda.append("$"+str(despues - antes)+"$")
            print(proc.stdout)
            # contamos el número de enlaces que obtenemos
            enlaces = proc.stdout.split(b'*edges\n')[1].count(b'\n')
            lista_enlaces.append(enlaces)
            # calculamos la densidad de la red
            densidad = enlaces/l_max(n)
            lista_densidad.append(densidad)
        except sp.TimeoutExpired as t:
            tiempos_poda.append("> 1800")

    table_row.append(mean(lista_enlaces) + mean(lista_densidad) + tiempos_poda)

# generamos la tabla 
table = [r for r in table_row]
print(tabulate(table, headers=["$N$","Media L", "Media D", "Original", "Binary", 
    "Fast", "MST (Teorico)", "MST (Práctico)"], tablefmt="latex"))
