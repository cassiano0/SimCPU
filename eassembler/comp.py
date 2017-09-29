#!/usr/bin/env python3
import sys
import easm

ops = easm.mapFile("OPCODES.esym")
regs = easm.mapFile("REGCODES.esym")

# Validação da entrada de linha de comando
if (len(sys.argv) > 1):
    fileToCompile = sys.argv[1]
else:
	fileToCompile = input("Nome do arquivo a ser compilado: ")
	
f = open(fileToCompile,"r")

easm.compileFile(f, ops, regs)
