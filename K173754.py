

import numpy as np
import pandas as pd
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import pickle



ps = PorterStemmer()
StopWords=open("D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Stopword-List.txt")
StopWords=StopWords.readlines()
Results=open("D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Querry List.txt")
Results=Results.readlines()





def QuerryAndOperation(TermL,TermR):
    
    if isinstance(TermL,list)==False:
        TermL=ps.stem(TermL)
        Left=SortedDictionary[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=ps.stem(TermR)
        Right=SortedDictionary[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    for i in LeftDocumentId:
        for j in RightDocumentId:
            if i==j:
                Ans.append(i)
    return Ans
    
    
def QuerryOrOperation(TermL,TermR):
    
    if isinstance(TermL,list)==False:
        TermL=ps.stem(TermL)
        Left=SortedDictionary[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=ps.stem(TermR)
        Right=SortedDictionary[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    AnsSet=set() #For Unique Values
    
    for i in LeftDocumentId:
        AnsSet.add(i)
    for j in RightDocumentId:
        AnsSet.add(j)
        
    for ans in AnsSet:
        Ans.append(ans)
    return Ans

def GeneratingStopWordsList(File):
    StopWordList=[]
    for word in StopWords:
        word=re.split("\\n",word)
        if word[0]!="":
            StopWordList.append(word[0].replace(" ",""))
    return StopWordList

def GenerateTokensBySpace(File):
    Tokens=[]
    for Word in File:
        Token=""
        for Character in Word:
            if Character!=" ":
                Token+=Character
            else:
                Tokens.append(Token)
                Token=""
    return Tokens

def RemovingDots(Tokens):
    Result=[]
    for Token in Tokens:
        if Token.count(".")>=2: #For Initials like U.S.A
            Result.append(Token.replace(".",""))
        else:
            SplitByDot=re.split("\.",Token) # For Words Like Thousands.So
            for Word in SplitByDot:
                if Word!="":
                    Result.append(Word)
    return Result
def RemovingContractions(Tokens):
    Result=[]
    for Token in Tokens:
        Word=Token.replace("?","").replace(":","").replace(",","").replace('"',"")
        Word=re.split(r"n't",Word)
        if len(Word)>1:
            Word[1]="not"
        if len(Word)<2:
            Word=re.split(r"'s",Word[0])
            if len(Word)>1:
                Word[1]="is"
        if len(Word)<2:
            Word=re.split(r"'re",Word[0])
            if len(Word)>1:
                Word[1]="are"
        if len(Word)<2:
            Word=re.split(r"'m",Word[0])
            if len(Word)>1:
                Word[1]="am"
        if len(Word)<2:
            Word=re.split(r"'ll",Word[0])
            if len(Word)>1:
                Word[1]="will"
        if len(Word)<2:
            Word=re.split(r"'ve",Word[0])
            if len(Word)>1:
                Word[1]="have"
        if len(Word)<2:
            Word=re.split(r"'d",Word[0])
            if len(Word)>1:
                Word[1]="had"
        for W in Word:
            if W!="":
                Result.append(W)
    return Result

def LOWERCASECONVERTOR(Tokens):
    Result=[]
    for Token in Tokens:
        Result.append(Token.lower())
    return Result

def RemovingBraces(Tokens): #[]
    Result=[]
    for Token in Tokens:
        Words=re.split(r"\[(\w+)\]",Token)
        for Word in Words:
            if Word!="":
                Result.append(Word)
    return Result
def RemovingStopWords(Tokens,StopWordList):
    Result=[]
    for Token in Tokens:
        if Token not in StopWordList:
            Result.append(Token)
    return Result
def RemovingHypens(Tokens):
    Result=[]
    for Token in Tokens:
        Words=re.split(r"\-",Token)
        for Word in Words:
            if Word!="":
                Result.append(Word)
    return Result

def PorterStemming(Tokens):
    Result=[]
    for Token in Tokens:
        Result.append(ps.stem(Token))
    return Result

def GeneratingPostingList():
    
    Dictionary={}
    StopWordDictionary={}
    
    SortedDictionary={}
    SortedDictionaryWithStopWord={}
    
    TokensWithStopWords=[]
    
    for file in range(0,56):
        
        FileName="D:\MY SEMESTER\SEMESTER 6\INFORMATION RETRIEVAL\ASSIGNMENT 1\Trump Speechs\speech_"
        FileName+=str(file)
        FileName+=".txt"
        File=open(FileName)
        Speech=File.readlines()
#         print(FileName)
        Speech=Speech[1:]
        # Filtering Data
        StopWordList=GeneratingStopWordsList(StopWords)
        Tokens=GenerateTokensBySpace(Speech)
        Tokens=RemovingContractions(Tokens)
        Tokens=RemovingDots(Tokens)
        Tokens=LOWERCASECONVERTOR(Tokens)
        Tokens=RemovingBraces(Tokens)
        Tokens=RemovingHypens(Tokens)
        
        TokensWithStopWords=Tokens
        
        #StopWordsTokens
        Tokens=RemovingStopWords(Tokens,StopWordList)
        
        Tokens=PorterStemming(Tokens)
        
        #StopWordsTokens With Porter Stemming
        TokensWithStopWords=PorterStemming(TokensWithStopWords)
    
        #Generate Dictionary
    
    
        for i in range(0,len(Tokens)):
            Dictionary.setdefault(Tokens[i],{})
            Dictionary[Tokens[i]].setdefault(file,[])
            Dictionary[Tokens[i]][file].append(i)
            
            #StopWords Dictionary
            
            StopWordDictionary.setdefault(TokensWithStopWords[i],{})
            StopWordDictionary[TokensWithStopWords[i]].setdefault(file,[])
            StopWordDictionary[TokensWithStopWords[i]][file].append(i)
    
    SortedKeys=sorted(Dictionary)
    
    # Keys Of Dictionary Including Stop Words
    StopWordSortedKeys=sorted(StopWordDictionary)
    
    for key in SortedKeys:
        SortedDictionary.setdefault(key,{})
        for j in Dictionary[key]:
            SortedDictionary[key].setdefault(j,Dictionary[key][j])
            
    for key in StopWordSortedKeys:
        SortedDictionaryWithStopWord.setdefault(key,{})
        for j in StopWordDictionary[key]:
            SortedDictionaryWithStopWord[key].setdefault(j,StopWordDictionary[key][j])
            
    return Dictionary,SortedDictionary,SortedDictionaryWithStopWord

def QuerryNotOperation(Term):
    if isinstance(Term,list)==False:
        Term=ps.stem(Term)
        Left=SortedDictionary[Term]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=Term
    Ans=[]
    for i in range(0,56):
        if i not in LeftDocumentId:
            Ans.append(i)
    return Ans

def ProximityQuerryOperation(TermL,TermR,Factor):
    
    if isinstance(TermL,list)==False:
        TermL=ps.stem(TermL)
        Left=SortedDictionaryWithStopWord[TermL]
        LeftDocumentId=Left.keys()
    else:
        LeftDocumentId=TermL
    
    if isinstance(TermR,list)==False:
        TermR=ps.stem(TermR)
        Right=SortedDictionaryWithStopWord[TermR]
        RightDocumentId=Right.keys()
    else:
        RightDocumentId=TermR
    Ans=[]
    AnsSet=set()
    
    
    for LeftId in LeftDocumentId:
        if LeftId in RightDocumentId:
            PositionsIndexLeft=SortedDictionaryWithStopWord[ps.stem(TermL)][LeftId]
            PositionsIndexRight=SortedDictionaryWithStopWord[ps.stem(TermR)][LeftId]
            for LeftPositionIndex in PositionsIndexLeft:
                if LeftPositionIndex+Factor in PositionsIndexRight:
                    AnsSet.add(LeftId)
    
    for ans in AnsSet:
        Ans.append(ans)
    return Ans

def TermsOfFileAndTheirIndexes(FileName):
    for i in SortedDictionary:
        if FileName in SortedDictionary[i].keys():
            print(i,SortedDictionary[i][FileName])

def Querry(querry):
    
    #Proximity Querry Parsingy
    
    if '/' in querry:
        Factor=""
        ProximityList=[]
        Terms=re.split(r"\W+",querry)
        for i in range(len(Terms)-1,-1,-1):
            if Terms[i].isdigit():
                Factor=int(Terms[i])
            else:
                ProximityList.append(Terms[i])
        for i in range(len(ProximityList)-1,-1,-1):
            if i==1:
                Result=ProximityQuerryOperation(ProximityList[i],ProximityList[i-1],Factor+1)
        return Result
    
    #QuerryParsing
    Terms=re.split(r"\W+",querry)
    
    
    #For Phrasal Querry
    if len(re.split("and|AND|or|OR|NOT|not|/",querry))==1:
        Result=QuerryOrOperation(Terms[0],[])
        return Result
    
    
    if '' in Terms:
        Terms.remove("")
    
    Result=[]
    
    
    
    if len(Terms)==1:
        Result=QuerryOrOperation(Terms[0],[])
        return Result
    
    i=len(Terms)-1
    
    for Term in range(len(Terms)):
        
        if (Terms[i]=="or" or Terms[i]=="OR") and Term==1:
            
            Result=QuerryOrOperation(Terms[i+1],Terms[i-1])
            
            
        elif Term>2 and (Terms[i]=="or" or Terms[i]=="OR"):
            
            Result=QuerryOrOperation(Terms[i-1],Result)
            
        if (Terms[i]=="and" or Terms[i]=="AND") and Term==1:
            
            Result=QuerryAndOperation(Terms[i+1],Terms[i-1])
        
        elif Term>2 and (Terms[i]=="and" or Terms[i]=="AND"):
            
            Result=QuerryAndOperation(Terms[i-1],Result)
            
        if (Terms[i]=="NOT" or Terms[i]=="not") and Term==1:
            
            Result=QuerryNotOperation(Terms[i-1])
        
        elif Term>1 and (Terms[i]=="NOT" or Terms[i]=="not"):
            
            Result=QuerryNotOperation(Result)
            
        i-=1
        
    return Result

def GenerateFile(SortedDictionary,SortedDictionaryWithStopWord,Dictionary):
    with open('data.p', 'wb') as fp:
        pickle.dump(SortedDictionary, fp, protocol=pickle.HIGHEST_PROTOCOL)
    with open('datas.p', 'wb') as fp:
        pickle.dump(SortedDictionaryWithStopWord, fp, protocol=pickle.HIGHEST_PROTOCOL)
    with open('datad.p', 'wb') as fp:
        pickle.dump(Dictionary, fp, protocol=pickle.HIGHEST_PROTOCOL)




try:
    with open('data.p', 'rb') as fp:
        SortedDictionary= pickle.load(fp)
    with open('datas.p', 'rb') as fp:
        SortedDictionaryWithStopWord=pickle.load(fp)
    with open('datad.p', 'rb') as fp:
        Dictionary=pickle.load(fp)
	
		 
except IOError:
    Dictionary,SortedDictionary,SortedDictionaryWithStopWord = GeneratingPostingList()
    GenerateFile(SortedDictionary,SortedDictionaryWithStopWord,Dictionary)




#Dictionary,SortedDictionary,SortedDictionaryWithStopWord = GeneratingPostingList()
def main(inp):
	# Ans=sorted(ProximityQuerryOperation('keep','out',3))
	Ans=Querry(inp)
	print(Ans)
	return(Ans)



if __name__=="__main__": 
    main(sys.argv[1])


	
