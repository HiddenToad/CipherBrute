import re
import json
import os
from os.path import isfile, basename

words = open("./words_alpha.txt", "r").read()
key_lbls = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class BruteKey:
    def read_command(self):
        command = input("?> ")
        match command:
            case "help":
                print("List of commands:\nshowkey: shows the current cipher key.\n\ls: displays all saved tables\nclaimed: views characters found with certainty\nload: loads a saved table by name\nsave: saves a loaded table\nunload: saves, and then unloads current table\nfunload: unloads current table without saving\nquit: saves and exits\nfquit: exits without saving\nupdate: allows updating data in table")

            case "showkey":
                print(self.key)
            
            case "ls":
                self.display_tables()

            case "unload":
                self.save_key()
                self.clean()

            case "funload":
                self.clean()

            case "load":
                self.load_key()

            case "save":
                self.save_key()

            case "quit":
                self.save_key()
                exit(0)

            case "fquit":
                exit(0)
            
            case "update":
                self.update_from_input()
            
            case "claimed":
                print("Found chrs: ", sorted(self.claimed_chrs))

            case _:
                print("command not recognized. try typing 'help' for a list of commands.")


    def clean(self):
        [self.key.update({c: None}) for c in key_lbls]

    

    def update_from_input(self):
        pat = input("Enter pattern coded according to symbol key (alphabetic): ")
        if not pat.isalpha() or not pat.isupper():
            print("String must be composed of alphabetic uppercase characters.")
            return
        self.update_with_pattern(pat)
  

    def update_claimed_chrs(self):
        for key_n in key_lbls:
            if self.key[key_n] == None:
                continue
            if len(self.key[key_n]) == 1:
                if not self.key[key_n][0] in self.claimed_chrs:
                    self.claimed_chrs.append(self.key[key_n][0])
            else:
                self.key[key_n] = [l for l in self.key[key_n] if not l in self.claimed_chrs]


    def update_with_pattern(self, pat):
        
        regex = r"\b"
        chrs_done = []
        plen = len(pat)
        for c in pat:
            if c in chrs_done:
                pos = chrs_done.index(c) + 1
                regex += f"(\\{pos})"
            else:
                if self.key[c] == None:
                    neg_pos = [str(pat.index(ch) + 1) for ch in chrs_done if ch != c]
                    lookahead = "((?!\\"
                    suffix = r").)"
                    clause = "|\\".join(neg_pos)

                    expr = f"{lookahead}{clause}{suffix}"
                   # print(expr)
                    if len(neg_pos) == 0:
                        regex += "(\\w)"
                    else:
                        regex += expr
                else:
                    possible_chrs = "".join(self.key[c])
                    regex += f"([{possible_chrs}])"
            chrs_done.append(c)
        regex += "\n"
        #print(regex)
        regex = re.compile(regex)
        matching_words = [m[0].strip() for m in regex.finditer(words)]
        
        print(matching_words)


        updated = []
        for i in range(0, plen):
            key_n = pat[i]
            if key_n in updated:
                continue
            
            idx = lambda s: s[i]

            unique_poss_letters = list(set(map(idx, matching_words)))
            if self.key[key_n] == None:
                self.key[key_n] = unique_poss_letters
            else:
                prev_letters = self.key[key_n]
                overlap = [l for l in unique_poss_letters if l in prev_letters]
                self.key[key_n] = overlap

            
                
            updated.append(key_n)
        self.update_claimed_chrs()
        self.update_claimed_chrs()
        #print(self.key)
        #print("Found chrs: ", sorted(self.claimed_chrs))
        

    
    def display_tables(self):
        files = [basename(f) for f in os.listdir() if isfile(f)]
        tables = [f for f in files if "_tbl.json" in f]
        print("Available table names:\n")
        for f in tables:
            print(f.removesuffix("_tbl.json"))

    def save_key(self):
        name = input("Enter a name for this table: ")

        try:
            file = open(name + "_tbl.json", "x+")
            serialized = json.dumps(self.key)
            file.write(serialized)
        except FileExistsError:
            file = open(name + "_tbl.json", "w")
            serialized = json.dumps(self.key)
            file.write(serialized)

    def load_key(self):
        name = input("Enter the name of the table you wish to load: ")

        try:
            f = open(name + "_tbl.json", "r")
            self.key = json.loads(f.read())
        except:
            print("Could not load table. Check the name!")
            return
        
        print("Table successfully loaded.")
        self.update_claimed_chrs()
        self.update_claimed_chrs()

    
    def __init__(self):
        self.key = {}
        self.claimed_chrs = []
        self.clean()
        


def main():
    optometrist = "ABCADECFGHC"
    please = "ABCDEC"
    key = BruteKey()
    while(True):
        key.read_command()
    

main()