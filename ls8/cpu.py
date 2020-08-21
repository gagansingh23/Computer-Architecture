"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000
PUSH = 0b01000101   
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 #program counter
        self.running = True
        self.flag = 0b00000000
        self.reg[7] = 255
        self.sp = self.reg[7]
        
        
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
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            value_1 = self.reg[reg_a]
            value_2 = self.reg[reg_b]
            if value_1 > value_2:
                self.flag = 0b00000010 #sets flag to "2"
            elif value_1 == value_2:
                self.flag = 0b00000001 #sets flag to "1"
            elif value_1 < value_2:
                self.flag = 0b00000100
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
        running = True
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            number_of_operands = int(ir) >> 6

            self.pc += (1 + number_of_operands)

            # LDI: "LOAD IMMEDIATE" Set the value of a register to an integer.
            if ir == LDI:
                self.reg[operand_a] = operand_b

            # HLT: "HALT" the CPU.
            elif ir == HLT:
                running = False

            # PRN: "PRINT" numeric value stored in the given register.
            elif ir == PRN:
                print( self.reg[operand_a] )

            # MUL: "MULTIPLY" the values in two registers together and store the result in registerA.
            elif ir == MUL:
                self.reg[operand_a] *= self.reg[operand_b]

            # PUSH: "PUSH" the value in the given register on the stack.
            elif ir == PUSH:
                self.sp = (self.sp % 257) - 1
                self.ram[self.sp] = self.reg[operand_a]

            # POP: "POP" the value from the top of the stack and store it in the PC.
            elif ir == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp % 257) + 1

            # CMP: "COMPARE" the results in memory and change the flag is accordance to the result
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)

            # CALL: we "CALL" the location of the register in memory so we can jump to in the subroutine
            elif ir == CALL:
                address = self.reg[operand_a]
                return_address = self.pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]
                self.ram[sp] = return_address
                self.pc = address

            # RET: "RETURN" the procedure from the value from the top of the stack and store it in the PC.
            elif ir == RET:
                self.pc = self.ram_read(self.reg[7])
                self.reg[7] += 1

            # JMP: ALWAYS "JUMP" to the address stored in the given register
            elif ir == JMP:
                address = self.reg[operand_a]
                self.pc = address

            # JEQ: "JUMP IF EQUAL" If the flag result is == 0 then jump to the address stored in the given register
            elif ir == JEQ:
                if self.flag == 0b00000001:
                    address = self.reg[operand_a]
                    self.pc = address

            # JNE: "JUMP IF NOT EQUAL" if flag DOESN"T != 0 then jump to the address stored in the given register.
            elif ir == JNE:
                if self.flag & 0b00000001 == 0b00000000:
                    address = self.reg[operand_a]
                    self.pc = address
        