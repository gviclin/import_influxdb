import xlrd
import pandas as pd
import sys
from datetime import datetime


def main() -> int:
    myBook = xlrd.open_workbook("/home/gv/Téléchargements/export_17_03_2023_20_00_12.xls")

    mySheet = myBook.sheet_by_index(0)

    da = mySheet.cell_value(5, 0)
    print("date :", da)

    d = datetime.strptime(da, '%d-%m-%Y')
    print ("type : ",type(d))
    print("date :", d)
    # df = pd.read_excel
    # print("dataframe :")
    # print(df.columns.values.tolist())

    # print(df.head(10))
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
