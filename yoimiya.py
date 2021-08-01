#/usr/bin/env python3

import os
import argparse
import random
import string

from src.logs import LOGS

class SETTINGS:
    def __init__(self):
        self.comments = False
        self.oneline = False
        self.sleep = False
        self.rename = False

        self.exceptions = {
            "operators" : [
                ";",
                ":",
                "=",
                "+",
                "-",
                "*",
                "%",
                "^",
                "<",
                ">",
                "|",
                "/",
                ",",
                "{",
                "}",
                "[",
                "]",
                "\n"
            ]
        }

class YOIMIA:
    def __init__(self):
        self.settings = SETTINGS()
        self.logs = LOGS()
        self.path = None
        self.line = None
        self.sizes = [256, 256]
        self.content = []
        self.obfuscated = []
        self.renamed = {}
        self.sleep_line = "sleep(0)"
        if (self.arguments() == True):
            self.load()
            self.obfuscate()
            self.dump()

    def arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", action = "store", help = "File to obfuscate", default = None, required = True)
        parser.add_argument("-o", "--oneline", action = "store_true", help = "Remove all new line", default = False, required = False)
        parser.add_argument("-s", "--sleep", action = "store_true", help = "Add useless sleep 0", default = False, required = False)
        parser.add_argument("-c", "--comments", action = "store_true", help = "Remove comments", default = False, required = False)
        parser.add_argument("-r", "--rename", action = "store_true", help = "Rename variables", default = False, required = False)
        args = parser.parse_args()
        self.path = args.file
        self.settings.oneline = args.oneline
        self.settings.sleep = args.sleep
        self.settings.comments = args.comments
        self.settings.rename = args.rename
        
        if (self.path == None):
            return (False)
        return (True)

    def check(self):
        if (os.path.isfile(self.path) == True):
            return (True)
        self.logs.fail("Error: '{}' not found".format(self.path))
        return (False)

    def load(self):
        if (self.check() == True):
            with open(self.path, 'r') as f:
                for line in f:
                    self.content.append(line)
            f.close()
            self.logs.ok("content loaded")

    def generate_name(self):
        characters = string.ascii_letters
        size = random.randint(self.sizes[0], self.sizes[1])
        name = ''.join(random.choice(characters) for i in range(size))
        
        return (name)

    def oneline(self):
        valid = True
        previous = None

        if (self.settings.oneline == True and '\n' in self.line):
            for element in self.settings.exceptions["operators"]:
                self.line = self.line.rstrip('\n')
                if (self.line.endswith(element) == True):
                    valid = False
            if (valid == True):
                self.line += ';'
            if (len(self.obfuscated) > 0):
                previous = self.obfuscated[len(self.obfuscated) - 1]
                self.line = self.line.lstrip()
            self.logs.item_method("onlined")

    def comment(self):
        if (self.settings.comments == True):
            if (self.line.startswith('#') == True or self.line.lstrip().startswith('#') == True):
                self.line = None
                self.logs.item_method("comments")

    def check_exceptions(self, data):
        inside = False
    
        for element in self.settings.exceptions["operators"]:
            if (element in data):
                inside = True
        try:
            getattr(__import__("builtins"), data)(1)
            inside = True
        except Exception as e:
            if (inside != True):
                inside = False

        return (inside)

    def special(self, c):
        specials = string.punctuation + " "
        
        if (c in specials):
            return (True)
        return (False)

    def vault(self, name, value):
        if (name in self.renamed.keys()):
            return (False)
        self.renamed[name] = value
        return (True)

    def rename_variable(self, line):
        renamed = False
        name = ""

        for i, character in enumerate(line):
            if (self.special(character) == True or self.check_exceptions(name) == True):
                name = ""
            else:
                name += character
                if (i < (len(line) - 1)):
                    if (self.check_exceptions(line[i + 1]) == True):
                        self.vault(name, self.generate_name())
                        renamed = True
                else:
                    if (len(name) > 1 and self.check_exceptions(name) == False):
                        self.vault(name, self.generate_name())
                        renamed = True
        if (renamed == True):
            self.logs.item_method("rename variables")

    def rename(self):
        if (self.settings.rename == True):
            self.rename_variable(self.line.lstrip())
            
    def obfuscate(self):
        self.logs.ok("variables sizes:\n\t{}\n\t{}".format(self.sizes[0], self.sizes[1]))
        self.logs.load("Obfuscating...")
        for i, line in enumerate(self.content):
            self.logs.item_load("line: {}".format(i))
            if (len(line) > 1):
                self.line = line
                if (self.line.startswith('#') == False and (line.startswith(' ') == True or line.startswith('\t') == True or line.endswith(":\n") == True)):
                    self.oneline()
                else:
                    self.obfuscated.append('\n')
                self.rename()
                self.comment()
                self.logs.item("obfuscated".format(i))
                if (self.line != None):
                    self.obfuscated.append(self.line)
            else:
                self.logs.empty_item("not obfuscated".format(i))
        for i, data in enumerate(self.renamed):
            if (data.isnumeric() == True):
                self.obfuscated.insert(0, "{} = {}\n".format(self.renamed[data], data))
            else:
                self.obfuscated.insert(0, "{} = \"{}\"\n".format(self.renamed[data], data))
            for index, element in enumerate(self.obfuscated):
                if (index > i):
                    self.obfuscated[index] = element.replace(data, self.renamed[data])

        self.logs.load("Obfuscated")

    def dump(self):
        with open("{}".format(self.path.replace(".py", "_yoimiya.py")), 'w+') as f:
            for line in self.obfuscated:
                f.write(line)
        f.close()

if (__name__ == "__main__"):
    YOIMIA()
