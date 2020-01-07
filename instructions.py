import json

instructions = [
    
    # when formatting, 0 = uint8_t, 1 = uint16_t, 2 = int8_t, 3 = int16_t, 4 = second uint8_t

    ["ADD A,A", ["00"], 1],
    ["ADD A,B", ["01"], 1],
    ["ADD A,#{0}h", ["02"], 2],
    ["ADD A,[HL]", ["03"], 1],
    ["ADD A,[BR:{0}h]", ["04"], 2],
    ["ADD A,[{1}h]", ["05"], 3],
    ["ADD A,[IX]", ["06"], 1],
    ["ADD A,[IY]", ["07"], 1],

    ["ADC A,A", ["08"], 1],
    ["ADC A,B", ["09"], 1],
    ["ADC A,#{0}h", ["0A"], 2],
    ["ADC A,[HL]", ["0B"], 1],
    ["ADC A,[BR:{0}h]", ["0C"], 2],
    ["ADC A,[{1}h]", ["0D"], 3],
    ["ADC A,[IX]", ["0E"], 1],
    ["ADC A,[IY]", ["0F"], 1],

    ["SUB A,A", ["10"], 1],
    ["SUB A,B", ["11"], 1],
    ["SUB A,#{0}h", ["12"], 2],
    ["SUB A,[HL]", ["13"], 1],
    ["SUB A,[BR:{0}h]", ["14"], 2],
    ["SUB A,[{1}h]", ["15"], 3],
    ["SUB A,[IX]", ["16"], 1],
    ["SUB A,[IY]", ["17"], 1],

    ["SBC A,A", ["18"], 1],
    ["SBC A,B", ["19"], 1],
    ["SBC A,#{0}h", ["1A"], 2],
    ["SBC A,[HL]", ["1B"], 1],
    ["SBC A,[BR:{0}h]", ["1C"], 2],
    ["SBC A,[{1}h]", ["1D"], 3],
    ["SBC A,[IX]", ["1E"], 1],
    ["SBC A,[IY]", ["1F"], 1],

    ["AND A,A", ["20"], 1],
    ["AND A,B", ["21"], 1],
    ["AND A,#{0}h", ["22"], 2],
    ["AND A,[HL]", ["23"], 1],
    ["AND A,[BR:{0}h]", ["24"], 2],
    ["AND A,[{1}h]", ["25"], 3],
    ["AND A,[IX]", ["26"], 1],
    ["AND A,[IY]", ["27"], 1],

    ["OR A,A", ["28"], 1],
    ["OR A,B", ["29"], 1],
    ["OR A,#{0}h", ["2A"], 2],
    ["OR A,[HL]", ["2B"], 1],
    ["OR A,[BR:{0}h]", ["2C"], 2],
    ["OR A,[{1}h]", ["2D"], 3],
    ["OR A,[IX]", ["2E"], 1],
    ["OR A,[IY]", ["2F"], 1],

    ["CP A,A", ["30"], 1],
    ["CP A,B", ["31"], 1],
    ["CP A,#{0}h", ["32"], 2],
    ["CP A,[HL]", ["33"], 1],
    ["CP A,[BR:{0}h]", ["34"], 2],
    ["CP A,[{1}h]", ["35"], 3],
    ["CP A,[IX]", ["36"], 1],
    ["CP A,[IY]", ["37"], 1],

    ["XOR A,A", ["38"], 1],
    ["XOR A,B", ["39"], 1],
    ["XOR A,#{0}h", ["3A"], 2],
    ["XOR A,[HL]", ["3B"], 1],
    ["XOR A,[BR:{0}h]", ["3C"], 2],
    ["XOR A,[{1}h]", ["3D"], 3],
    ["XOR A,[IX]", ["3E"], 1],
    ["XOR A,[IY]", ["3F"], 1],

    ["LD A,A", ["40"], 1],
    ["LD A,B", ["41"], 1],
    ["LD A,L", ["42"], 1],
    ["LD A,H", ["43"], 1],
    ["LD A,[BR:{0}h]", ["44"], 2],
    ["LD A,[HL]", ["45"], 1],
    ["LD A,[IX]", ["46"], 1],
    ["LD A,[IY]", ["47"], 1],

    ["LD B,A", ["48"], 1],
    ["LD B,B", ["49"], 1],
    ["LD B,L", ["4A"], 1],
    ["LD B,H", ["4B"], 1],
    ["LD B,[BR:{0}h]", ["4C"], 2],
    ["LD B,[HL]", ["4D"], 1],
    ["LD B,[IX]", ["4E"], 1],
    ["LD B,[IY]", ["4F"], 1],

    ["LD L,A", ["50"], 1],
    ["LD L,B", ["51"], 1],
    ["LD L,L", ["52"], 1],
    ["LD L,H", ["53"], 1],
    ["LD L,[BR:{0}h]", ["54"], 2],
    ["LD L,[HL]", ["55"], 1],
    ["LD L,[IX]", ["56"], 1],
    ["LD L,[IY]", ["57"], 1],

    ["LD H,A", ["58"], 1],
    ["LD H,B", ["59"], 1],
    ["LD H,L", ["5A"], 1],
    ["LD H,H", ["5B"], 1],
    ["LD H,[BR:{0}h]", ["5C"], 2],
    ["LD H,[HL]", ["5D"], 1],
    ["LD H,[IX]", ["5E"], 1],
    ["LD H,[IY]", ["5F"], 1],

    ["LD [IX],A", ["60"], 1],
    ["LD [IX],B", ["61"], 1],
    ["LD [IX],L", ["62"], 1],
    ["LD [IX],H", ["63"], 1],
    ["LD [IX],[BR:{0}h]", ["64"], 2],
    ["LD [IX],[HL]", ["65"], 1],
    ["LD [IX],[IX]", ["66"], 1],
    ["LD [IX],[IY]", ["67"], 1],

    ["LD [HL],A", ["68"], 1],
    ["LD [HL],B", ["69"], 1],
    ["LD [HL],L", ["6A"], 1],
    ["LD [HL],H", ["6B"], 1],
    ["LD [HL],[BR:{0}h]", ["6C"], 2],
    ["LD [HL],[HL]", ["6D"], 1],
    ["LD [HL],[IX]", ["6E"], 1],
    ["LD [HL],[IY]", ["6F"], 1],

    ["LD [IY],A", ["70"], 1],
    ["LD [IY],B", ["71"], 1],
    ["LD [IY],L", ["72"], 1],
    ["LD [IY],H", ["73"], 1],
    ["LD [IY],[BR:{0}h]", ["74"], 2],
    ["LD [IY],[HL]", ["75"], 1],
    ["LD [IY],[IX]", ["76"], 1],
    ["LD [IY],[IY]", ["77"], 1],

    ["LD [BR:{0}h],A", ["78"], 2],
    ["LD [BR:{0}h],B", ["79"], 2],
    ["LD [BR:{0}h],L", ["7A"], 2],
    ["LD [BR:{0}h],H", ["7B"], 2],
    # 7C
    None,
    ["LD [BR:{0}h],[HL]", ["7D"], 2],
    ["LD [BR:{0}h],[IX]", ["7E"], 2],
    ["LD [BR:{0}h],[IY]", ["7F"], 2],

    ["INC A", ["80"], 1],
    ["INC B", ["81"], 1],
    ["INC L", ["82"], 1],
    ["INC H", ["83"], 1],
    ["INC BR", ["84"], 1],
    ["INC [BR:{0}h]", ["85"], 2],
    ["INC [HL]", ["86"], 1],
    ["INC SP", ["87"], 1],

    ["DEC A", ["88"], 1],
    ["DEC B", ["89"], 1],
    ["DEC L", ["8A"], 1],
    ["DEC H", ["8B"], 1],
    ["DEC BR", ["8C"], 1],
    ["DEC [BR:{0}h]", ["8D"], 2],
    ["DEC [HL]", ["8E"], 1],
    ["DEC SP", ["8F"], 1],

    ["INC BA", ["90"], 1],
    ["INC HL", ["91"], 1],
    ["INC IX", ["92"], 1],
    ["INC IY", ["93"], 1],

    ["BIT A,B", ["94"], 1],
    ["BIT [HL],#{0}h", ["95"], 2],
    ["BIT A,#{0}h", ["96"], 2],
    ["BIT B,#{0}h", ["97"], 2],

    ["DEC BA", ["98"], 1],
    ["DEC HL", ["99"], 1],
    ["DEC IX", ["9A"], 1],
    ["DEC IY", ["9B"], 1],

    ["AND SC,#{0}h", ["9C"], 2],

    ["OR SC,#{0}h", ["9D"], 2],

    ["XOR SC,#{0}h", ["9E"], 2],

    ["LD SC,#{0}h", ["9F"], 2],

    ["PUSH BA", ["A0"], 1],
    ["PUSH HL", ["A1"], 1],
    ["PUSH IX", ["A2"], 1],
    ["PUSH IY", ["A3"], 1],
    ["PUSH BR", ["A4"], 1],
    ["PUSH EP", ["A5"], 1],
    ["PUSH IP", ["A6"], 1],
    ["PUSH SC", ["A7"], 1],

    ["POP BA", ["A8"], 1],
    ["POP HL", ["A9"], 1],
    ["POP IX", ["AA"], 1],
    ["POP IY", ["AB"], 1],
    ["POP BR", ["AC"], 1],
    ["POP EP", ["AD"], 1],
    ["POP IP", ["AE"], 1],
    ["POP SC", ["AF"], 1],

    ["LD A,#{0}h", ["B0"], 2],
    ["LD B,#{0}h", ["B1"], 2],
    ["LD L,#{0}h", ["B2"], 2],
    ["LD H,#{0}h", ["B3"], 2],
    ["LD BR,#{0}h", ["B4"], 2],
    ["LD [HL],#{0}h", ["B5"], 2],
    ["LD [IX],#{0}h", ["B6"], 2],
    ["LD [IY],#{0}h", ["B7"], 2],
    ["LD BA,[{1}h]", ["B8"], 3],
    ["LD HL,[{1}h]", ["B9"], 3],
    ["LD IX,[{1}h]", ["BA"], 3],
    ["LD IY,[{1}h]", ["BB"], 3],
    ["LD [{1}h],BA", ["BC"], 3],
    ["LD [{1}h],HL", ["BD"], 3],
    ["LD [{1}h],IX", ["BE"], 3],
    ["LD [{1}h],IY", ["BF"], 3],

    ["ADD BA,#{1}h", ["C0"], 3],
    ["ADD HL,#{1}h", ["C1"], 3],
    ["ADD IX,#{1}h", ["C2"], 3],
    ["ADD IY,#{1}h", ["C3"], 3],

    ["LD BA,#{1}h", ["C4"], 3],
    ["LD HL,#{1}h", ["C5"], 3],
    ["LD IX,#{1}h", ["C6"], 3],
    ["LD IY,#{1}h", ["C7"], 3],

    ["EX BA,HL", ["C8"], 1],
    ["EX BA,IX", ["C9"], 1],
    ["EX BA,IY", ["CA"], 1],
    ["EX BA,SP", ["CB"], 1],
    ["EX A,B", ["CC"], 1],
    ["EX A,[HL]", ["CD"], 1],
    [
        ["ADD A,[IX+{2}h]", ["CE", "00"], 3],
        ["ADD A,[IY+{2}h]", ["CE", "01"], 3],
        ["ADD A,[IX+L]", ["CE", "02"], 2],
        ["ADD A,[IY+L]", ["CE", "03"], 2],
        ["ADD [HL],A", ["CE", "04"], 2],
        ["ADD [HL],#{0}h", ["CE", "05"], 3],
        ["ADD [HL],[IX]", ["CE", "06"], 2],
        ["ADD [HL],[IY]", ["CE", "07"], 2],

        ["ADC A,[IX+{2}h]", ["CE", "08"], 3],
        ["ADC A,[IX+{2}h]", ["CE", "09"], 3],
        ["ADC A,[IX+L]", ["CE", "0A"], 2],
        ["ADC A,[IY+L]", ["CE", "0B"], 2],
        ["ADC [HL],A", ["CE", "0C"], 2],
        ["ADC [HL],#{0}h", ["CE", "0D"], 3],
        ["ADC [HL],[IX]", ["CE", "0E"], 2],
        ["ADC [HL],[IY]", ["CE", "0F"], 2],

        ["SUB A,[IX+{2}h]", ["CE", "10"], 3],
        ["SUB A,[IX+{2}h]", ["CE", "11"], 3],
        ["SUB A,[IX+L]", ["CE", "12"], 2],
        ["SUB A,[IY+L]", ["CE", "13"], 2],
        ["SUB [HL],A", ["CE", "14"], 2],
        ["SUB [HL],#{0}h", ["CE", "15"], 3],
        ["SUB [HL],[IX]", ["CE", "16"], 2],
        ["SUB [HL],[IY]", ["CE", "17"], 2],

        ["SBC A,[IX+{2}h]", ["CE", "18"], 3],
        ["SBC A,[IX+{2}h]", ["CE", "19"], 3],
        ["SBC A,[IX+L]", ["CE", "1A"], 2],
        ["SBC A,[IY+L]", ["CE", "1B"], 2],
        ["SBC [HL],A", ["CE", "1C"], 2],
        ["SBC [HL],#{0}h", ["CE", "1D"], 3],
        ["SBC [HL],[IX]", ["CE", "1E"], 2],
        ["SBC [HL],[IY]", ["CE", "1F"], 2],

        ["AND A,[IX+{2}h]", ["CE", "20"], 3],
        ["AND A,[IX+{2}h]", ["CE", "21"], 3],
        ["AND A,[IX+L]", ["CE", "22"], 2],
        ["AND A,[IY+L]", ["CE", "23"], 2],
        ["AND [HL],A", ["CE", "24"], 2],
        ["AND [HL],#{0}h", ["CE", "25"], 3],
        ["AND [HL],[IX]", ["CE", "26"], 2],
        ["AND [HL],[IY]", ["CE", "27"], 2],

        ["OR A,[IX+{2}h]", ["CE", "28"], 3],
        ["OR A,[IX+{2}h]", ["CE", "29"], 3],
        ["OR A,[IX+L]", ["CE", "2A"], 2],
        ["OR A,[IY+L]", ["CE", "2B"], 2],
        ["OR [HL],A", ["CE", "2C"], 2],
        ["OR [HL],#{0}h", ["CE", "2D"], 3],
        ["OR [HL],[IX]", ["CE", "2E"], 2],
        ["OR [HL],[IY]", ["CE", "2F"], 2],

        ["CP A,[IX+{2}h]", ["CE", "30"], 3],
        ["CP A,[IX+{2}h]", ["CE", "31"], 3],
        ["CP A,[IX+L]", ["CE", "32"], 2],
        ["CP A,[IY+L]", ["CE", "33"], 2],
        ["CP [HL],A", ["CE", "34"], 2],
        ["CP [HL],#{0}h", ["CE", "35"], 3],
        ["CP [HL],[IX]", ["CE", "36"], 2],
        ["CP [HL],[IY]", ["CE", "37"], 2],

        ["XOR A,[IX+{2}h]", ["CE", "38"], 3],
        ["XOR A,[IX+{2}h]", ["CE", "39"], 3],
        ["XOR A,[IX+L]", ["CE", "3A"], 2],
        ["XOR A,[IY+L]", ["CE", "3B"], 2],
        ["XOR [HL],A", ["CE", "3C"], 2],
        ["XOR [HL],#{0}h", ["CE", "3D"], 3],
        ["XOR [HL],[IX]", ["CE", "3E"], 2],
        ["XOR [HL],[IY]", ["CE", "3F"], 2],

        ["LD A,[IX+{0}h]", ["CE", "40"], 3],
        ["LD A,[IY+{0}h]", ["CE", "41"], 3],
        ["LD A,[IX+L]", ["CE", "42"], 2],
        ["LD A,[IY+L]", ["CE", "43"], 2],

        ["LD [IX+{0}h],A", ["CE", "44"], 3],
        ["LD [IY+{0}h],A", ["CE", "45"], 3],
        ["LD [IX+L],A", ["CE", "46"], 2],
        ["LD [IY+L],A", ["CE", "47"], 2],

        ["LD B,[IX+{0}h]", ["CE", "48"], 3],
        ["LD B,[IY+{0}h]", ["CE", "49"], 3],
        ["LD B,[IX+L]", ["CE", "4A"], 2],
        ["LD B,[IY+L]", ["CE", "4B"], 2],

        ["LD [IX+{0}h],B", ["CE", "4C"], 3],
        ["LD [IY+{0}h],B", ["CE", "4D"], 3],
        ["LD [IX+L],B", ["CE", "4E"], 2],
        ["LD [IY+L],B", ["CE", "4F"], 2],

        ["LD L,[IX+{0}h]", ["CE", "50"], 3],
        ["LD L,[IY+{0}h]", ["CE", "51"], 3],
        ["LD L,[IX+L]", ["CE", "52"], 2],
        ["LD L,[IY+L]", ["CE", "53"], 2],

        ["LD [IX+{0}h],L", ["CE", "54"], 3],
        ["LD [IY+{0}h],L", ["CE", "55"], 3],
        ["LD [IX+L],L", ["CE", "56"], 2],
        ["LD [IY+L],L", ["CE", "57"], 2],

        ["LD H,[IX+{0}h]", ["CE", "58"], 3],
        ["LD H,[IY+{0}h]", ["CE", "59"], 3],
        ["LD H,[IX+L]", ["CE", "5A"], 2],
        ["LD H,[IY+L]", ["CE", "5B"], 2],

        ["LD [IX+{0}h],H", ["CE", "5C"], 3],
        ["LD [IY+{0}h],H", ["CE", "5D"], 3],
        ["LD [IX+L],H", ["CE", "5E"], 2],
        ["LD [IY+L],H", ["CE", "5F"], 2],

        ["LD [HL],[IX+{0}h]", ["CE", "60"], 3],
        ["LD [HL],[IY+{0}h]", ["CE", "61"], 3],
        ["LD [HL],[IX+L]", ["CE", "62"], 2],
        ["LD [HL],[IY+L]", ["CE", "63"], 2],

        # CE 64, CE 65, CE 66, CE 67
        None, None, None, None,

        ["LD [IX],[IX+{0}h]", ["CE", "68"], 3],
        ["LD [IX],[IY+{0}h]", ["CE", "69"], 3],
        ["LD [IX],[IX+L]", ["CE", "6A"], 2],
        ["LD [IX],[IY+L]", ["CE", "6B"], 2],

        # CE 6C, CE 6D, CE 6E, CE 6F
        None, None, None, None,

        # CE 70, CE 71, CE 72, CE 73, CE 74, CE 75, CE 76, CE 77
        None, None, None, None, None, None, None, None,

        ["LD [IY],[IX+{0}h]", ["CE", "78"], 3],
        ["LD [IY],[IY+{0}h]", ["CE", "79"], 3],
        ["LD [IY],[IX+L]", ["CE", "7A"], 2],
        ["LD [IY],[IY+L]", ["CE", "7B"], 2],

        ["LD [{1}h],SP", ["CE", "7C"], 4],

        # CE 7D, CE 7E, CE 7F
        None, None, None,

        ["SLA A", ["CE", "80"], 2],
        ["SLA B", ["CE", "81"], 2],
        ["SLA [BR:{0}h]", ["CE", "82"], 3],
        ["SLA [HL]", ["CE", "83"], 2],

        ["SLL A", ["CE", "84"], 2],
        ["SLL B", ["CE", "85"], 2],
        ["SLL [BR:{0}h]", ["CE", "86"], 3],
        ["SLL [HL]", ["CE", "87"], 2],

        ["SRA A", ["CE", "88"], 2],
        ["SRA B", ["CE", "89"], 2],
        ["SRA [BR:{0}h]", ["CE", "8A"], 3],
        ["SRA [HL]", ["CE", "8B"], 2],

        ["SRL A", ["CE", "8C"], 2],
        ["SRL B", ["CE", "8D"], 2],
        ["SRL [BR:{0}h]", ["CE", "8E"], 3],
        ["SRL [HL]", ["CE", "8F"], 2],

        ["RL A", ["CE", "90"], 2],
        ["RL B", ["CE", "91"], 2],
        ["RL [BR:{0}h]", ["CE", "92"], 3],
        ["RL [HL]", ["CE", "93"], 2],

        ["RLC A", ["CE", "94"], 2],
        ["RLC B", ["CE", "95"], 2],
        ["RLC [BR:{0}h]", ["CE", "96"], 3],
        ["RLC [HL]", ["CE", "97"], 2],

        ["RR A", ["CE", "98"], 2],
        ["RR B", ["CE", "99"], 2],
        ["RR [BR:{0}h]", ["CE", "9A"], 3],
        ["RR [HL]", ["CE", "9B"], 2],

        ["RRC A", ["CE", "9C"], 2],
        ["RRC B", ["CE", "9D"], 2],
        ["RRC [BR:{0}h]", ["CE", "9E"], 3],
        ["RRC [HL]", ["CE", "9F"], 2],

        ["CPL A", ["CE", "A0"], 2],
        ["CPL B", ["CE", "A1"], 2],
        ["CPL [BR:{0}h]", ["CE", "A2"], 3],
        ["CPL [HL]", ["CE", "A3"], 2],

        ["NEG A", ["CE", "A4"], 2],
        ["NEG B", ["CE", "A5"], 2],
        ["NEG [BR:{0}h]", ["CE", "A6"], 3],
        ["NEG [HL]", ["CE", "A7"], 2],

        ["SEP", ["CE", "A8"], 2],

        # CE A9, CE AA, CE AB, CE AC, CE AD
        None, None, None, None, None,

        ["HALT", ["CE", "AE"], 2],

        ["SLP", ["CE", "AF"], 2],

        ["AND B,#{0}h", ["CE", "B0"], 3],
        ["AND L,#{0}h", ["CE", "B1"], 3],
        ["AND H,#{0}h", ["CE", "B2"], 3],

        # CE B3
        None,

        ["OR B,#{0}h", ["CE", "B4"], 3],
        ["OR L,#{0}h", ["CE", "B5"], 3],
        ["OR H,#{0}h", ["CE", "B6"], 3],

        # CE B7
        None,

        ["XOR B,#{0}h", ["CE", "B8"], 3],
        ["XOR L,#{0}h", ["CE", "B9"], 3],
        ["XOR H,#{0}h", ["CE", "BA"], 3],

        # CE BB
        None,

        ["CP B,#{0}h", ["CE", "BC"], 3],
        ["CP L,#{0}h", ["CE", "BD"], 3],
        ["CP H,#{0}h", ["CE", "BE"], 3],
        ["CP BR,#{0}h", ["CE", "BF"], 3],

        ["LD A,BR", ["CE", "C0"], 2],
        ["LD A,SC", ["CE", "C1"], 2],
        ["LD BR,A", ["CE", "C2"], 2],
        ["LD SC,A", ["CE", "C3"], 2],

        ["LD NB,#{0}h", ["CE", "C4"], 3],
        ["LD EP,#{0}h", ["CE", "C5"], 3],
        ["LD XP,#{0}h", ["CE", "C6"], 3],
        ["LD YP,#{0}h", ["CE", "C7"], 3],

        ["LD A,NB", ["CE", "C8"], 2],
        ["LD A,EP", ["CE", "C9"], 2],
        ["LD A,XP", ["CE", "CA"], 2],
        ["LD A,YP", ["CE", "CB"], 2],
        ["LD NB,A", ["CE", "CC"], 2],
        ["LD EP,A", ["CE", "CD"], 2],
        ["LD XP,A", ["CE", "CE"], 2],
        ["LD YP,A", ["CE", "CF"], 2],

        ["LD A,[{1}h]", ["CE", "D0"], 4],
        ["LD B,[{1}h]", ["CE", "D1"], 4],
        ["LD L,[{1}h]", ["CE", "D2"], 4],
        ["LD H,[{1}h]", ["CE", "D3"], 4],
        ["LD [{1}h],A", ["CE", "D4"], 4],
        ["LD [{1}h],B", ["CE", "D5"], 4],
        ["LD [{1}h],L", ["CE", "D6"], 4],
        ["LD [{1}h],H", ["CE", "D7"], 4],

        ["MLT", ["CE", "D8"], 2],
        ["DIV", ["CE", "D9"], 2],

        # CE DA, CE DB, CE DC, CE DD, CE DE, CE DF
        None, None, None, None, None, None,


        ["JRS LT,{2}", ["CE", "E0"], 3],
        ["JRS LE,{2}", ["CE", "E1"], 3],
        ["JRS GT,{2}", ["CE", "E2"], 3],
        ["JRS GE,{2}", ["CE", "E3"], 3],
        ["JRS V,{2}", ["CE", "E4"], 3],
        ["JRS NV,{2}", ["CE", "E5"], 3],
        ["JRS P,{2}", ["CE", "E6"], 3],
        ["JRS M,{2}", ["CE", "E7"], 3],
        ["JRS F0,{2}", ["CE", "E8"], 3],
        ["JRS F1,{2}", ["CE", "E9"], 3],
        ["JRS F2,{2}", ["CE", "EA"], 3],
        ["JRS F3,{2}", ["CE", "EB"], 3],
        ["JRS NF0,{2}", ["CE", "EC"], 3],
        ["JRS NF1,{2}", ["CE", "ED"], 3],
        ["JRS NF2,{2}", ["CE", "EE"], 3],
        ["JRS NF3,{2}", ["CE", "EF"], 3],

        ["CARS LT,{2}", ["CE", "F0"], 3],
        ["CARS LE,{2}", ["CE", "F1"], 3],
        ["CARS GT,{2}", ["CE", "F2"], 3],
        ["CARS GE,{2}", ["CE", "F3"], 3],
        ["CARS V,{2}", ["CE", "F4"], 3],
        ["CARS NV,{2}", ["CE", "F5"], 3],
        ["CARS P,{2}", ["CE", "F6"], 3],
        ["CARS M,{2}", ["CE", "F7"], 3],
        ["CARS F0,{2}", ["CE", "F8"], 3],
        ["CARS F1,{2}", ["CE", "F9"], 3],
        ["CARS F2,{2}", ["CE", "FA"], 3],
        ["CARS F3,{2}", ["CE", "FB"], 3],
        ["CARS NF0,{2}", ["CE", "FC"], 3],
        ["CARS NF1,{2}", ["CE", "FD"], 3],
        ["CARS NF2,{2}", ["CE", "FE"], 3],
        ["CARS NF3,{2}", ["CE", "FF"], 3],
    ],
    [
        ["ADD BA,BA", ["CF", "00"], 2],
        ["ADD BA,HL", ["CF", "01"], 2],
        ["ADD BA,IX", ["CF", "02"], 2],
        ["ADD BA,IY", ["CF", "03"], 2],

        ["ADC BA,BA", ["CF", "04"], 2],
        ["ADC BA,HL", ["CF", "05"], 2],
        ["ADC BA,IX", ["CF", "06"], 2],
        ["ADC BA,IY", ["CF", "07"], 2],

        ["SUB BA,BA", ["CF", "08"], 2],
        ["SUB BA,HL", ["CF", "09"], 2],
        ["SUB BA,IX", ["CF", "0A"], 2],
        ["SUB BA,IY", ["CF", "0B"], 2],

        ["SBC BA,BA", ["CF", "0C"], 2],
        ["SBC BA,HL", ["CF", "0D"], 2],
        ["SBC BA,IX", ["CF", "0E"], 2],
        ["SBC BA,IY", ["CF", "0F"], 2],

        # CF 10, CF 11, CF 12, CF 13, CF 14, CF 15, CF 16, CF 17
        None, None, None, None, None, None, None, None,

        ["CP BA,BA", ["CF", "18"], 2],
        ["CP BA,HL", ["CF", "19"], 2],
        ["CP BA,IX", ["CF", "1A"], 2],
        ["CP BA,IY", ["CF", "1B"], 2],

        # CF 1C, CF 1D, CF 1E, CF 1F
        None, None, None, None,

        ["ADD HL,BA", ["CF", "20"], 2],
        ["ADD HL,HL", ["CF", "21"], 2],
        ["ADD HL,IX", ["CF", "22"], 2],
        ["ADD HL,IY", ["CF", "23"], 2],

        ["ADC HL,BA", ["CF", "24"], 2],
        ["ADC HL,HL", ["CF", "25"], 2],
        ["ADC HL,IX", ["CF", "26"], 2],
        ["ADC HL,IY", ["CF", "27"], 2],

        ["SUB HL,BA", ["CF", "28"], 2],
        ["SUB HL,HL", ["CF", "29"], 2],
        ["SUB HL,IX", ["CF", "2A"], 2],
        ["SUB HL,IY", ["CF", "2B"], 2],

        ["SBC HL,BA", ["CF", "2C"], 2],
        ["SBC HL,HL", ["CF", "2D"], 2],
        ["SBC HL,IX", ["CF", "2E"], 2],
        ["SBC HL,IY", ["CF", "2F"], 2],

        # CF 30, CF 31, CF 32, CF 33, CF 34, CF 35, CF 36, CF 37
        None, None, None, None, None, None, None, None,

        ["CP HL,BA", ["CF", "38"], 2],
        ["CP HL,HL", ["CF", "39"], 2],
        ["CP HL,IX", ["CF", "3A"], 2],
        ["CP HL,IY", ["CF", "3B"], 2],

        # CF 3C, CF 3D, CF 3E, CF 3F
        None, None, None, None,

        ["ADD IX,BA", ["CF", "40"], 2],
        ["ADD IX,HL", ["CF", "41"], 2],
        ["ADD IY,BA", ["CF", "42"], 2],
        ["ADD IY,HL", ["CF", "43"], 2],
        ["ADD SP,BA", ["CF", "44"], 2],
        ["ADD SP,HL", ["CF", "45"], 2],

        # CF 46, CF 47
        None, None,

        ["SUB IX,BA", ["CF", "48"], 2],
        ["SUB IX,HL", ["CF", "49"], 2],
        ["SUB IY,BA", ["CF", "4A"], 2],
        ["SUB IY,HL", ["CF", "4B"], 2],
        ["SUB SP,BA", ["CF", "4C"], 2],
        ["SUB SP,HL", ["CF", "4D"], 2],

        # CF 4E, CF 4F
        None, None,

        # CF 50, CF 51, CF 52, CF 53, CF 54, CF 55, CF 56, CF 57, CF 58, CF 59, CF 5A, CF 5B
        None, None, None, None, None, None, None, None, None, None, None, None,

        ["CP SP,BA", ["CF", "5C"], 2],
        ["CP SP,HL", ["CF", "5D"], 2],

        # CF 5E, CF 5F
        None, None,

        ["ADC BA,#{1}h", ["CF", "60"], 4],
        ["ADC HL,#{1}h", ["CF", "61"], 4],

        ["SBC BA,#{1}h", ["CF", "62"], 4],
        ["SBC HL,#{1}h", ["CF", "63"], 4],

        # CF 64, CF 65, CF 66, CF 67
        None, None, None, None,

        ["ADD SP,#{1}h", ["CF", "68"], 4],

        # CF 69
        None,

        ["SUB SP,#{1}h", ["CF", "6A"], 4],

        # CF 6B
        None,

        ["CP SP,#{1}h", ["CF", "6C"], 4],

        # CF 6D
        None,

        ["LD SP,#{1}h", ["CF", "6E"], 4],

        # CF 6F
        None,

        ["LD BA,[SP+{0}h]", ["CF", "70"], 3],
        ["LD HL,[SP+{0}h]", ["CF", "71"], 3],
        ["LD IX,[SP+{0}h]", ["CF", "72"], 3],
        ["LD IY,[SP+{0}h]", ["CF", "73"], 3],
        ["LD [SP+{0}h],BA", ["CF", "74"], 3],
        ["LD [SP+{0}h],HL", ["CF", "75"], 3],
        ["LD [SP+{0}h],IX", ["CF", "76"], 3],
        ["LD [SP+{0}h],IY", ["CF", "77"], 3],
        ["LD SP,[{1}h]", ["CF", "78"], 4],

        # CF 79, CF 7A, CF 7B, CF 7C, CF 7D, CF 7E, CF 7F
        None, None, None, None, None, None, None,

        # CF 80 - CF AF
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None,

        ["PUSH A", ["CF", "B0"], 2],
        ["PUSH B", ["CF", "B1"], 2],
        ["PUSH L", ["CF", "B2"], 2],
        ["PUSH H", ["CF", "B3"], 2],

        ["POP A", ["CF", "B4"], 2],
        ["POP B", ["CF", "B5"], 2],
        ["POP L", ["CF", "B6"], 2],
        ["POP H", ["CF", "B7"], 2],

        ["PUSH ALL", ["CF", "B8"], 2],
        ["PUSH ALE", ["CF", "B9"], 2],

        # CF BA, CF BB
        None, None,

        ["POP ALL", ["CF", "BC"], 2],
        ["POP ALE", ["CF", "BD"], 2],

        # CF BE, CF BF
        None, None,

        ["LD BA,[HL]", ["CF", "C0"], 2],
        ["LD HL,[HL]", ["CF", "C1"], 2],
        ["LD IX,[HL]", ["CF", "C2"], 2],
        ["LD IY,[HL]", ["CF", "C3"], 2],
        ["LD [HL],BA", ["CF", "C4"], 2],
        ["LD [HL],HL", ["CF", "C5"], 2],
        ["LD [HL],IX", ["CF", "C6"], 2],
        ["LD [HL],IY", ["CF", "C7"], 2],

        # CF C8, CF C9, CF CA, CF CB, CF CC, CF CD, CF CE, CF CF
        None, None, None, None, None, None, None, None,

        ["LD BA,[IX]", ["CF", "D0"], 2],
        ["LD HL,[IX]", ["CF", "D1"], 2],
        ["LD IX,[IX]", ["CF", "D2"], 2],
        ["LD IY,[IX]", ["CF", "D3"], 2],
        ["LD [IX],BA", ["CF", "D4"], 2],
        ["LD [IX],HL", ["CF", "D5"], 2],
        ["LD [IX],IX", ["CF", "D6"], 2],
        ["LD [IX],IY", ["CF", "D7"], 2],
        ["LD BA,[IY]", ["CF", "D8"], 2],
        ["LD HL,[IY]", ["CF", "D9"], 2],
        ["LD IX,[IY]", ["CF", "DA"], 2],
        ["LD IY,[IY]", ["CF", "DB"], 2],
        ["LD [IY],BA", ["CF", "DC"], 2],
        ["LD [IY],HL", ["CF", "DD"], 2],
        ["LD [IY],IX", ["CF", "DE"], 2],
        ["LD [IY],IY", ["CF", "DF"], 2],

        ["LD BA,BA", ["CF", "E0"], 2],
        ["LD BA,HL", ["CF", "E1"], 2],
        ["LD BA,IX", ["CF", "E2"], 2],
        ["LD BA,IY", ["CF", "E3"], 2],
        ["LD HL,BA", ["CF", "E4"], 2],
        ["LD HL,HL", ["CF", "E5"], 2],
        ["LD HL,IX", ["CF", "E6"], 2],
        ["LD HL,IY", ["CF", "E7"], 2],
        ["LD IX,BA", ["CF", "E8"], 2],
        ["LD IX,HL", ["CF", "E9"], 2],
        ["LD IX,IX", ["CF", "EA"], 2],
        ["LD IX,IY", ["CF", "EB"], 2],
        ["LD IY,BA", ["CF", "EC"], 2],
        ["LD IY,HL", ["CF", "ED"], 2],
        ["LD IY,IX", ["CF", "EE"], 2],
        ["LD IY,IY", ["CF", "EF"], 2],

        ["LD SP,BA", ["CF", "F0"], 2],
        ["LD SP,HL", ["CF", "F1"], 2],
        ["LD SP,IX", ["CF", "F2"], 2],
        ["LD SP,IY", ["CF", "F3"], 2],
        ["LD HL,SP", ["CF", "F4"], 2],
        ["LD HL,PC", ["CF", "F5"], 2],

        # CF F6, CF F7
        None, None,

        ["LD BA,SP", ["CF", "F8"], 2],
        ["LD BA,PC", ["CF", "F9"], 2],
        ["LD IX,SP", ["CF", "FA"], 2],

        # CF FB, CF FC, CF FD
        None, None, None,

        ["LD IY,SP", ["CF", "FE"], 2],

        # CF FF
        None,
    ],
    ["SUB BA,#{1}h", ["D0"], 3],
    ["SUB HL,#{1}h", ["D1"], 3],
    ["SUB IX,#{1}h", ["D2"], 3],
    ["SUB IY,#{1}h", ["D3"], 3],

    ["CP BA,#{1}h", ["D4"], 3],
    ["CP HL,#{1}h", ["D5"], 3],
    ["CP IX,#{1}h", ["D6"], 3],
    ["CP IY,#{1}h", ["D7"], 3],

    ["AND [BR:{0}h],#{4}h", ["D8"], 3],

    ["OR [BR:{0}h],#{4}h", ["D9"], 3],

    ["XOR [BR:{0}h],#{4}h", ["DA"], 3],

    ["CP [BR:{0}h],#{4}h", ["DB"], 3],

    ["BIT [BR:{0}h],#{4}h", ["DC"], 3],

    ["LD [BR:{0}h],#{4}h", ["DD"], 3],

    ["PACK", ["DE"], 1],

    ["UPCK", ["DF"], 1],

    ["CARS C,{2}", ["E0"], 2],
    ["CARS NC,{2}", ["E1"], 2],
    ["CARS Z,{2}", ["E2"], 2],
    ["CARS NZ,{2}", ["E3"], 2],

    ["JRS C,{2}", ["E4"], 2],
    ["JRS NC,{2}", ["E5"], 2],
    ["JRS Z,{2}", ["E6"], 2],
    ["JRS NZ,{2}", ["E7"], 2],

    ["CARL C,{3}h", ["E8"], 3],
    ["CARL NC,{3}h", ["E9"], 3],
    ["CARL Z,{3}h", ["EA"], 3],
    ["CARL NZ,{3}h", ["EB"], 3],

    ["JRL C,{3}h", ["EC"], 3],
    ["JRL NC,{3}h", ["ED"], 3],
    ["JRL Z,{3}h", ["EE"], 3],
    ["JRL NZ,{3}h", ["EF"], 3],

    ["CARS {2}", ["F0"], 2],

    ["JRS {2}", ["F1"], 2],

    ["CARL {3}", ["F2"], 3],

    ["JRL {3}", ["F3"], 3],

    ["JP HL", ["F4"], 1],

    ["DJR NZ,{2}", ["F5"], 2],

    ["SWAP A", ["F6"], 1],
    ["SWAP [HL]", ["F7"], 1],

    ["RET", ["F8"], 1],
    ["RETE", ["F9"], 1],
    ["RETS", ["FA"], 1],

    ["CALL [{1}h]", ["FB"], 3],

    ["INT [{0}h]", ["FC"], 2],

    ["JP [{0}h]", ["FD"], 2],

    # FE
    None,

    ["NOP", ["FF"], 1],

]

json.dump(instructions, open("instructions.json", "w"))