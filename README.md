# Yoimiya
Python Obfuscator

### Usage
```
usage: yoimiya.py [-h] -f FILE [-o] [-s] [-c] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to obfuscate
  -o, --oneline         Remove all new line
  -s, --sleep           Add useless sleep 0 => in progress
  -c, --comments        Remove comments
  -r, --rename          Rename variables
```

### Example
```
python3 yoimiya.py -f test/test_0.py

==> content loaded
==> variables sizes:
        256
        256
:: Obfuscating...
        line: 0
        obfuscated
        line: 1
        obfuscated
        line: 2
        obfuscated
        line: 3
        obfuscated
        line: 4
        not obfuscated
        line: 5
        obfuscated
:: Obfuscated
```