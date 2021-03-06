# -*- coding: utf-8 -*-

import json, struct, argparse

instructions = json.load(open("instructions.json"))

parser = argparse.ArgumentParser(description = "Pokémon Mini ROM disassembler")
parser.add_argument("inp", type = str, help = "Input ROM file")
parser.add_argument("-o", "--out", type = str, help = "Output ASM file (optional, default = filename.asm)")
parser.add_argument("-f", "--flow", type = str, help = "Execution path output file (optional)")
parser.add_argument("-s", "--symbols", type = str, help = "PMAs .sym file path (optional)")
parser.add_argument("-e", "--entrypoints", type = str, help = "Newline-separated additional code entrypoints file (optional)")
parser.add_argument("-d", "--debug", action = "store_true", help = "Display file offset for debugging purposes (optional, default = False)")
parser.add_argument("-b", "--bios", action = "store_true", help = "Change some functionality of the disassembler to properly handle disassembling the BIOS (optional, default = False)")
parser.add_argument("-ne", "--no_default_entrypoints", action = "store_true", help = "Only use entrypoints added with -e (optional, default = False)")
parser.add_argument("-i", "--prompt_ignores", action = "store_true", help = "Prompt JP HL instructions to ignore (optional, default = False)")
parser.add_argument("-of", "--offset", type = lambda x: int(x, 16), help = "Memory offset to use for jumps and loads - handy when disassembling parts of binaries (optional)")

args = parser.parse_args()

rom = bytearray(open(args.inp, "rb").read())

if args.offset:
    rom = bytearray([0] * args.offset) + rom # quick and dirty way to handle offsets
usedArray = [False] * len(rom) # checked to see if an address has already been disassembled

entrypoints = [[ # code entrypoints list - dynamically extended as code paths are found
    [0x2102, [], 0],
    [0x2108, [], 0],
    [0x210E, [], 0],
    [0x2114, [], 0],
    [0x211A, [], 0],
    [0x2120, [], 0],
    [0x2126, [], 0],
    [0x212C, [], 0],
    [0x2132, [], 0],
    [0x2138, [], 0],
    [0x213E, [], 0],
    [0x2144, [], 0],
    [0x214A, [], 0],
    [0x2150, [], 0],
    [0x2156, [], 0],
    [0x215C, [], 0],
    [0x2162, [], 0],
    [0x2168, [], 0],
    [0x216E, [], 0],
    [0x2174, [], 0],
    [0x217A, [], 0],
    [0x2180, [], 0],
    [0x2186, [], 0],
    [0x218C, [], 0],
    [0x2192, [], 0],
    [0x2198, [], 0],
    [0x219E, [], 0],
    ], [
    [0x009A, [], 0],
    [0x00AB, [], 0],
    [0x00AB, [], 0],
    [0x01CF, [], 0],
    [0x01E0, [], 0],
    [0x01F1, [], 0],
    [0x0202, [], 0],
    [0x0213, [], 0],
    [0x0224, [], 0],
    [0x0235, [], 0],
    [0x0246, [], 0],
    [0x025A, [], 0],
    [0x026B, [], 0],
    [0x027C, [], 0],
    [0x028D, [], 0],
    [0x029E, [], 0],
    [0x02AF, [], 0],
    [0x00AB, [], 0],
    [0x00AB, [], 0],
    [0x043E, [], 0],
    [0x02C0, [], 0],
    [0x03BA, [], 0],
    [0x02D1, [], 0],
    [0x02E2, [], 0],
    [0x02F3, [], 0],
    [0x0304, [], 0],
    [0x0315, [], 0],
    [0x0326, [], 0],
    [0x0337, [], 0],
    [0x0348, [], 0],
    [0x035C, [], 0],
    [0x036D, [], 0],
    [0xFFF1, [], 0],
    [0x0713, [], 0],
    [0x077C, [], 0],
    [0x078B, [], 0],
    [0x079D, [], 0],
    [0x07B1, [], 0],
    [0x07E9, [], 0],
    [0x0802, [], 0],
    [0x081B, [], 0],
    [0x0821, [], 0],
    [0x0830, [], 0],
    [0x084E, [], 0],
    [0x0871, [], 0],
    [0x08CB, [], 0],
    [0x08EC, [], 0],
    [0x0904, [], 0],
    [0x0923, [], 0],
    [0x092E, [], 0],
    [0x0949, [], 0],
    [0x0961, [], 0],
    [0x097D, [], 0],
    [0x09E4, [], 0],
    [0x0A4F, [], 0],
    [0x0A76, [], 0],
    [0x0A81, [], 0],
    [0x0AA6, [], 0],
    [0x0ACD, [], 0],
    [0x0AE6, [], 0],
    [0x0AF9, [], 0],
    [0x0B20, [], 0],
    [0x0B2E, [], 0],
    [0x0B8F, [], 0],
    [0x0BA3, [], 0],
    [0x0BB1, [], 0],
    [0x047A, [], 0],
    [0x0493, [], 0],
    [0x04A4, [], 0],
    [0x04C8, [], 0],
    [0x04F5, [], 0],
    [0x0506, [], 0],
    [0x0517, [], 0],
    [0x0529, [], 0],
    [0x053A, [], 0],
    [0x0BBD, [], 0],
    ], [
    ]
][2 if args.no_default_entrypoints else 1 if args.bios else 0]

replacements = [[ # symbols used for every game
    ["loc_0x002102", "reset_vector",],
    ["loc_0x002108", "prc_frame_copy_irq",],
    ["loc_0x00210E", "prc_render_irq",],
    ["loc_0x002114", "timer_2h_underflow_irq",],
    ["loc_0x00211A", "timer_2l_underflow_irq",],
    ["loc_0x002120", "timer_1h_underflow_irq",],
    ["loc_0x002126", "timer_1l_underflow_irq",],
    ["loc_0x00212C", "timer_3h_underflow_irq",],
    ["loc_0x002132", "timer_3_cmp_irq",],
    ["loc_0x002138", "timer_32hz_irq",],
    ["loc_0x00213E", "timer_8hz_irq",],
    ["loc_0x002144", "timer_2hz_irq",],
    ["loc_0x00214A", "timer_1hz_irq",],
    ["loc_0x002150", "ir_rx_irq",],
    ["loc_0x002156", "shake_irq",],
    ["loc_0x00215C", "key_power_irq",],
    ["loc_0x002162", "key_right_irq",],
    ["loc_0x002168", "key_left_irq",],
    ["loc_0x00216E", "key_down_irq",],
    ["loc_0x002174", "key_up_irq",],
    ["loc_0x00217A", "key_c_irq",],
    ["loc_0x002180", "key_b_irq",],
    ["loc_0x002186", "key_a_irq",],
    ["loc_0x00218C", "unknown_irq0",],
    ["loc_0x002192", "unknown_irq1",],
    ["loc_0x002198", "unknown_irq2",],
    ["loc_0x00219E", "cartridge_irq",],
], [ # symbols used for bios
    ["loc_0x00009A", "reset_vector"],
    ["loc_0x0000AB", "unused"],
    ["loc_0x0001CF", "prc_frame_copy_irq"],
    ["loc_0x0001E0", "prc_render_irq"],
    ["loc_0x0001F1", "timer_2h_underflow_irq"],
    ["loc_0x000202", "timer_2l_underflow_irq"],
    ["loc_0x000213", "timer_1h_underflow_irq"],
    ["loc_0x000224", "timer_1l_underflow_irq"],
    ["loc_0x000235", "timer_3h_underflow_irq"],
    ["loc_0x000246", "timer_3_cmp_irq"],
    ["loc_0x00025A", "timer_32hz_irq"],
    ["loc_0x00026B", "timer_8hz_irq"],
    ["loc_0x00027C", "timer_2hz_irq"],
    ["loc_0x00028D", "timer_1hz_irq"],
    ["loc_0x00029E", "ir_rx_irq"],
    ["loc_0x0002AF", "shake_irq"],
    ["loc_0x00043E", "cart_ejected_irq"],
    ["loc_0x0002C0", "cartridge_irq"],
    ["loc_0x0003BA", "key_power_irq"],
    ["loc_0x0002D1", "key_right_irq"],
    ["loc_0x0002E2", "key_left_irq"],
    ["loc_0x0002F3", "key_down_irq"],
    ["loc_0x000304", "key_up_irq"],
    ["loc_0x000315", "key_c_irq"],
    ["loc_0x000326", "key_b_irq"],
    ["loc_0x000337", "key_a_irq"],
    ["loc_0x000348", "unknown_irq0"],
    ["loc_0x00035C", "unknown_irq1"],
    ["loc_0x00036D", "unknown_irq2"],
    ["loc_0x000713", "suspend_system"],
    ["loc_0x00077C", "sleep"],
    ["loc_0x00078B", "sleep_with_display"],
    ["loc_0x00079D", "shutdown"],
    ["loc_0x0007B1", "unknown_eject0"],
    ["loc_0x0007E9", "default_contrast"],
    ["loc_0x000802", "change_contrast"],
    ["loc_0x00081B", "apply_default_contrast"],
    ["loc_0x000821", "get_default_contrast"],
    ["loc_0x000830", "set_temp_contast"],
    ["loc_0x00084E", "lcd_on"],
    ["loc_0x000871", "init_lcd"],
    ["loc_0x0008CB", "lcd_off"],
    ["loc_0x0008EC", "ena_ram_vec"],
    ["loc_0x000904", "dis_ram_vec"],
    ["loc_0x000923", "dis_irq_13"],
    ["loc_0x00092E", "ena_irq_13"],
    ["loc_0x000949", "unknown_eject1"],
    ["loc_0x000961", "unknown_eject2"],
    ["loc_0x00097D", "dev_card0"],
    ["loc_0x0009E4", "dev_card1"],
    ["loc_0x000A4F", "unknown_eject3"],
    ["loc_0x000A76", "dis_cart_eject"],
    ["loc_0x000A81", "unknown_eject4"],
    ["loc_0x000AA6", "inc_cpu_speed"],
    ["loc_0x000ACD", "recover_inc_cpu"],
    ["loc_0x000AE6", "cart_off_update0"],
    ["loc_0x000AF9", "cart_off_update1"],
    ["loc_0x000B20", "cart_detect"],
    ["loc_0x000B2E", "read_structure"],
    ["loc_0x000B8F", "set_prc_rate"],
    ["loc_0x000BA3", "get_prc_rate"],
    ["loc_0x000BB1", "test_cart_type"],
    ["loc_0x00047A", "dev_read_ids"],
    ["loc_0x000493", "dev_reset"],
    ["loc_0x0004A4", "dev_program_byte"],
    ["loc_0x0004C8", "dev_erase_sector"],
    ["loc_0x0004F5", "dev_unlock_page_register"],
    ["loc_0x000506", "dev_sel_bank"],
    ["loc_0x000517", "dev_cmd_c9"],
    ["loc_0x000529", "dev_prepare_readout"],
    ["loc_0x00053A", "dev_sel_game"],
    ["loc_0x000BBD", "ir_pulse"],
    ], [
    ]
][2 if args.no_default_entrypoints else 1 if args.bios else 0]

def hexStr(num, digits): # convert number to hex string with given number of digits, ensuring a leading 0 where required, as per the weird assembly syntax
    value = hex(num).replace("0x", "").upper().zfill(digits)
    if not value[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        if not value.startswith("-"):
            value = "0" + value
        else:
            if not value.lstrip("-")[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                value = "-0" + value.lstrip("-")
    return value

labs = [] # initialise labels array

if args.symbols: # if the user passes a symbols file, parse it and add to the replacements array
    symfile = open(args.symbols).readlines()
    
    syms = []
    lab = []
    repls = []
    for i in symfile:
        if i == "" or i.startswith(";"):
            continue
        if (split := i.split())[0] in ["LOC", "LAB"] and (split[2] != split[2].upper() or split[2].startswith("__")):
            syms.append(split[:])
        if (split := i.split())[0] in ["LAB"] and (split[2] != split[2].upper() or split[2].startswith("__")):
            lab.append(split[:])
        if (split := i.split())[0] in ["REPL"]:
            repls.append(split[:])        
    for i in syms:
        address = int(i[1].replace("$", ""), 16)
        label = i[2].rstrip("\n")
        replacements.append(["loc_0x{}".format(hexStr(address, 6).upper()), label])
        if i[0] == "LOC":
            entrypoints.append([address & 0xFFFF | (0 if address < 0x10000 else 0x8000), [], address >> 15])
    for i in lab:
        address = int(i[1].replace("$", ""), 16)
        label = i[2].rstrip("\n")
        labs.append([address, label])
    for i in repls:
        replacements.append(i[1:])      

if args.entrypoints: # do the same for any additional entrypoints
    entrypointsfile = open(args.entrypoints).readlines()
    
    for i in entrypointsfile:
        entrypoints.append([(address := int(i.rstrip("\n"), 16)) & 0xFFFF | (0 if address < 0x10000 else 0x8000), [], address >> 15])

jphl = []
if args.prompt_ignores: # JP HL instructions are sometimes impossible to disassemble without dynamic code analysis, so this argument disables warnings for a given instance
    ignores = input("Please enter any JP HL ignores in hex, comma-separated:\n")
    try:
        if ignores:
            for i in ignores.split(","):
                jphl.append(int(i, 16))    
    except:
        ig = open(ignores).readlines()
        for i in ig:
            jphl.append(int(i.rstrip("\n"), 16))

warnings = [] # warnings output

errors = [] # errors output

sp_choice = 2

if args.debug:
    sp_choice = 0

STANDARD_PATTERN = ["0x{0}: ", "            ", "\t"][sp_choice] # pattern for regular instructions
LOC_PATTERN = ["loc_0x{0}: ", "loc_0x{0}:\n"][1] # pattern for locs
LAB_PATTERN = ["{1}:\n"][0]
ASCII_PATTERN = [STANDARD_PATTERN + "ASCII \"{1}\""][0] # pattern for strings
ASCIZ_PATTERN = [STANDARD_PATTERN + "ASCIZ \"{1}\""][0] # pattern for null-terminated strings
DB_PATTERN = [STANDARD_PATTERN + "DB {1}h"][0] # pattern for data

SEPARATOR = "\n; ----------------------" # separator after unconditional jumps, returns etc

defsect = ["DEFSECT \".rom{0}\", CODE AT {1}\nSECT \".rom{0}\"" + SEPARATOR, ""][0] # defsect template for games

defsect_bios = "DEFSECT \".bios\", CODE AT 0000H\nSECT \".bios\"" + SEPARATOR # defsect template for BIOS

def be_uint16(num):
    return struct.unpack('>H', bytes([num % 0x100, num // 0x100]))[0]

def be_int16(num):
    return struct.unpack('>h', bytes([num % 0x100, num // 0x100]))[0]

def be_uint8(num):
    return struct.unpack('>B', bytes([num]))[0]

def be_int8(num):
    return struct.unpack('>b', bytes([num]))[0] # unpack bytes as various big endian types

def prepare_format(offset):
    uint8_t, uint16_t, int8_t, int16_t, next_uint8_t = [None] * 5
    if offset < len(rom) - 1:
        uint8_t = hexStr(rom[offset + 1], 2)
        int8_t = hexStr(be_int8(rom[offset + 1]), 2)
        if offset < len(rom) - 2:
            uint16_t = hexStr(be_uint16((rom[offset + 1] << 8) + rom[offset + 2]), 4)
            int16_t = hexStr(be_int16((rom[offset + 1] << 8) + rom[offset + 2]), 4)
            next_uint8_t = hexStr(rom[offset + 2], 2)
    return uint8_t, uint16_t, int8_t, int16_t, next_uint8_t # parse the rom data and prepare arguments for a .format() call

lines = []

for i in range(len(rom)):
    lines.append(STANDARD_PATTERN.format(hexStr(i, 6))) # initialise output array

locs = set(i[0] & 0x7FFF | i[2] << 15 if i[0] & 0x8000 else i[0] for i in entrypoints) # initialise locs array

def getOffset(line, instEnd): # function for retrieving the destination of a jump from the raw disassembled line - for some reason I thought this was the best way to implement this
    num = ""
    for i in list(lines[line])[::-1]:
        if i in [" ", ","]:
            break
        num = i + num # traverse the line from the end going left until a separator is reached
    lineRaw = lines[line][::-1].replace(num[::-1], "", 1)[::-1] # remove the last instance of the number from the line
    lowerBits = (instEnd + int(num.replace("h", ""), 16) - 1) % 0x10000 # convert the number from a string and constrain it
    
    return lowerBits, lineRaw # return the line without the number and the raw program counter value

if args.flow:
    flow = open(args.flow, "w")

def setProgCounterFull(programCounter, cb):
    # program counter is 16 bits but program space is 23 bits - so if bit 8 of the program counter is set, the CB register takes the place of bits 15-22
    if programCounter & 0x8000:
        return (programCounter & 0x7FFF) | (cb << 15)
    return programCounter

def disassemble(context): # function for actually disassembling a code path, given the context (i.e. program counter, return address and CB value)

    programCounter, returnAddrs, cb = context
    
    nb = cb # NB register is initialised with CB
    
    progCounterFull = setProgCounterFull(programCounter, cb)
    
    while True:
        progCounterFull = setProgCounterFull(programCounter, cb)
        # make sure we're actually disassembling the ROM and not the header
        while progCounterFull < len(rom) and progCounterFull >= 0 and not usedArray[progCounterFull] and (args.no_default_entrypoints or progCounterFull not in range(0x21A4, 0x21BE)) and (args.no_default_entrypoints or progCounterFull not in range(0x1000, 0x2100)):
            
            opcode = rom[progCounterFull] # retrieve the opcode from the ROM
            
            curProgCounter = hexStr(progCounterFull, 6) # string representation of program counter used for things™
            
            instr = instructions[opcode] # retrieve the instruction
            if instr is not None: # if it's a valid opcode,
                if (is16 := len(instr)) == 3:
                    instruction = instr # and it's a single-byte instruction, it must be that
                else:
                    opcode16 = rom[progCounterFull + 1] # otherwise, retrieve the second byte of the opcode
                    instr16 = instructions[opcode][opcode16]
                    if instr16 is not None: # and check whether it's valid
                        instruction = instr16
                    else:
                        errors.append("Illegal opcode16 at {}: {} {}".format(curProgCounter, hexStr(opcode, 2), hexStr(opcode16, 2)))
                        break
            else:
                errors.append("Illegal opcode at {}: {}".format(curProgCounter, hexStr(opcode, 2)))
                break
    
            lines[progCounterFull] += instruction[0].format(*prepare_format(progCounterFull if is16 == 3 else progCounterFull + 1))
            # set the output line corresponding to the program counter to the disassembled instruction
            if args.flow:
                flow.write("{}\t{} {}\n".format(lines[progCounterFull], cb, nb))

            usedArray[progCounterFull:progCounterFull + instruction[2]] = [True] * instruction[2] # set the used array
            
            instrEnd = programCounter + instruction[2] # instrEnd points to the start of the next instruction, used for return addresses and suchlike
            
            if instruction[1] in [
                ["CE", "F0"], # CARS LT,rr
                ["CE", "F1"], # CARS LE,rr
                ["CE", "F2"], # CARS GT,rr
                ["CE", "F3"], # CARS GE,rr
                ["CE", "F4"], # CARS V,rr
                ["CE", "F5"], # CARS NV,rr
                ["CE", "F6"], # CARS P,rr
                ["CE", "F7"], # CARS M,rr
                ["CE", "F8"], # CARS F0,rr
                ["CE", "F9"], # CARS F1,rr
                ["CE", "FA"], # CARS F2,rr
                ["CE", "FB"], # CARS F3,rr
                ["CE", "FC"], # CARS NF0,rr
                ["CE", "FD"], # CARS NF1,rr
                ["CE", "FE"], # CARS NF2,rr
                ["CE", "FF"], # CARS NF3,rr
    
                ["E0"], # CARS C,rr
                ["E1"], # CARS NC,rr
                ["E2"], # CARS Z,rr
                ["E3"], # CARS NZ,rr
    
                ["E8"], # CARL C,qqrr
                ["E9"], # CARL NC,qqrr
                ["EA"], # CARL Z,qqrr
                ["EB"], # CARL NZ,qqrr
                
                ["F0"], # CARS rr

                ["F2"], # CARL qqrr
            ]:
                dest, lineRaw = getOffset(progCounterFull, instrEnd)
                # get function location
                returnAddrs.append([instrEnd, cb])
                entrypoints.append([instrEnd, returnAddrs[:], cb])
                # set return address etc
                if nb != None: # if NB register is in a known state,
                    prev = progCounterFull
                    # perform the jump
                    programCounter = dest
                    cb = nb
                    progCounterFull = setProgCounterFull(programCounter, cb)
                    
                    if progCounterFull > 0x2100:
                        lines[prev] = lineRaw + "loc_0x" + hexStr(progCounterFull, 6)
                    else:
                        diff = progCounterFull - prev
                        lines[prev] = lineRaw + hexStr(diff, 4) + "h"
                    
                    locs.add(progCounterFull)
                else:
                    lines[progCounterFull] += " ; WARNING: NB not known, branch not executed"
                    # otherwise error
                    errors.append("ERROR: Branching instruction without NB set at {}".format(curProgCounter))
                    break
            elif instruction[1] in [
                ["CE", "E0"], # JRS LT,rr
                ["CE", "E1"], # JRS LE,rr
                ["CE", "E2"], # JRS GT,rr
                ["CE", "E3"], # JRS GE,rr
                ["CE", "E4"], # JRS V,rr
                ["CE", "E5"], # JRS NV,rr
                ["CE", "E6"], # JRS P,rr
                ["CE", "E7"], # JRS M,rr
                ["CE", "E8"], # JRS F0,rr
                ["CE", "E9"], # JRS F1,rr
                ["CE", "EA"], # JRS F2,rr
                ["CE", "EB"], # JRS F3,rr
                ["CE", "EC"], # JRS NF0,rr
                ["CE", "ED"], # JRS NF1,rr
                ["CE", "EE"], # JRS NF2,rr
                ["CE", "EF"], # JRS NF3,rr
            
                ["E4"], # JRS C,rr
                ["E5"], # JRS NC,rr
                ["E6"], # JRS Z,rr
                ["E7"], # JRS NZ,rr
                
                ["EC"], # JRL C,qqrr
                ["ED"], # JRL NC,qqrr
                ["EE"], # JRL Z,qqrr
                ["EF"], # JRL NZ,qqrr
                
                ["F5"], # DJR NZ,rr
            ]:
                dest, lineRaw = getOffset(progCounterFull, instrEnd)
                # jumps don't return so no return address pushing required
                entrypoints.append([instrEnd, returnAddrs[:], cb])
                    
                if nb != None:
                    prev = progCounterFull
                
                    programCounter = dest
                    cb = nb
                    progCounterFull = setProgCounterFull(programCounter, cb)
                    
                    if progCounterFull > 0x2100:
                        lines[prev] = lineRaw + "loc_0x" + hexStr(progCounterFull, 6)
                    else:
                        diff = progCounterFull - prev
                        lines[prev] = lineRaw + hexStr(diff, 4) + "h"
                    
                    locs.add(progCounterFull)
                else:
                    lines[progCounterFull] += " ; WARNING: NB not known, branch not executed"
                    
                    errors.append("ERROR: Branching instruction without NB set at {}".format(curProgCounter))
                    break
            elif instruction[1] in [
                ["F1"], # JRS rr

                ["F3"], # JRL qqrr
            ]:
                dest, lineRaw = getOffset(progCounterFull, instrEnd)
                # special case for unconditional jump - no entrypoint required after it either
                if nb != None:
                    prev = progCounterFull
                
                    programCounter = dest
                    cb = nb
                    progCounterFull = setProgCounterFull(programCounter, cb)
                    
                    if progCounterFull > 0x2100:
                        lines[prev] = lineRaw + "loc_0x" + hexStr(progCounterFull, 6)
                    else:
                        diff = progCounterFull - prev
                        lines[prev] = lineRaw + hexStr(diff, 4) + "h"

                    lines[prev] += SEPARATOR          
                    # and add a separator for niceness
                    locs.add(progCounterFull)
                else:
                    lines[progCounterFull] += " ; WARNING: NB not known, branch not executed"

                    lines[progCounterFull] += SEPARATOR          
                                        
                    errors.append("ERROR: Branching instruction without NB set at {}".format(curProgCounter))
                    break      
            elif instruction[1] == ["F4"]: # JP HL
                lines[progCounterFull] += SEPARATOR # separator for niceness
                HL = None
                if rom[progCounterFull - 3] == 0xC5:
                    HL = be_uint16((rom[progCounterFull - 2] << 8) + rom[progCounterFull - 1])
                elif rom[progCounterFull - 6] == 0xC5 and rom[progCounterFull - 3:progCounterFull - 1] == bytearray([0xCE, 0xC4]):
                    HL = be_uint16((rom[progCounterFull - 5] << 8) + rom[progCounterFull - 4])
                if HL != None:
                    # JP HL is a massive pain to implement - without tracking HL through execution, we need to parse the bytes before the instruction to retrieve the jump destination
                    if nb != None:
                        
                        programCounter = HL
                        cb = nb
                        progCounterFull = setProgCounterFull(programCounter, cb)
                        locs.add(progCounterFull)
                    else:
                        errors.append("ERROR: Branching instruction without NB set at {}".format(curProgCounter))
                        break                        
                else:
                    if progCounterFull not in jphl:
                        warnings.append("WARNING: JP HL encountered at {}, some code may not be disassembled".format(curProgCounter))
                    break
            elif instruction[1] == ["F8"]: # RET
                lines[progCounterFull] += SEPARATOR # separator for niceness
                if len(returnAddrs) > 0:
                    programCounter, cb = returnAddrs.pop()
                    nb = cb # CB and NB are restored to pre-call values on returning (annoying bug to hunt down)
                else:
                    warnings.append("WARNING: RET without return address at 0x{}".format(curProgCounter))
                    break
            elif instruction[1] == ["F9"]: # RETE
                lines[progCounterFull] += SEPARATOR
                if len(returnAddrs) > 0:
                    programCounter, cb = returnAddrs.pop()
                    nb = cb
                else:
                    break
            elif instruction[1] == ["FA"]: # RETS
                lines[progCounterFull] += SEPARATOR
                if len(returnAddrs) > 0:
                    programCounter, cb = returnAddrs.pop()
                    programCounter += 2
                    nb = cb
                else:
                    warnings.append("WARNING: RETS without return address at 0x{}".format(curProgCounter))
                    break                
            elif instruction[1] == ["FB"]:
                warnings.append("WARNING: CALL [hhll] encountered at {}, some code past 0xFFFF will not be disassembled".format(curProgCounter))
                programCounter = instrEnd
                nb = cb
            elif instruction[1] == ["FD"]:
                lines[progCounterFull] += SEPARATOR                
                warnings.append("WARNING: JP [kk] encountered at {}, some code may not be disassembled".format(curProgCounter))
                break # these two instructions are pretty much impossible to implement without emulating the code, so I just ignore them
            elif instruction[1] == ["CE", "C4"]: # LB NB,#bb
                nb = rom[progCounterFull + instruction[2] - 1]
                programCounter += instruction[2] # I track NB through execution as though I were emulating the program, so I had to immplement the LD NB instruction
            elif instruction[1] == ["CE", "CC"]: # LD NB,A
                nb = None # LD NB,A destroys the tracked value of NB, as it's not possible to know A without emulating the code
                programCounter += instruction[2]
            else: # for all other instructions, just move on to the next byte
                programCounter += instruction[2]
                
            progCounterFull = setProgCounterFull(programCounter, cb)
            
        # if the end of a code path is reached with no return addresses remaining, move onto the next entrypoint
        if len(returnAddrs) == 0:
            break
        # otherwise, move onto the next return address
        programCounter, cb = returnAddrs.pop()
        nb = cb

print("Disassembling {}...".format(args.inp))

entrypoint = 0
while entrypoint < len(entrypoints):
    disassemble(entrypoints[entrypoint])
    entrypoint += 1 # iterate through the entrypoints and disassemble them

print("Formatting output...")

section = 1

dbs = 1

asciz = None

dbmode = 0

lastlab = None

sect = "non-empty string"

for i in range(len(lines)): # formatting and parsing of data and strings is really complicated and hard to understand - do your best
    
    index = hexStr(i, 6)
    if i in [j[0] for j in labs]:
        for j in labs:
            if i == j[0]:
                lines[i] = LAB_PATTERN.format(index, j[1]) + lines[i]
                replacements.append([hexStr(j[0], 4), j[1]])
                dbs = 1
                dbmode = 0
                lastlab = j[1]
                break
    elif i in locs:
        lines[i] = LOC_PATTERN.format(index) + lines[i]
    
    if not usedArray[i] and lines[i].endswith(STANDARD_PATTERN.format(index)):
        lines[i] = lines[i].replace(STANDARD_PATTERN.format(index), DB_PATTERN.format(index, hexStr(rom[i], 2)))
    
    if (i + 1) % 0x8000 == 0 and i != 0:
        lines[i] += "\n" + (sect := defsect.format(section, hexStr(section * 0x8000, 6) + "H"))
        section += 1
    
    if lines[i].startswith(STANDARD_PATTERN.format(index) + "DB ") or lines[i].startswith(LAB_PATTERN.format(index, lastlab) + STANDARD_PATTERN.format(index) + "DB "):
        if dbmode == 0:
            if rom[i] in [*range(48, 58), *range(65, 91), *range(97, 123)]:
                dbs = 1
                dbmode = 1
                if lines[i].startswith(LAB_PATTERN.format(index, lastlab)):
                    lines[i] = LAB_PATTERN.format(index, lastlab) + ASCII_PATTERN.format(index, chr(rom[i]))
                else:
                    lines[i] = ASCII_PATTERN.format(index, chr(rom[i]))
        else:
            if rom[i] < 32 or rom[i] > 127:
                if rom[i] == 0:
                    asciz = dbs
                else:
                    asciz = None
                dbs = 1
                dbmode = 0
                if lines[i - 1].endswith(", 22h, \"\""):
                    lines[i - 1] = lines[i - 1][:-4]
        
        if dbmode == 0:
            if dbs < 8 and sect not in lines[i - 1]:
                if asciz and (lines[i - asciz].startswith(STANDARD_PATTERN.format(hexStr(i - asciz, 6)) + "ASCII ") or lines[i - asciz].startswith(LAB_PATTERN.format(hexStr(i - asciz, 6), lastlab) + STANDARD_PATTERN.format(hexStr(i - asciz, 6)) + "ASCII ")):
                    lines[i - asciz] = lines[i - asciz].replace(STANDARD_PATTERN.format(hexStr(i - asciz, 6)) + "ASCII ", STANDARD_PATTERN.format(hexStr(i - asciz, 6)) + "ASCIZ ")
                    lines[i] = STANDARD_PATTERN.format(index)
                elif (lines[i - dbs].startswith(STANDARD_PATTERN.format(hexStr(i - dbs, 6)) + "DB ") or lines[i - dbs].startswith(LAB_PATTERN.format(hexStr(i - dbs, 6), lastlab) + STANDARD_PATTERN.format(hexStr(i - dbs, 6)) + "DB ")) and not lines[i].startswith(LAB_PATTERN.format(hexStr(i, 6), lastlab) + STANDARD_PATTERN.format(hexStr(i, 6)) + "DB "):
                    lines[i - dbs] += ", {}h".format(hexStr(rom[i], 2))
                    lines[i] = STANDARD_PATTERN.format(index)
                    dbs += 1
                else:
                    dbs = 1
                    dbmode = 0                    
                
                if (i + 1) % 0x8000 == 0 and i + 1 < len(rom):
                    lines[i] += "\n" + sect
        
            else:
                dbs = 1                    
        elif lines[i - dbs].startswith(STANDARD_PATTERN.format(hexStr(i - dbs, 6)) + "ASCII ") or lines[i - dbs].startswith(LAB_PATTERN.format(hexStr(i - dbs, 6), lastlab) + STANDARD_PATTERN.format(hexStr(i - dbs, 6)) + "ASCII "):
            if rom[i] != 34:
                lines[i - dbs] = lines[i - dbs][:-1] + chr(rom[i]) + "\""
            else:
                lines[i - dbs] = lines[i - dbs] + ", 22h, \"\"" # special case for if there's a " in there for some reason
            lines[i] = STANDARD_PATTERN.format(index)
            if (i + 1) % 0x8000 == 0:
                lines[i - dbs] += "\n" + sect
                dbmode = 0
                dbs = 0
            dbs += 1
 
    else:
        if dbs != 1 or STANDARD_PATTERN.format(index) + "DB " in lines[i - 1] and SEPARATOR not in lines[i - 1]:
            lines[i - dbs] += SEPARATOR
            dbs = 1
            dbmode = 0

for i in range(len(lines)): # final formatting before replacements
    if args.bios:
        break
    if any(j in lines[i] for j in ["loc_0x00218C", "loc_0x002192", "loc_0x002198"]):
        if not lines[i - 1].endswith(SEPARATOR) and lines[i - 1] != STANDARD_PATTERN.format(hexStr(i - 1, 6)):
            lines[i - 1] += SEPARATOR # add separators for a couple of the IRQs
    elif "loc_0x00219E" in lines[i]: # cartridge IRQ is a pain to add a separator for
        if not lines[i - 1].endswith(SEPARATOR) and lines[i - 1] != STANDARD_PATTERN.format(hexStr(i - 1, 6)):
            lines[i - 1] += SEPARATOR
        j = 0
        while j < 10:
            if ASCII_PATTERN.format("21A4", "N")[:-1] in lines[i + j] or ASCIZ_PATTERN.format("21A4", "N")[:-1] in lines[i + j]:
                back = 1
                while lines[i + j - back] == STANDARD_PATTERN.format(hexStr(i + j - back, 6)):
                    back += 1
                if not lines[i + j - back].endswith(SEPARATOR):
                    lines[i + j - back] += SEPARATOR
                break
            j += 1
        break
    
progStart = args.offset if args.offset else 0 if args.bios else 0x2100

output = "\n".join([line.replace(STANDARD_PATTERN.format(hexStr(index + progStart, 6)) + "\n", "") + " ; {}".format(hexStr(index + progStart, 4).lower()) for index, line in enumerate(lines[progStart:]) if line != STANDARD_PATTERN.format(hexStr(index + progStart, 6))])
# clear empty lines
unuseds = []
unuseds_raw = []

for i in replacements:
    if (replacement := i[0]) in output:
        if replacement.startswith("loc_0x"):
            output = output.replace(replacement, i[1])
        else:
            output = output.replace("[{0}h]".format(replacement), "[{0}]".format(i[1])).replace("#{0}h".format(replacement), "#{0}".format(i[1]))
    else: # apply symbols
        if replacement.lstrip("loc_0x") not in output and "loc_0x{0}".format(replacement.zfill(6)) not in output and i[1] not in unuseds_raw:
            unuseds_raw.append(i[1])

for i in unuseds_raw:
    if i not in output:
        unuseds.append("Unused symbol: {}".format(i))    
    
if args.bios and not args.offset:
    output = defsect_bios + "\n" + output
elif section == 1:
    output = defsect.format("", "{}H".format(hexStr(progStart, 4))) + "\n" + output
else:
    output = defsect.format(0, "{}H".format(hexStr(progStart, 4))) + "\n" + output
# final prettification
if args.out is not None:
    outpath = args.out
else:
    outpath = ".".join(args.inp.split(".")[:-1]) + ".asm"

asm = open(outpath, "w")

print("Disassembly of {} saved to {}".format(args.inp, outpath))

asm.write(output)
asm.close()
# print warnings and errors
if warnings:
    print("\n" + "\n".join(sorted(warnings)))
if errors:
    print("\n" + "\n".join(sorted(errors)))
if unuseds:
    print("\n" + "\n".join(sorted(unuseds)))