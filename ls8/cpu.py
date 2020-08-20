"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000
PUSH = 0b01000101   
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 #program counter
        self.running = True
        
        



    # accept the address to read and return the value stored there.
    def ram_read(self, index):
        # index contains address that is being read or written to
        return self.ram[index]

    #  accept a value to write, and the address to write it to.
    def ram_write(self, index, value):
        # contains date that was read or written or data to write
        self.ram[index] = value
    
    def load(self, filename):
        """Load a program into memory."""
        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                value = line.split("#")[0].strip()
                if value == '':
                    continue
                v = int(value, 2)
                self.ram[address] = v
                address += 1

                
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        print("alu", reg_a, reg_b)
        a = self.reg[reg_a]
        b = self.reg[reg_b]
        print(a, b)
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        
        while self.running:
            ir = self.ram_read(self.pc)
            reg_num = self.ram_read(self.pc + 1)
            value = self.ram_read(self.pc + 2)
            if ir == LDI: #SAVE THE REG and set value of reg to int
                self.reg[reg_num] = value
                self.pc += 3
            elif ir == HLT: #HALT
                self.running = False
            elif ir == PRN: #PRINT REG
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2
            elif ir == MUL:
                self.alu("MUL", reg_num, value)
                self.pc += 3
            elif ir == PUSH:
                self.reg[7] -= 1
                reg_a = self.ram[self.pc+1]
                value = self.reg[reg_a]

                # put it on the stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value

                # increment pc
                self.pc += 2
            elif ir == POP:
                sp = self.reg[7]

                # get register number to put value in
                reg_a = self.ram[self.pc+1]

                # use stack pointer to get the value
                value = self.ram[sp]
                # put the value into a given register
                self.reg[reg_a] = value

                # increment stack pointer
                self.reg[7] += 1
                # increment program counter
                self.pc += 2

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)


