// file: sti.cc
// author:  Steve Kinzler, August 1985
// stas.c - Stack Machine Assembly Language Interpreter

// revised:  Rick Walker, March 2005
//           added fpu instructions
//                FLT - float literal
//                OPR - 20 - cast int to float
//			33 - negate
//                      34 - add
//                      35 - subtract
//                      36 - multiply
//                      37 - divide
//                      40 - equal relop
//                      41 - not equal relop
//                      42 - less than
//                      43 - greater than or equal
//                      44 - greater than
//                      45 - less than or equal
//                      46 - read float
//                      47 - write float
//			52 - cast float to int
//          changed file handling to C++ streams
//          changed the address field of the assembly instruction to allow floats, though
//                  the only place this makes sense is when using FLT ... everywhere else
//                  it is cast to an int.  This is a real kludge, but it'll work in the 
//                  short run.
//          changed the stack cells from long to a union that can hold long or float (but
//                  not both)
//          comments should work, now (6/07)
//          addresses with multiple decimal points will cause the machine to halt with an
//                  input error.

#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

#define CODESIZE    3072
#define STACKSIZE   4096

#define OPR    1
#define LIT    2
#define LOD    3
#define STO    4
#define LAR    5
#define SAR    6
#define PAS    7
#define CAL    8
#define INT    9
#define JMP    10
#define JPC    11
#define FLT 34

struct instruction {
    int function, level;
    float address;
} code[CODESIZE];

union memory {
    long i;
    float f;
};

int cmax = 0;           // highest addressed instruction
memory s[STACKSIZE];    // data store
int p = 0,              // program register
    b = 1,              // base register
    t = 0;              // top register
    char *prog;         // program name

// Utility prototypes
int parse(ifstream &);
int interpret(void);
int base(int);

int main(int argc, char **argv)
{
    ifstream ins;       // sti source file

    prog = argv[0];
    if (argc == 2) {
        if (strcmp(argv[1] + strlen(argv[1]) - 3, ".st")) {
            cerr << prog << ": program file must end in \".st\"\n";
            exit(3);
        }
        ins.open(argv[1]);
        if (ins.fail()) {
            cerr << prog << ": cannot open " << argv[1] << " for reading\n";
            exit(2);
        }
        if (!parse(ins))
            interpret();
    } else {
        cerr << "usage: " << prog << " file.st\n";
        exit(1);
    }
    return 0;
}

// Processes the input file and produces an array of instructions that makes up the data store 
// of the machine.
int parse(ifstream & ins)
{
    char line[512],         // contents of current source line
         fct[4],            // function field of current source line
         comm[512];         // comment field of current source line
    int num,                // current source line number
        lev,                // level field of current source linelong
        err = 0;            // error flag
    float adr;              // address field of current source line2

    while (ins.getline(line, 512) != NULL) {
        if (sscanf(line, "%d%3s%d%f %511s", &num, fct, &lev, &adr, comm) != 4 &&      // instruction
            sscanf(line, "%d%3s%d%f #%511s", &num, fct, &lev, &adr, comm) != 4 &&      // instruction & empty comment
            sscanf(line, "%d%3s%d%f #%511s", &num, fct, &lev, &adr, comm) != 5) {       // instruction & comment
            if (sscanf(line, " #%511s", comm) == 0 &&                                  // comment
                sscanf(line, "%511s", comm) == 1) {                                    // blank line
                cerr << prog << ": improper line:\t"  << line << endl;
                err++;
            }
            continue;
        }
        if (num >= 0 && num < CODESIZE)
            cmax = (num + 1 > cmax) ? num + 1 : cmax;
        else {
            cerr << prog << ": line number " << num << " out of range, 0 thru " << CODESIZE - 1 << endl;
            err++;
            continue;
        }
        if (!strcasecmp(fct, "opr") || !strcmp(fct, "OPR"))
            code[num].function = OPR;
        else if (!strcasecmp(fct, "lit"))
            code[num].function = LIT;
        else if (!strcasecmp(fct, "flt"))
            code[num].function = FLT;
        else if (!strcasecmp(fct, "lod"))
            code[num].function = LOD;
        else if (!strcasecmp(fct, "sto"))
            code[num].function = STO;
        else if (!strcasecmp(fct, "lar"))
            code[num].function = LAR;
        else if (!strcasecmp(fct, "sar"))
            code[num].function = SAR;
        else if (!strcasecmp(fct, "pas"))
            code[num].function = PAS;
        else if (!strcasecmp(fct, "cal"))
            code[num].function = CAL;
        else if (!strcasecmp(fct, "int"))
            code[num].function = INT;
        else if (!strcasecmp(fct, "jmp"))
            code[num].function = JMP;
        else if (!strcasecmp(fct, "jpc"))
            code[num].function = JPC;
        else {
            cerr << prog << ": unknown function \"" << fct << "\" in instruction " << num << endl;
            err++;
        }
        if (lev >= 0)
            code[num].level = lev;
        else {
            cerr << prog << ": negative level " << lev << " in instruction " << num << endl;
            err++;
        }
        code[num].address = adr;
    }
    return(err);
}

// Processes the instructions in the data store to manipulate the contents of the stack.
int interpret()
{
    int fct, lev, x;
    float adr;

    s[1].i = s[2].i = s[3].i = 0;       // main block mark  
    do {
        fct = code[p].function;
        lev = code[p].level;
        adr = code[p++].address;        // increments p  
        switch (fct) {
        case OPR:                       // operation  
            switch ((int) adr) {
            case 0:                     // return  
                t = b - 1;
                p = s[t + 3].i;         // return address  
                b = s[t + 2].i;         // dynamic link  
                break;
            case 1:                     // integer negate  
                s[t].i = -s[t].i;
                break;
            case 33:                    // float negate
                s[t].f = -s[t].f;
                break;
            case 2:                     // integer addition  
                t--;
                s[t].i = s[t].i + s[t + 1].i;
                break;
            case 34:                    // float addition
                t--;
                s[t].f = s[t].f + s[t + 1].f;
                break;
            case 3:                     // integer subtraction  
                t--;
                s[t].i = s[t].i - s[t + 1].i;
                break;
            case 35:                    // float subtraction
                t--;
                s[t].f = s[t].f - s[t + 1].f;
                break;
            case 4:                     // integer multiplication  
                t--;
                s[t].i = s[t].i * s[t + 1].i;
                break;
            case 36:                    // float multiplication
                t--;
                s[t].f = s[t].f * s[t + 1].f;
                break;
            case 5:                     // machine independent integer division  
                t--;
                if (!s[t + 1].i)
                    cerr << prog << ": division by zero at instruction " << p - 1 << endl;
                else if (s[t + 1].i < 0)
                    s[t].i = (s[t].i < 0) ? -s[t].i / -s[t + 1].i : -(s[t].i / -s[t + 1].i);
                else
                    s[t].i = (s[t].i < 0) ? -(-s[t].i / s[t + 1].i) : s[t].i / s[t + 1].i;
                break;
            case 37:                    // float division
                t--;
                s[t].f = s[t].f / s[t + 1].f;
                break;
            case 6:                     // machine independent "odd" function  
                s[t].i = ((s[t].i < 0) ? -s[t].i : s[t].i) % 2 == 1;
                break;
            case 7:                     // replicate top of stack  
                t++;
                memcpy(&s[t], &s[t - 1], sizeof(memory));
                break;
            case 8:                     // integer equal  
                t--;
                s[t].i = s[t].i == s[t + 1].i;
                break;
            case 40:                    // float equal
                t--;
                s[t].i = s[t].f == s[t + 1].f;
                break;
            case 9:                     // integer not equal  
                t--;
                s[t].i = s[t].i != s[t + 1].i;
                break;
            case 41:                    // integer not equal
                t--;
                s[t].i = s[t].f != s[t + 1].f;
                break;
            case 10:                    // integer less than  
                t--;
                s[t].i = s[t].i < s[t + 1].i;
                break;
            case 42:                    // float less than
                t--;
                s[t].i = s[t].f < s[t + 1].f;
                break;
            case 11:                    // integer greater than or equal  
                t--;
                s[t].i = s[t].i >= s[t + 1].i;
                break;
            case 43:                    // float greater than or equal
                t--;
                s[t].i = s[t].f >= s[t + 1].f;
                break;
            case 12:                    // integer greater than  
                t--;
                s[t].i = s[t].i > s[t + 1].i;
                break;
            case 44:                    // float greater than
                t--;
                s[t].i = s[t].f > s[t + 1].f;
                break;
            case 13:                    // integer less than or equal  
                t--;
                s[t].i = s[t].i <= s[t + 1].i;
                break;
            case 45:                    // float less than or equal
		t--;
                s[t].i = s[t].f <= s[t + 1].f;
                break;
            case 14:                    // read integer  
                t++;
                //if ((x = scanf("%*[^-+0123456789]%ld", &s[t].i)) == 0)
                if ((x = scanf("%ld", &s[t].i)) == 0)
                    s[t].i = 0;
                else if (x == EOF) {
                    cerr << prog << ": read an end-of-file on integer read at instruction " << p - 1 << endl;
                    exit(4);
                }
                break;
            case 15:                    // write integer  
                cout << s[t].i << " ";
                t--;
                break;
            case 16:                    // read character  
                t++;
                if ((x = getchar()) == EOF) {
                    cerr << prog << ": read an end-of-file on character read at instruction " << p - 1 << endl;
                    exit(4);
                }
                s[t].i = (long) x;
                break;
            case 17:                    // write character  
                cout << (char) s[t].i;
                t--;
                break;
            case 46:                    // read float
                t++;
                //if ((x = scanf("%*[^-+0123456789.]%f", &s[t].f)) == 0)
                if ((x = scanf("%f", &s[t].f)) == 0)
                    s[t].f = 0;
                else if (x == EOF) {
                    cerr << prog << ": read an end-of-file on float read at instruction " << p - 1 << endl;
                    exit(4);
                }
                break;
            case 47:                    // write float
                cout << fixed << showpoint;
                cout << s[t].f << " ";
                t--;
                break;
            case 20:                    // cast: integer to float
                s[t].f = float(s[t].i);
                break;
            case 52:                    // cast: float to integer
                s[t].i = int(s[t].f);
                break;
            default:
                cerr << prog << ": invalid operation at instruction " << p - 1 << endl;
            }
            break;
        case LIT:                       // load integer literal  
            t++;
            s[t].i = long(adr);
            break;
        case FLT:                       // load float literal
            t++;
            s[t].f = adr;
            break;
        case LOD:                       // load variable  
            t++;
            memcpy(&s[t], &s[base(lev) + int(adr)], sizeof(memory));
            break;
        case STO:                       // store variable  
            memcpy(&s[base(lev) + int(adr)], &s[t], sizeof(memory));
            t--;
            break;
        case LAR:                       // load array element  
            memcpy(&s[t], &s[base(lev) + int(adr) + s[t].i - 1], sizeof(memory));
            break;
        case SAR:                       // store array element  
            memcpy(&s[base(lev) + int(adr) + s[t - 1].i -1], &s[t], sizeof(memory));
            t -= 2;
            break;
        case PAS:                       // pass values to subroutine  
            while (adr--  > 0) {
                //s[t + 3] = s[t];
                memcpy(&s[t+3], &s[t], sizeof(memory));
                t--;
            }
            break;
        case CAL:                       // call subroutine, generate new block mark  
            s[t + 1].i = base(lev);     // static link  
            s[t + 2].i = b;             // dynamic link  
            s[t + 3].i = p;             // return address  
            b = t + 1;
            p = int(adr);
            break;
        case INT:                       // increment top register  
            t += int(adr);
            break;
        case JMP:                       // jump  
            p = int(adr);
            break;
        case JPC:                       // jump conditionally  
            if (!s[t].i)
                p = int(adr);
            t--;
        }
    } while (p > 0 && p < cmax);        // while not exited or out of code  
}

// find base l levels down ... searches static link chain
int base(int l)                         
                                       
{
    int b1 = b;

    while (l--)
        b1 = s[b1].i;
    return(b1);
}
