#!/usr/bin/env python3.4

import random
import argparse

__all__ = []
__author__ = 'Andy Moe'
__email__ = 'moea@?.com'
__version__ = '0.9'

__ERR_STRING_LENGTH = "String length must be greater than zero!"
__ERR_INVALID_PARAMETERS = "Invalid parameters in function!"

#def generate_charscope_random_string(charscope, length):
#    assert length > 0, __ERR_STRING_LENGTH
#    assert charscope != None and charscope != "", "Charscope must be valid string of length > 0."
#    outbuf = ""
#    for i in list(range(0,length)):
#        outbuf += random.choice(charscope)
#    return outbuf

def generate_full256_string(length):
    return generate_string_in_range(length, 0, 256)

def generate_printable94_string(length):
    return generate_string_in_range(length, 32, 127)

def generate_string_in_range(length, lobound, hibound):
    return __generate_string(length, lobound, hibound, None)

def generate_string_in_charscope(length, charscope):
    return __generate_string(length, -1, -1, charscope)

def generate_character_in_range(lobound, hibound):
    return chr(random.randrange(lobound, hibound))

def generate_character_in_charscope(charscope):
    return random.choice(charscope)

def __generate_string(length, lobound, hibound, charscope):
    if charscope != None and charscope != "":
        if length > 1:
            return generate_character_in_charscope(charscope) + __generate_string(length - 1, -1, -1, charscope)
        elif length is 1:
            return generate_character_in_charscope(charscope)

    elif lobound >= 0 and hibound > 0:
        if length > 1:
            return generate_character_in_range(lobound, hibound) + __generate_string(length - 1, lobound, hibound, None)
        elif length is 1:
            return generate_character_in_range(lobound, hibound)
    
    raise Exception(__ERR_INVALID_PARAMETERS + " lobound=" + str(lobound) + " hibound=" + str(hibound) + " charscope=" + str(charscope))
    return None

def parse_args():
    ## Constructing argument parser
    parser = argparse.ArgumentParser(description="A handy tool to generate (pseudo-)random ASCII strings.")
    parser.add_argument("--charscope", required=False, type=str, help="List of characters to be chosen at random.") 
    parser.add_argument("--printable94", action='store_true', default=True, help="The charscope of all 94 key-combinations on a standard keyboard.") 
    parser.add_argument("--full256", action='store_true', help="The charscope of all 256 Extended ASCII characters.") 
    parser.add_argument("--length", required=False, type=int, default=8, help="Quantity of characters in generated string.")  
    parser.add_argument("--verbose", action="store_true", help="Display randstr debug output during runtime.")
    parser.add_argument("--version", action='version', version='randstr %s' % __version__)

    ## Process arguments
    args = parser.parse_args()

    ## Display program variables
    if args.verbose == True:
        print("randstr.py input arguments")
        print("\t--charscope \t"+str(args.charscope))
        print("\t--printable94 \t"+str(args.printable94))
        print("\t--full256 \t"+str(args.full256))
        print("\t--length \t"+str(args.length))
        print("\t--verbose \t"+str(args.verbose))
        print("")

    return(args.charscope, args.printable94, args.full256, args.length, args.verbose)

## Program execution start
if __name__ == "__main__":
    
    (charscope, printable94, full256, length, verbose) = parse_args()

    ## Validate parameters
    if charscope != None:
        assert printable94 != full256, "printable94 xor full256 must be selected!"

    print("Printable 94 [8]")
    print(generate_printable94_string(8))
    print()
    print("Full 256 [7]")
    print(generate_full256_string(7))
    print()
    print("Charscope abcd [6]")
    print(generate_string_in_charscope(6, "abcd"))
    print()
