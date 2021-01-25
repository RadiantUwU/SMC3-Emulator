import time
import sys
import math
import threading
guion = 0
#temp
threadlist = []
for i range(65535):threadlist.append('FE')
if guion == 1:
    import pygame
    pygame.init()
    black = (0,0,0)
    display_surface = pygame.display.set_mode((640,480))
    pygame.display.set_caption("SMC3 GUI")
    bg = pygame.image.load("./smc3bg.jpg")
tick = 0
def waituntil(init,cond,times):
    exec(init)
    while not eval(cond):
        time.sleep(times)
class Module:
    def __init__(self,outputs,code,mID,name,hasinitcode,config):
        self.inputs = []
        self.outputs = []
        self.mID = mID
        self.name = name
        self.activeoutputs = []
        for i in range(outputs):
            self.outputs.append(0)
            self.activeoutputs.append(0)
        self.code = code
        self.hasinitcode = hasinitcode
        self.config = config
        if self.hasinitcode:
            exec(self.code[1])
            self.code = self.code[0]
    def emulate(self):
        try:
            exec(self.code)
        except BaseException as e:
            print(terminalcolors.red + "An error has occured")
            print(e)
            print(self.code)
            print(self.mID)
            print(self.name + terminalcolors.endc)
            raise Exception
    def update(self):
        j = 0
        for i in self.outputs:
            self.activeoutputs[j] = i
            j += 1
    def getinp(self,num):
        temp = self.inputs[num]
        return(temp[0].activeoutputs[temp[1]])
class terminalcolors:
    pink = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
class ModuleGroup:
    def __init__(self):
        self.arr = []
    def findmID(self,mID):
        for i in self.arr:
            if i.mID == mID:
                return(i)
        return(None)
    def findName(self,name):
        for i in self.arr:
            if i.name == name:
                return(i)
        return(None)
    def emulate(self):
        for i in range(len(self.arr)):
            self.arr[i].emulate()
    def update(self):
        for i in range(len(self.arr)):
            self.arr[i].update()
    def add(self,m):
        self.arr.append(m)
class Random:
        def __init__(self):
            self.seed = 0
            self.multiplier = 2925921
            self.mod = 2 ** 18
            self.increment = 1125
            self.mm = 0
            self.mom = 0
            self.counter = 0
        def pos(self,pos):
            if pos == 0:
                return(self.seed)
            elif pos > 0:
                if pos == 1:
                    return((self.seed * self.multiplier + self.increment) % self.mod)
                else:
                    current = (self.seed * self.multiplier + self.increment) % self.mod
                    for i in range(pos - 1):
                        current = (current * self.multiplier + self.increment) % self.mod
                    return(current)
            elif pos < 0:
                self.checkif()
                if pos == -1:
                    return(((self.seed - self.increment) * self.modinv) % self.mod)
                else:
                    current = ((self.seed - self.increment) * self.modinv) % self.mod
                    for i in range((pos * -1) - 1):
                        current = ((current - self.increment) * self.modinv) % self.mod
                    return(current)
        def forward(self,amount=1):
            if amount == 1:
                self.seed = (self.seed * self.multiplier + self.increment) % self.mod
                self.counter += amount
                return([self.seed])
            else:
                alist = []
                for i in range(amount):
                    self.seed = (self.seed * self.multiplier + self.increment) % self.mod
                    alist.append(self.seed)
                self.counter += amount
                return(alist)
        def back(self,amount=1):
            self.checkif()
            if amount == 1:
                self.seed = ((self.seed - self.increment) * self.modinv) % self.mod
                self.counter -= amount
                return([self.seed])
            else:
                alist = []
                for i in range(amount):
                    self.seed = ((self.seed - self.increment) * self.modinv) % self.mod
                    alist.append(self.seed)
                self.counter -= amount
                return(alist)
        def modInverse(self,a, m):
            A = a % m 
            for x in range(1, m): 
                if ((A * x) % m == 1): 
                    return(x)
            return(1)
        def checkif(self):
            if ((self.mm != self.multiplier) or (self.mom != self.mod)):
                self.modinv = self.modInverse(self.multiplier,self.mod)
                self.mm = self.multiplier
                self.mom = self.mod
        def counterReset(self):
            self.counter = 0
        def reloadOnCounter(self):
            self.seed = self.pos(self.counter * -1)
            self.counter = 0
class Memory:
    def __init__(self):
        self.memory = []
    def findin(self,adr):
        for i in self.memory:
            if i.addr == adr:
                return(i)
        return(None)
    def setmem(self,adr,num):
        e = self.findin(adr)
        if e == None:
            e = DefaultObject()
            e.adr = adr
            e.num = num
            self.memory.append(e)
        else:e.num = num
    def readmem(self,adr):
        e = self.findin(adr)
        if e == None:return(0)
        else:return(e.num)
class DefaultObject:
    def __init__(self):
        pass
class Shell:
    def __init__(self):
        self.running = False
    def load(self):
        self.running = True
        while self.running:
            try:
                try:
                    exec(input('>>> '))
                except Exception as e:
                    print(e)
            except KeyboardInterrupt:
                print('KeyboardInterrupt')
    def exit(self):
        self.running = False
    def clear(self):
        print('\n' * 50)
class newThread(threading.Thread):
    def __init__(self,Name,execute,threadlist,itself):
        threading.Thread.__init__(self)
        self.name = Name
        self.code = execute
        self.deleted = False
        self.threadlist = threadlist
        for i in range(len(threadlist)):
            if threadlist[i] = 'FE':
                self.pos = i
                break
        self.threadlist[self.pos] = self
        self.itself = itself
    def run(self):
        itself = self.itself
        exec(self.code)
        self.deleted = True
        self.threadlist[self.pos] = 'FE'
#0- andgate (digital)
#1- orgate (digital)
#2- xorgate (digital)
#3- notgate (digital)
#4- constant (can be digital or analog)
#5- print inputs to terminal (can be digital or analog)
#6- memory:
#   pins:
#       input(0): number(analog)
#       input(1): address(analog)
#       input(2): R/W(digital)
#       output(0): number(analog)
#7- input from terminal (digital/analog)
#8- counter:
#   pins:
#       input(0):add/subtract(plus or minus)(analog)
#       input(1):reset(digital)
#       output(0):number(analog)
#9- ReadOnlyMemory:
#   pins:
#       input(0):addr(analog)
#       output(0):number(analog)
#10- Invert:
#   pins:
#       input(0):num
#       output(0):num(* -1)
#
version = '0.2.0.0'
print('Module sim by Radiant, version',version)
modulecode = ['''
temp = 1
for i in range(len(self.inputs)):
    if self.getinp(i) == 0:
        temp = 0
        break
self.outputs[0] = temp''','''
temp = 0
for i in range(len(self.inputs)):
    if self.getinp(i) == 1:
        temp = 1
        break
self.outputs[0] = temp''','''
temp = 0
for i in range(len(self.inputs)):
    temp += self.getinp(i)
return(temp % 2)''','self.outputs[0] = (self.getinp(0) + 1) % 2','if self.outputs[0] != self.const:for i in range(len(self.outputs)):self.outputs[i] = self.const','''
print("Module",self.mID,self.name,"Type sendsignal")
for i in range(len(self.inputs)):
    print(self.getinp(i))
print("End of Transmission")''','''
if not hasattr(self, 'memory'):
    self.memory = Memory()
if self.getinp(2) == 0:
    self.outputs[0] = self.memory.readmem(self.getinp(1))
else:
    self.memory.setmem(self.getinp(1),self.getinp(0))
    self.outputs[0] = self.getinp(0)''','''
print('Module',self.mID,self.name,'is asking for Input to be sent at the next cycle in the circuit, type E to keep current changes(for all pins)')
for i in range(len(self.outputs)):
    try:
        e = int(input('Output pin ' + str(i) + ':'))
        self.outputs[i] = e
    except BaseException as e:
        break
''','''
if not hasattr(self, 'memory'):
    self.memory = 0
self.memory += self.getinp(0)
if self.getinp(1) == 1:
    self.memory = 0
self.outputs[0] = self.memory
''','''
if not hasattr(self, 'memory'):
    self.memory = Memory()
self.outputs[0] = self.memory.readmem(self.getinp(0))
''','self.outputs[0] = self.getinp(0) * -1']
class smc3code:
    def __init__(self,moduleself):
        self.version = '0.0.0.1'
        print('SMC3 sim by Radiant, version',self.version)
        self.moduleself = moduleself
        self.sysconfig = self.moduleself.config[0]
        self.memory = []
        self.intram = []
        self.stackmem = []
        self.registers = []
        self.ewo = ["0","1","self.registers[0] % 2","(self.registers[0] > 127) * 1","(self.registers[0] > self.registers[1]) * 1","(self.registers[0] == self.registers[1]) * 1","","(xorstr(bin(self.registers[0])[2:]) == 0) * 1","","",""]
        self.intramadr = 0
        self.increg = [0,1,3,4,8]
        self.fulfilledcond = 0
        self.pc = 0
        self.online = 0
        self.systemspeed = self.sysconfig[1]
        self.oksyssped = [1,2,4,8,10,20,40]
        self.subroutine = 0
        if not self.systemspeed in self.oksyssped:
            raise ZeroDivisionError
        for i in range(16):self.registers.append(0)
        for i in range(256):self.intram.append(0)
        for i in range(self.sysconfig[2]):self.memory.append(0)
        for i in range(self.sysconfig[0]):self.stackmem.append(0)
        # 0 = ALU A
        # 1 = ALU B
        # 2 = COND REG
        # 3 = high bit addr
        # 4 = low bit addr
        # 5 = expansion addr
        # 6 = user input
        # 7 = user output
        # 8 = stack pointer
        # 9 = lognet address send port
        # 10 = lognet address listen port
        # 11 = alu output
        # 12-15 = nonhooked
        #sys config:
        # 0 = stackmem size (max 256)
        # 1 = system speed (1,2,4,8,10,20,40 hz)
        # 2 = external memory size (max 65535)
    def exec(self):
        global tick
        if self.online == 1 and tick % (40 / self.systemspeed) == 0:
            self.pc %= self.sysconfig[2]
            inst = self.memory[self.pc]
            arg1 = self.memory[(self.pc + 1) % self.sysconfig[2]]
            arg2 = self.memory[(self.pc + 2) % self.sysconfig[2]]
            if inst == 0:
                self.online = 0
                print("System paused")
                self.pc += 1
            elif inst == 1:
                self.online = 0
                print(terminalcolors.yellow + "In " + str(pc) + " ERR action call" + terminalcolors.endc)
                self.pc += 1
            elif inst == 2:
                self.online = 0
                print(terminalcolors.yellow + "In " + str(pc) + " ERR action call" + terminalcolors.endc)
                self.pc += 1
            elif inst == 3:
                self.pc = 0
                self.registers = []
                self.stackmem = []
                self.fulfilledcond = 0
                for i in range(16):self.registers.append(0)
                for i in range(self.sysconfig[0]):self.stackmem.append(0)
                print("System reboot")
            elif inst == 4:
                self.registers[3] = arg1
                self.registers[4] = arg2
                self.pc += 3
            elif inst == 5:
                self.registers[arg1] = self.memory[self.registers[3] * 256 + self.registers[4]]
                self.pc += 2
            elif inst == 6:
                self.memory[self.registers[3] * 256 + self.registers[4]] = self.registers[arg1]
                self.pc += 2
            elif inst == 7:
                self.registers[arg1] = len(self.memory) // 256
                self.registers[arg2] = len(self.memory) % 256
                self.pc += 3
            elif inst == 8:
                self.registers[arg1] = arg2
                self.pc += 3
            elif inst == 9:
                self.registers[arg2] = self.registers[arg1]
                self.pc += 3
            elif inst == 10:
                self.intramadr = self.registers[arg1]
                self.pc += 2
            elif inst == 11:
                self.registers[arg1] = self.intram[self.intramadr]
                self.pc += 2
            elif inst == 12:
                self.intram[self.intramadr] = self.registers[arg1]
                self.pc += 2
            elif inst == 13:
                self.registers[arg1] = (len(self.intram) - 1) % 256
                self.pc += 2
            elif inst == 14:
                if arg1 == 4:
                    self.registers[arg1] += 1
                    if self.registers[4] == 256:
                        self.registers[4] = 0
                        self.registers[3] += 1
                        if self.registers[3] == 256:
                            self.registers[3] = 0
                            if self.registers[2] == 6:_cond = 1
                        else:
                            if self.registers[2] == 6:_cond = 0
                else:
                    self.registers[arg1] += 1
                    if self.registers[arg1] == 256:
                        self.registers[arg1] = 0
                        if self.registers[2] == 6:_cond = 1
                    else:
                        if self.registers[2] == 6:_cond = 0
                self.pc += 2
            elif inst == 15:
                if arg1 == 4:
                    self.registers[arg1] -= 1
                    if self.registers[4] == -1:
                        self.registers[4] = 255
                        self.registers[3] -= 1
                        if self.registers[3] == -1:
                            self.registers[3] = 255
                            if self.registers[2] == 6:_cond = 1
                        else:
                            if self.registers[2] == 6:_cond = 0
                else:
                    self.registers[arg1] -= 1
                    if self.registers[arg1] == -1:
                        self.registers[arg1] = 255
                        if self.registers[2] == 6:_cond = 1
                    else:
                        if self.registers[2] == 6:_cond = 0
                self.pc += 2
            elif inst == 16:
                summed = self.registers[0] + self.registers[1]
                if summed > 255:if self.registers[2] == 6:_cond = 1
                else:if self.registers[2] == 6:_cond = 0
                self.registers[11] = summed % 256
                self.pc += 1
            elif inst == 17:
                summed = self.registers[0] - self.registers[1]
                if summed < 0:if self.registers[2] == 6:_cond = 1
                else:if self.registers[2] == 6:_cond = 0
                self.registers[11] = summed % 256
                self.pc += 1
            elif inst == 18:
                a = bin(self.registers[0])[2:]
                b = bin(self.registers[1])[2:]
                c = '0b'
                while len(a) < 8:
                    a = '0' + a
                while len(b) < 8:
                    b = '0' + b
                for i in range(8):
                    if a[i] == '1' and b[i] == '1':
                        c += '1'
                    else:
                        c += '0'
                self.registers[11] = int(c,2)
                self.pc += 1
            elif inst == 19:
                a = bin(self.registers[0])[2:]
                b = bin(self.registers[1])[2:]
                c = '0b'
                while len(a) < 8:
                    a = '0' + a
                while len(b) < 8:
                    b = '0' + b
                for i in range(8):
                    if a[i] == '1' or b[i] == '1':
                        c += '1'
                    else:
                        c += '0'
                self.registers[11] = int(c,2)
                self.pc += 1
            elif inst == 20:
                a = bin(self.registers[0])[2:]
                b = bin(self.registers[1])[2:]
                c = '0b'
                while len(a) < 8:
                    a = '0' + a
                while len(b) < 8:
                    b = '0' + b
                for i in range(8):
                    if a[i] == '1' or b[i] == '1':
                        c += '1'
                    else:
                        c += '0'
                self.registers[11] = int(c,2)
                self.pc += 1
            elif inst == 21:
                a = bin(self.registers[0])[2:]
                b = bin(self.registers[1])[2:]
                c = '0b'
                while len(a) < 8:
                    a = '0' + a
                while len(b) < 8:
                    b = '0' + b
                for i in range(8):
                    if xor((a[i] == '1'),(b[i] == '1')):
                        c += '1'
                    else:
                        c += '0'
                self.registers[11] = int(c,2)
                self.pc += 1
            elif inst == 22:
                a = bin(self.registers[0])[2:]
                a = a + "0"
                if a[0] == "1":if self.registers[2] == 6:_cond = 1
                else:if self.registers[2] == 6:_cond = 0
                a = '0b' + a[1:]
                self.registers[11] = int(a,2)
                self.pc += 1
            elif inst == 23:
                a = bin(self.registers[0])[2:]
                a = "0" + a
                if a[-1] == "1":if self.registers[2] == 6:_cond = 1
                else:if self.registers[2] == 6:_cond = 0
                a = '0b' + a[0:-1]
                self.registers[11] = int(a,2)
                self.pc += 1
            elif inst == 24:
                self.pc = self.registers[3] * 256 + self.registers[4]
            elif inst == 25:
                if _cond == 1:
                    self.pc = self.registers[3] * 256 + self.registers[4]
                else:
                    self.pc += 1
            elif inst == 26:
                self.subroutine = self.pc + 1
                self.pc = self.registers[3] * 256 + self.registers[4]
            elif inst == 27:
                if _cond == 1:
                    self.subroutine = self.pc + 1
                    self.pc = self.registers[3] * 256 + self.registers[4]
                else:
                    self.pc += 1
            elif inst == 28:
                self.pc = self.subroutine
                self.subroutine = 0
            elif inst == 29:
                self.stackmem[self.registers[8]] = self.registers[arg1]
                self.registers[8] += 1
                self.registers[8] %= len(self.stackmem)
                self.pc += 2
            elif inst == 30:
                self.registers[arg1] = self.stackmem[self.registers[8]]
                self.registers[8] -= 1
                self.registers[8] %= len(self.stackmem)
                self.pc += 2
    def reset(self):
        self.pc = 0
        self.registers = []
        self.stackmem = []
        self.fulfilledcond = 0
        for i in range(16):self.registers.append(0)
        for i in range(self.sysconfig[0]):self.stackmem.append(0)
        print("System reboot")
    def calccond(self):
        _cond = eval(self.registers[2])
def xor(a,b):
    if (not a) and b:
        return(True)
    elif (not b) and a:
        return(True)
    else:
        return(False)
def xorstr(a):
    b = 0
    for i in a:
        b = (a + b) % 2
    return(b)
clocktick = 0
ticksys = newThread("ticksystem","global clocktick\nwhile True:\n  clocktick = 1\n  time.sleep(1 / 40)",threadlist,group)
ticksys.start()
prompt = ""
promptcode = ""
group = ModuleGroup()
smc3 = Module(0,["self.thesmc3.exec()","self.thesmc3 = smc3code(self)"],0,"SMC3",True,[[256,1,65536]])
if guion == 1:
    while True:
        display_surface.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos == (0,0):
                    pass
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
else:
    inmenu = 0
    while True:
        if inmenu == 0:
            try:
                waituntil("global clocktick","clocktick == 1",0.01)
                clocktick = 0
                e = newThread("emulation","global group\nglobal tick\ngroup.emulate()\ngroup.update()\ntick += 1",threadlist,group)
                e.start()
                e.join()
            except KeyboardInterrupt:
                print(terminalcolors.blue + 'Entered menu, emulation paused')
                inmenu = 1
        else:
            choice = input("Select(changeinp,reset,exitmenu,start,stop" + prompt + ")")
            if choice == "changeinp":
                try:
                    smc3.thesmc3.registers[6] = (int(input("Input:")) % 256)
                except:
                    pass
            elif choice == "reset":
                smc3.thesmc3.reset()
            elif choice == "exitmenu":
                inmenu = 0
            elif choice == "start":
                smc3.thesmc3.online = 1
            elif choice == "stop":
                smc3.thesmc3.online = 0
            else:
                exec(promptcode)
