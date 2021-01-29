from src.method_registrator import MethodRegistrator
from typing import List
import sys

# První musí zůstat prázdný!
# Jméno registrované metody,
# První parametr pro metodu
DEBUG_SYS_ARGV: List[str] = [
    " ",                
    "trade",
]

DEBUG: bool = True

if __name__ == "__main__":
    print("test Volume")
    args: List[str] = DEBUG_SYS_ARGV if DEBUG else sys.argv
    if DEBUG: 
        print("YOU ARE IN DEBUG ARGS MODE")

    met_reg = MethodRegistrator(arguments=args)
    met_reg.run()


