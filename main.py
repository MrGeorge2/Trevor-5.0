from src.method_registrator import MethodRegistrator

from src.api_handler.api_handler import ApiHandler
import sys


if __name__ =="__main__":
    met_reg = MethodRegistrator(arguments=sys.argv)
    met_reg.run()


