import sys
import ast
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give the input file name to read.")
        print('Example: python read.py "2017-07-31 05:15:39.356754.txt"')
    else:
        filename = sys.argv[1]
        with open(filename, "r") as f:
            """Here is the example code to read the output file.
            The first line is the comment.
            The second line is a dictionary storing all attribute names and values.
            To read it, use "ast.literal_eval"
            """
            
            dic_str = f.readline()
            dic = ast.literal_eval(dic_str)
            pprint(dic)
            # Uncomment if you want to export the pretty printed dictionary to a file
#            with open("1" + sys.argv[1], "w+") as f:
#                pprint(dic, stream=f)
