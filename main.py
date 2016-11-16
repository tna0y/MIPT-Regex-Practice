__author__ = "Maxim Kochukov"
__project__ = "mRegex"

from enum import Enum

class Vertex:
    #to = {}
    #isEnd = False
    been = False
    vid = 0
    def __init__(self):
        self.to = {}
        self.frm = {}
        self.isEnd = False
        self.vid = Vertex.vid
        Vertex.vid += 1


    def addTo(self,letter,vrtx):
        if not letter in self.to.keys(): # add to self.to
            nto = []
        else:
            nto = self.to[letter]

        if not letter in vrtx.frm.keys(): # add to
            nfrm = []
        else:
            nfrm = vrtx.frm[letter]

        nto.append(vrtx)
        nfrm.append(self)
        self.to[letter] = nto
        vrtx.frm[letter] = nfrm

    def goBackWithLetter(self,let, depth, beento):
        if self.vid in beento:
            if depth == 0:
                return 0
            else:
                return "INF"

        solutions = [depth]
        nbeento = beento[::]
        nbeento.append(self.vid)
        if let in self.frm.keys():
            for v in self.frm[let]:
                solutions.append(v.goBackWithLetter(let, depth+1, nbeento))
        if "@" in self.frm.keys():
            for v in self.frm["@"]:
                solutions.append(v.goBackWithLetter(let, depth, nbeento))
        if "INF" in solutions:
            return "INF"
        return max(solutions)

class AutomatEntry:
    def __init__(self, letter):
        a = Vertex()
        b = Vertex()
        b.isEnd = True
        a.addTo(letter,b)
        self.begin = a
        self.end = [b]

    def concat(self, am):
        for e in self.end:
            e.isEnd = False
            e.addTo("@",am.begin)
        self.end = am.end

    def plus(self,am):
        nbegin = Vertex()
        nbegin.addTo("@",self.begin)
        nbegin.addTo("@",am.begin)
        self.end += am.end
        self.begin = nbegin

    def star(self):
        nBegin = Vertex()
        nBegin.addTo("@",self.begin)
        self.begin = nBegin
        for e in self.end:
            e.isEnd = False
            e.addTo("@",self.begin)
        self.begin.isEnd = True
        self.end = [self.begin]

class Token:

    class TokenType(Enum):
        star = 1
        concat = 2
        plus =  3
        automat = 4

    def __init__(self,let):
        self.type = 0
        self.args = 0
        self.mAutomat = None
        if let == '*':
            self.type = Token.TokenType.star
            self.args = 1
        elif let == '+':
            self.type = Token.TokenType.plus
            self.args = 2
        elif let == '.':
            self.type = Token.TokenType.concat
            self.args = 2
        else:
            self.type = Token.TokenType.automat
            self.mAutomat = AutomatEntry(let)


class mRegex:
    def __init__(self,expression):
        self.rpn = ""
        self.tokens = []
        self.automat = None
        # print("Let's rock!")
        self.rpn = expression
        self.correct = self.prepareRE()
        if not self.correct:
            print("Expression not correct!")
        else:
            self.tokenize()
            self.correct = self.generateAutomat()

    def prepareRE(self):
        self.rpn = self.rpn.replace(" ","")
        self.rpn = self.rpn.replace("1","@")

        for c in list(set(list(self.rpn))):
            if not c in list("abc@*.+"):
                return False
        return True


    def tokenize(self):
        [self.tokens.append(Token(x)) for x in self.rpn]


    def generateAutomat(self):
        tokenStack = []
        for t in self.tokens:
            if t.type == Token.TokenType.automat:
                tokenStack.append(t)
            elif t.type == Token.TokenType.star:
                if len(tokenStack) == 0:
                    return False
                am = tokenStack.pop()
                am.mAutomat.star()
                tokenStack.append(am)
            elif t.type == Token.TokenType.concat:
                if len(tokenStack) < 2:
                    return False
                a2 = tokenStack.pop()
                a1 = tokenStack.pop()
                a1.mAutomat.concat(a2.mAutomat)
                tokenStack.append(a1)
            elif t.type == Token.TokenType.plus:
                if len(tokenStack) < 2:
                    return False
                a2 = tokenStack.pop()
                a1 = tokenStack.pop()
                a1.mAutomat.plus(a2.mAutomat)
                tokenStack.append(a1)
        if len(tokenStack) != 1:
            return False
        self.automat = tokenStack[0].mAutomat
        return True

    def getMaxLen(self,letter):
        if not self.correct:
            print("Expression not correct")
        # print("Testing...")
        solutions = [0]
        for i in self.automat.end:
            solutions.append(i.goBackWithLetter(letter,0,[]))

        if "INF" in solutions:
            return "INF"
        return max(solutions)

# INPUT FORMAT: regex letter
# Ex: aa.*b.*a. a

reg, letter = input().split(" ")
regex = mRegex(reg)
print(regex.getMaxLen(letter))
