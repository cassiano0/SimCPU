#!/usr/bin/python
import re
	
#Carregar tabela de instruções e registradores
def mapFile(fileName):
    auxDict = {}
    codesFile = open(fileName, "r")
    counter = 0
    for line in codesFile:
        value = clearCodesLine(line)
        if (len(value) > 0):
            auxDict[clearCodesLine(line)] = counter
            counter = counter + 1
    codesFile.close()
    return auxDict

#Alterar extensão do arquivo para easm
def changeFileExtension(fileName):
	return re.sub('\..*', ".easm", fileName)
	
#Transforma uma linha de código em um dicionário com as instruções
#@return Dictionary: op: string com as operações, args: vetor com os argumentos
def prepareProgLine(line):
    aux = re.sub('(\t|\n|;.*)+', "", line).strip(" ")
    aux = re.sub(', +', ",", aux).split(' ')
    d = {"op": aux[0]}
    if (len(aux) > 1):
        d["args"] = aux[1].split(',')
    else:
        d["args"] = []
    return d

#Remover todas informações que não são relevantes para o mapeamento dos OPCODES e REGCODES
def clearCodesLine(line):
    return re.sub('(\t| |\n|;.*)+',"", line)
#Transformar dicionario em código de máquina
#@return String
def instructionsToMC(instructions, ops, regs):
    op = instructions["op"]
    aux = str(ops[op]) + " "
    for arg in instructions["args"]:
	    aux += str(regs.get(arg,arg)) + " "
    return aux	

#Compilar arquivo utilizando operadores e registradores mapeados
#    @param f: File
#    @param ops: Dictionary
#    @param regs: Dictionary
def compileFile(f, ops, regs):
    compiledFile = open(changeFileExtension(f.name), "w")
	
    for line in f:
        instructions = prepareProgLine(line)
        code = instructionsToMC(instructions, ops, regs)
        compiledFile.write(code)
    return 0


