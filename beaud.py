#!python
import argparse
import re
import sys

beaud_rx = re.compile("[^beau -]")
morse_to_text = {
    ".-"    : "a",    "-..."  : "b",
    "-.-."  : "c",    "-.."   : "d",
    "."     : "e",    "..-."  : "f",
    "--."   : "g",    "...."  : "h",
    ".."    : "i",    ".---"  : "j",
    "-.-"   : "k",    ".-.."  : "l",
    "--"    : "m",    "-."    : "n",
    "---"   : "o",    ".--."  : "p",
    "--.-"  : "q",    ".-."   : "r",
    "..."   : "s",    "-"     : "t",
    "..-"   : "u",    "...-"  : "v",
    ".--"   : "w",    "-..-"  : "x",
    "-.--"  : "y",    "--.."  : "z",
    ".----" : "1",    "..---" : "2",
    "...--" : "3",    "....-" : "4",
    "....." : "5",    "-...." : "6",
    "--..." : "7",    "---.." : "8",
    "----." : "9",    "-----" : "0",
    "/"     : " ",
}
text_to_morse = {v: k for k, v in morse_to_text.items()}
text_to_morse["."] = ""
text_to_morse["-"] = ""

def main():
    """Main script function"""
    usage = "python beaud.py [-h] [-t|-f] [input_string] [input_string] ..."
    desc = "Convert text to/from morse beau'd."
    parser = argparse.ArgumentParser(usage=usage, description=desc)
    parser.add_argument("-t", "--to", dest="to_beaud", action="store_const", const=True, help="force conversion from normal text to beau'd")
    parser.add_argument("-f", "--from", dest="to_beaud", action="store_const", const=False, help="force conversion from beau'd to normal text")
    parser.add_argument("-d", "--delim", dest="d", default="-", help="string to delimit beaud characters with; default '-'")
    parser.add_argument("-", "--use-stdin", dest="use_stdin", action="store_true", help="read input strings from STDIN")
    args, input_strs = parser.parse_known_args()
    for s in input_strs:
        print(parse_string(s, args.to_beaud, hyphen=args.d))
    if args.use_stdin:
        for line in sys.stdin:
            print(parse_string(line, args.to_beaud, hyphen=args.d))

def test_input(s):
    """Tests whether or not a string 'looks like' morse beaud"""
    if re.match(beaud_rx, s) is None:
        return False
    return True

def parse_string(s, to_from=None, hyphen="-"):
    """Parses a single string to/from morse beaud"""
    if to_from is None:
        to_from = test_input(s)
    if to_from:
        return to_beaud(to_morse(s), hyphen=hyphen)
    else:
        return from_morse(from_beaud(s, hyphen=hyphen))

def to_morse(s):
    """Translate from text to morse"""
    mlookup = lambda c: text_to_morse[c] if c in text_to_morse else c
    return " ".join([mlookup(c) for c in s.lower()])

def to_beaud(s, hyphen="-"):
    """Translate from morse to beaud"""
    r = s.replace("-", "beau"+hyphen)   \
        .replace(".", "be"+hyphen)      \
        .replace("/", "")               \
        .replace(hyphen+" ", " ")
    return re.sub(hyphen+"$", "", r)

def from_beaud(s, hyphen="-"):
    """Translate from beaud to morse"""
    return s.lower()            \
        .replace(hyphen, "")    \
        .replace("beau", "-")   \
        .replace("be", ".")     \

def from_morse(s):
    """Translate from morse to text"""
    tlookup = lambda w: morse_to_text[w] if w in morse_to_text else w
    words = s.replace("  ", " / ").split(" ")
    return "".join([tlookup(w) for w in words])

if __name__=="__main__":
    main()
