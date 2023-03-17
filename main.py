import xlrd
import pandas
import sys

def echo(phrase: str) -> None:
   """A dummy wrapper around print."""
   # for demonstration purposes, you can imagine that there is some
   # valuable and reusable logic inside this function
   print(phrase)
   print("annotation : "+ echo.__annotations__['phrase'])

def main() -> int:
    df = pandas.read_excel("/home/gv/Téléchargements/export_17_03_2023_20_00_12.xls")
    echo("Columns")
    echo(df.columns)
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit

