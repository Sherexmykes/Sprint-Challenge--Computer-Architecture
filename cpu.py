import sys

# Instructions
LDI = 0b10000010
CMP = 0b10100111
JEQ = 0b01010101
PRN = 0b01000111
JNE = 0b01010110
HLT = 0b00000001
JMP = 0b01010100

class CPU:
  

    def __init__(self):
       
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.running = True
        self.FL = 0b00000000
        self.LDI = 0b10000010
        self.CMP = 0b10100111
        self.JEQ =  0b01010101
        self.JNE = 0b01010110
        self.JMP = 0b01010100
        self.PRN =  0b01000111
        self.HLT = 0b00000001
        
        #self.branch_table = {
            #0b10000010: self.LDI,
            #0b10100111: self.CMP,
            #0b01010101: self.JEQ,
            #0b01010110: self.JNE,
            #0b01010100: self.JMP,
            #0b01000111: self.PRN,
            #0b00000001: self.HLT,
           
       # }

    def load(self):

        address = 0
        with open(sys.argv[1]) as files:
            for line in files:
                    split_line = line.split('#')
                    command = split_line[0].strip()
                    if command == '':
                        continue
                    num_command = int(command, 2)

                    self.ram[address] = num_command
                    address += 1

    def alu(self, instruction, register1, register2):
        if instruction == "CMP":
            self.FL &= 0b00000000
            if self.registers[register1] == self.registers[register2]:
                self.FL = 0b00000001
            elif self.registers[register1] < self.registers[register2]:
                self.FL = 0b00000100
            elif self.registers[register1] > self.registers[register2]:
                self.FL = 0b00000010
            self.pc += 3

    def hlt(self):
        self.running = False

    def jeq(self, register_number):
        if self.FL & 1 == 1:
            self.pc = self.registers[register_number]
        else:
            self.pc += 2

    def jmp(self, register_number):
        self.pc = self.registers[register_number]

    def jne(self, register_number):
        if self.FL & 1 == 0:
            self.pc = self.registers[register_number]
        else:
            self.pc += 2

    def ldi(self, register_number, value):
        self.registers[register_number] = value
        self.pc += 3

    def prn(self, register_number):
        print(self.registers[register_number])
        self.pc += 2

    def load(self):
        if len(sys.argv) < 2:
            print("Please pass in a second file name: python3 ls8.py second_filename.py")
            sys.exit()
        file_name = sys.argv[1]
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def run(self):
        self.load()
        while self.running:
            instruction = self.ram[self.pc]

            if instruction == CMP:
                register1 = self.ram[self.pc + 1]
                register2 = self.ram[self.pc + 2]
                self.alu("CMP", register1, register2)

            elif instruction == HLT:
                self.hlt()

            elif instruction == JEQ:
                register_number = self.ram[self.pc + 1]
                self.jeq(register_number)

            elif instruction == JMP:
                register_number = self.ram[self.pc + 1]
                self.jmp(register_number)

            elif instruction == JNE:
                register_number = self.ram[self.pc + 1]
                self.jne(register_number)

            elif instruction == LDI:
                register_number = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.ldi(register_number, value)

            elif instruction == PRN:
                register_number = self.ram[self.pc + 1]
                self.prn(register_number)

            else:
                print(f"Instruction number {self.pc} not recognized!")
                self.pc += 1