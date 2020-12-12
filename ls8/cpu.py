"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
ADDI = 0b10001000
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 256
        self.SP = 256
        self.FL = 0b00000000

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            # print("{:08b}".format(instruction))
            address += 1

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        Running = True
        while Running:
          ir = self.ram_read(self.pc)
          operand_a = self.ram_read(self.pc + 1)
          operand_b = self.ram_read(self.pc + 2)
          
          if ir == HLT:
            Running = False
            sys.exit(0)
          elif ir == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
          elif ir == PRN:
            ans = self.reg[operand_a]
            print(ans)
            self.pc += 2
          elif ir == MUL:
            ans = self.reg[operand_a] * self.reg[operand_b]
            self.reg[operand_a] = ans
            self.pc += 3
          elif ir == PUSH:
            self.SP -= 1
            self.ram[self.SP] = self.reg[operand_a]
            self.pc += 2
          elif ir == POP:
            self.reg[operand_a] = self.ram[self.SP]
            self.SP += 1
            self.pc += 2
          elif ir == CALL:
            self.SP -= 1
            self.ram[self.SP] = self.pc + 2
            self.pc = self.reg[operand_a]
          elif ir == RET:
            self.pc = self.ram[self.SP]
            self.SP += 1
          elif ir == ADD:
            self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
            self.pc += 3
          elif ir == CMP:
            op1 = self.reg[operand_a]
            op2 = self.reg[operand_b]
            if op1 > op2:
              self.FL = 0b00000010
              self.pc += 3
            elif op1 < op2:
              self.FL = 0b00000100
              self.pc += 3
            else:
              self.FL = 0b00000001
              self.pc += 3
          elif ir == JMP:
            self.pc = self.reg[operand_a]
          elif ir == JEQ:
            if self.FL == 0b00000001:
              self.pc = self.reg[operand_a]
            else:
              self.pc += 2
          elif ir == JNE:
            if self.FL != 0b00000001:
              self.pc = self.reg[operand_a]
            else:
              self.pc += 2
          elif ir == ADDI:
            self.reg[operand_a] = self.reg[operand_a] + operand_b
            self.pc += 3
          else:
            print('Error', self.pc)
            self.pc += 1



        
    
    def ram_read(self, memory):
      return self.ram[memory]
    
    def ram_write(self, memory, value):
      self.ram[memory] = value
    
    def binaryToDecimal(self, n):
      return int(n,2)
