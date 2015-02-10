"""
    Input of this program is some integer, like 43 or 51 or 523. And the gene po
    ol consists of 0-9 and four basic operator +,-,*,/. Then this program will
    run basic genetic algorithm to generate a solution of which arithmetic resul
    is the input number 
    
"""

import random
import copy

ENCODING = {"0000":"0",
            "0001":"1",    
            "0010":"2",
            "0011":"3",
            "0100":"4",
            "0101":"5",
            "0110":"6",
            "0111":"7",
            "1000":"8",
            "1001":"9",
            "1010":"+",
            "1011":"-",
            "1100":"*",
            "1101":"/",
            "1110":"?",
            "1111":"?"
            }

class Chromosome:
    """
        chromosome class
        
    """
    def __init__(self,bitstring):
        self.bitstringRepresentation = bitstring
        self.hasUsedAllLegalSymbol = True
        
    def parse(self):
        self._setStringRepresentation()
        self._setValue()
        
    def _setValue(self):
        """
            evaluate string representation to get arithemetic value
        
        """
        needNumber = True 
        equation = []
        for i in self.stringRepresentation:
            if(needNumber):
                if(i.isdigit()):
                    number = int(i)
                    equation.append(number)
                    needNumber = False
                else:
                    
                    self.hasUsedAllLegalSymbol = False
                
            elif(i=="?"):
                continue
            else:
                if(i.isdigit()): 
                    equation[-1] = int(str(equation[-1]) + i)
                    needNumber = False
                    continue
                else:
                    equation.append(i)
                    needNumber = True
                 

        #if last element of the equation is an operator,then delete it 
        if(len(equation)%2 == 0 ):
            equation = equation[:-1]

        #evaluate the value from legal arithmetic equation
        if(equation == []):
            self.value = 0

        else:
            self.equation = equation[:]
            leftOperant = equation[0]
            length = len(equation) 
            flag = False
            i=1
            while(i <= length-1):
                if(equation[i]=="*"):
                    leftOperant = leftOperant * equation[i+1]
                elif(equation[i]=="/"):
                    leftOperant = 0 if equation[i+1]== 0 else \
                                  float(leftOperant) / equation[i+1]
                     
                     
                elif(equation[i]=="+"):
                    if(i+1 == length-1):
                        leftOperant = leftOperant + equation[i+1]
                    else:
                        if(equation[i+2]=="*"):
                            equation[i+3] = equation[i+1]*equation[i+3]
                            equation[i+2] = "+"
                        elif(equation[i+2]=="/"):
                            equation[i+3] = 0 if equation[i+3] == 0 else \
                                           float(equation[i+1])/equation[i+3]
                            equation[i+2] = "+"
                        else:
                            leftOperant = leftOperant + equation[i+1]
                                                          
                else:
                     if(i+1==length-1):
                        leftOperant = leftOperant - equation[i+1]
                     else:
                         if(equation[i+2]=="*"):
                             equation[i+3] = equation[i+1]*equation[i+3]
                             equation[i+2] = "-"
                         elif(equation[i+2]=="/"):
                            equation[i+3] = 0 if equation[i+3] ==0 else \
                                            float(equation[i+1])/equation[i+3]
                            equation[i+2] = "-"
                         else:
                            leftOperant = leftOperant - equation[i+1]
                            
                i += 2

            self.value = leftOperant
             
   
    def setFittness(self,target):
        """
            here fittness is the inverse of abs of target minus the value

        """
        self.fittness =  0 if target-self.value ==0 else \
                            1.0/(abs(target-self.value))
        return self.fittness
    
    def _setStringRepresentation(self):
        """
            from bitstring to string consists of 0-9 and four operators

        """  
        bits = self.bitstringRepresentation
        slicedSequence = [ bits[i:i+4] for i in range(0,len(bits),4)]
        string = ""
        for i in slicedSequence:
            string += ENCODING[i]

        self.stringRepresentation = string
        
         
    
class Demo:

    def __init__(self,mutationRate,crossOver,population,max_generation):
        self.MUTATE_RATE = mutationRate
        self.CROSS_OVER = crossOver
        self.POPULATION = population 
        self.MAX_GENERATION = max_generation
        random.seed()
        
    def startEvolve(self,target):
        """
            main function to evolve 

        """
        firstGeneration = self.firstGeneration()
        result  = self.reachTarget(firstGeneration,target)
        g = 0
        while(result[0]==False):
            generation = self.generateNextGeneration(firstGeneration,target)
            result = self.reachTarget(generation,target)
            g +=1
            #if number of generation has larger than self.MAX_GENERATION then,
            #we just restart, which can improve efficiency of finding a solution
            if(g>self.MAX_GENERATION):
                return self.startEvolve(target)
             
          
        self.endEvolve(result[1])

    def firstGeneration(self):
        """
            generate the first generation which contains self.POPULATION chromos
            omos and we assume each chromosome contains nine genes, and of cours
            each gene is a four bit binary string

        """
        size = self.POPULATION
        chromosomes = []
        for i in range(0,size):
            gene = ""
            for i in range(0,9):
                 gene += "".join([str(random.randint(0,1)) for i in range(0,4)])
            chromo = Chromosome(gene)
            chromo.parse()
            chromosomes.append(chromo)

       # test = Chromosome("001101111010100011000110110110001110")
       # test.parse()
       # chromosomes[-1] = test
        return chromosomes

    def reachTarget(self,chromosomes,target):
        """
            test whether a solution has been found
        """
        
        for chromo in chromosomes:
            if(chromo.value == target and chromo.hasUsedAllLegalSymbol):
                return True,chromo
            
        return False,None
    
    def generateNextGeneration(self,generation,target):
        """
            generate next generation and cross over, mutate them

        """
        newGeneration = []
        size = self.POPULATION
        pie = sum([ chromo.setFittness(target) for chromo in generation])
        for i in range(0,size/2):
            offspringOne =  self.generateOffspring(generation,pie)
            offspringTwo =  self.generateOffspring(generation,pie)
            if(random.random() > self.CROSS_OVER):
                offspringOne,offspringTwo = self.crossOver(offspringOne,offspringTwo)
            offspringOne = self.mutate(offspringOne)
            offspringTwo = self.mutate(offspringTwo)

            offspringOne.parse()
            offspringTwo.parse()
            
            newGeneration.append(offspringOne)
            newGeneration.append(offspringTwo)

       
        return newGeneration

    def mutate(self,chromo):
        """
            go through chromosome and decide whether mutate one point with proba
            bility MUTATE_RATE

        """
        bits = list(chromo.bitstringRepresentation)
        for i in range(0,len(bits)):
            if(random.random() <= self.MUTATE_RATE):
                bits[i] = str(int(bits[i])^1)
                
       
        chromo.bitstringRepresentation = "".join(bits)
        
        return chromo
        
        
    def crossOver(self,os1,os2):
        """
            cross over two chromosomes after a random point
            
        """
        bitsOne = os1.bitstringRepresentation
        bitsTwo  = os2.bitstringRepresentation
         
        crossPoint = random.randint(0,len(bitsOne)-2)
        newBitsOne = bitsOne[:crossPoint+1] + bitsTwo[crossPoint+1:] 
        newBitsTwo = bitsTwo[:crossPoint+1] + bitsOne[crossPoint+1:]
 
        
        os1.bitstringRepresentation = newBitsOne
        os2.bitstringRepresentation = newBitsTwo
        
        return os1,os2
    
    def generateOffspring(self,generation,pie):
        """
            generae offspring according to their fittness
            
        """
        randNumber = random.uniform(0,pie)
        fittnessSofar = 0
        for chromo in generation:
            fittnessSofar += chromo.fittness
            if(fittnessSofar >= randNumber):
                return copy.deepcopy(chromo)
        
    def endEvolve(self,answer):
        print answer.stringRepresentation
        print answer.value
        print answer.equation

if __name__ == "__main__":
    Demo(0.0001,0.7,100,1000).startEvolve(43)
