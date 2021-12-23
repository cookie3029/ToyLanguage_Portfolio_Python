#########################################################################################################
# 에러 정의 파트
#########################################################################################################
BRACKET_ERROR1 = "오른 괄호가 먼저 나왔습니다."
BRACKET_ERROR2 = "왼괄호의 개수가 더 많습니다."

NUM_ERROR1 = "마이너스가 중복 입력되었습니다."
NUM_ERROR2 = "숫자 사이에 '-'가 들어갔습니다."
NUM_ERROR3 = "실수를 입력하셨습니다."
NUM_ERROR4 = "알파벳 혹은 '-' 이외의 기호를 입력하셨습니다."

EXPRERESSION_ERROR = "완전한 수식을 입력하세요"
OPERATOR_ERROR = "UNDEFINED"

#########################################################################################################
# 에러 처리 클래스
#########################################################################################################
class ThatIsFloatError(Exception):
    pass

class UseForbiddenChracters(Exception):
    pass

#########################################################################################################
# 스택 클래스
#########################################################################################################
class Stack:
    def __init__(self):
        self.top = []

    def isEmpty(self):
        return len(self.top) == 0

    def push(self, item):
        self.top.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.top.pop(-1)

    def peek(self):
        return self.top[-1]

    def clear(self):
        self.top = []

#########################################################################################################
# 토큰화 함수
#########################################################################################################
def getTokens(input):
    tokens = []
    stack = Stack()

    for ch in input:
        if ch == '(': 
            tokens.append(ch)
        elif ch == ')' or ch == ' ':
            if not stack.isEmpty():
                tokens.append(''.join(stack.top))
                stack.clear()
            
            if ch == ')':
                tokens.append(ch)
        else: stack.push(ch)

    if not stack.isEmpty(): 
        tokens.append(''.join(stack.top))
    
    return tokens

#########################################################################################################
# 음수 판별 함수
#########################################################################################################
def isNagative(token):
    if token[0] == '-' and token[1:].isdigit(): 
        return True
    return False

#########################################################################################################
# 실수 판별 함수
#########################################################################################################
def isFloat(token):
    try:
        num1,_,num2 = token.partition('.')
        if (isNagative(num1) or num1.isdigit) and num2.isdigit(): 
            return True
    except: 
        pass
    
    return False

#########################################################################################################
# 문법 체크 함수
#########################################################################################################
def checkSyntax(tokens):
    stack = Stack()
    numOpCnt = 0

    for token in tokens:
        if token == '(': 
            stack.push(token)
        elif token == ')':
            if stack.isEmpty(): 
                return BRACKET_ERROR1
            else: stack.pop()
        else:
            if numOpCnt % 2 == 0:    
                try:  
                    if token.isdigit() or isNagative(token): 
                        numOpCnt += 1
                    elif token[0] == '-' and token[1] == '-' and token.lstrip('-').isdigit():
                        return NUM_ERROR1
                    elif token.count('-') >= 1 and not token.lstrip('-').isdigit() : 
                        return NUM_ERROR2 
                    elif isFloat(token):
                        raise ThatIsFloatError
                    else:
                        raise UseForbiddenChracters
                except ThatIsFloatError:
                    return NUM_ERROR3
                except UseForbiddenChracters:
                    return NUM_ERROR4
            else:
                if token == "MINUS": 
                    numOpCnt += 1
                else: 
                    return OPERATOR_ERROR
    
    
    if numOpCnt % 2 == 0: return EXPRERESSION_ERROR
    elif not stack.isEmpty(): return BRACKET_ERROR2
    else: return None
    
#########################################################################################################
# 후위식 변환 함수
#########################################################################################################
def getPostfix(expr):
    stack = Stack()
    output = []

    for term in expr:
        if term == '(': stack.push(term)
        elif term == ')':
            while not stack.isEmpty():
                op = stack.pop()
                
                if op == '(': break
                else: output.append(op)
        elif term == "MINUS":
            if not stack.isEmpty() and stack.peek() != '(': output.append(stack.pop())
            stack.push(term)
        else: 
            output.append(term)

    while not stack.isEmpty(): output.append(stack.pop())
    
    return output

#########################################################################################################
# 계산 수행 함수
#########################################################################################################
def eval(expr):
    stack = Stack()
    for token in expr:
        if token == "MINUS":
            val2 = stack.pop()
            val1 = stack.pop()
            stack.push(val1 - val2)
        else: stack.push(int(token))    
    
    return stack.pop()

#########################################################################################################
# 메뉴 출력 함수
#########################################################################################################
def programInterface():
    print("========================================================")
    print("1. File Load")
    print("2. Interaction Mode")
    print("3. Exit")
    print("========================================================")  


#########################################################################################################
# 파일 로드 함수
#########################################################################################################
def fileLoader(filename):
    try:
        infile = open(filename, "r")
    except FileNotFoundError:
        print("\n파일을 찾을 수가 없습니다.")
        return None
    
    lines = infile.readlines()
    infile.close()

    return lines

#########################################################################################################
# 파일 내용과 결과 출력 함수
#########################################################################################################
def showFileResult(lines):
    lineNum = 0

    print("\n파일 내용은")
    print("--------------------------------------------------------")
    
    for line in lines: 
        lineNum += 1 
        print(lineNum, "행 :", line[:-1])
    
    lineNum = 0

    print("--------------------------------------------------------")
    print("입니다.\n")
    print("출력 결과는")
    print("--------------------------------------------------------")
    
    for line in lines: 
        lineNum += 1    
        print(lineNum, "행 결과 :", operation(line[:-1]))
        
        
    print("--------------------------------------------------------")
    print("입니다.\n")

#########################################################################################################
# 인터렉션 모드 함수
#########################################################################################################
def interactionMode():
    inputStr = input("\n문장을 입력하세요 >> ")
    print("\n결과 :", operation(inputStr))

#########################################################################################################
# 연산작업 수행 함수
#########################################################################################################
def operation(inputStr):
    tokens = getTokens(inputStr)
    syntaxError = checkSyntax(tokens)

    if syntaxError == None:
        expr = getPostfix(tokens)
        result = eval(expr)
        return result
    return syntaxError

#########################################################################################################
# main
#########################################################################################################
if __name__ == "__main__":
    while True:
        programInterface()
        inputNum = int(input("메뉴를 선택 하세요 >> "))

        if inputNum == 1:
            fileName = input("\n파일명을 입력하세요 >> ")
            lines = fileLoader(fileName)
            if lines != None: 
               showFileResult(lines)
        elif inputNum == 2:
            interactionMode()
        elif inputNum == 3:
            break
        else: print("주어진 범위에 맞는 번호를 선택하세요!!")