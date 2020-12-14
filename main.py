from src.method_registrator import MethodRegistrator
from typing import List
import sys


DEBUG_SYS_ARGV: List[str] = [
    " ",                # První musí zůstat prázdný!
    "ApiHandler",     # Jméno registrované metody,
                        # První parametr pro metodu
]

DEBUG: bool = True

if __name__ =="__main__":
    args: List[str] = DEBUG_SYS_ARGV if DEBUG else sys.argv
    if DEBUG: 
        print("YOU ARE IN DEBUG ARGS MODE")

    met_reg = MethodRegistrator(arguments=args)
    met_reg.run()


