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
	return re.sub('\..*', ".run", fileName)
	
def changeIfMov(op, args):
    aux = op
    auxArgs = args

    if (op == "MOV"):
        arg0isReg = re.search('[a-zA-Z]+', args[0])
        arg0isMem = re.search('\[.+\]', args[0])
        arg0isIme = re.search('[0-9]+', args[0])
        arg1isReg = re.search('[a-zA-Z]+', args[1])
        arg1isMem = re.search('\[.+\]', args[1])
        arg1isIme = re.search('[0-9]+', args[1])

        if arg0isMem:
            auxArgs[0] = re.sub('\[|\]', "", args[0])
        if arg1isMem:
            auxArgs[1] = re.sub('\[|\]', "", args[1])

        if (arg0isReg and arg1isReg):
            aux = "MOV_RR"
        elif (arg0isReg and arg1isMem):
            aux = "MOV_RM"
        elif (arg0isMem and arg1isReg):
            aux = "MOV_MR"
        elif (arg0isReg and arg1isIme):
           aux = "MOV_RI"
        elif (arg0isMem and arg1isIme):
            aux = "MOV_MI"

    return {"op": aux, "args": auxArgs}
#Transforma uma linha de código em um dicionário com as instruções
#@return Dictionary: op: string com as operações, args: vetor com os argumentos
def prepareProgLine(line):
    aux = re.sub('(\t|\n|;.*)+', "", line).strip(" ")
    aux = re.sub(', +', ",", aux).split(' ')

    op = aux[0]

    if (len(aux) > 1):
        args = aux[1].split(',')
    else:
        args = []
    
    return changeIfMov(op, args)

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
        #print(instructions)
        if len(instructions["op"]) > 0:
            code = instructionsToMC(instructions, ops, regs)
            compiledFile.write(code)
    return 0


