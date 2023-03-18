import xlrd
import pandas as pd
import sys
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from enum import Enum

class TypeCompte(Enum):
    COMPTE_CHEQUE_00000322951 = 1
    LIVRET_A_00030209039 = 2
    CREDIT_IMMOBILIER_00060856774 = 3
def importToInfluxdb():
    org = "carignan"
    token = "2zhGO0LoXJYG9ngjaGyHmGzU9EOgfPFb2MZaGtlGcwKcNRZC7aKnx0PNY69sFLrPn0kRzT5YRdsGFeksquq6sQ=="
    # Store the URL of your InfluxDB instance
    url = "https://influxdb.mypersonalstats.duckdns.org/"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return write_api


def deleteBucket():
    org = "carignan"
    token = "2zhGO0LoXJYG9ngjaGyHmGzU9EOgfPFb2MZaGtlGcwKcNRZC7aKnx0PNY69sFLrPn0kRzT5YRdsGFeksquq6sQ=="
    # Store the URL of your InfluxDB instance
    url = "https://influxdb.mypersonalstats.duckdns.org/"
    bucket = "sandbox"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    delete_api = client.delete_api()
    delete_api.delete(start="2000-01-01T00:00:00Z",stop="2030-01-01T00:00:00Z", predicate="",bucket=bucket)



def readXlsFile(file: str, write_api) -> None:
    bucket = "sandbox"
    org = "carignan"

    myBook = xlrd.open_workbook(file)

    mySheet = myBook.sheet_by_index(0)

    # Recherche du type de compte
    strTypeCompte = mySheet.cell_value(0, 0)


    if (strTypeCompte.count("00000322951")>0):
        typeCompte = TypeCompte.COMPTE_CHEQUE_00000322951
    elif (strTypeCompte.count("00030209039")>0):
        typeCompte = TypeCompte.LIVRET_A_00030209039
    elif (strTypeCompte.count("0060856774")>0):
        typeCompte = TypeCompte.CREDIT_IMMOBILIER_00060856774

    print("- type de compte : ", typeCompte)

    for i in range(mySheet.nrows):
        firstCell = mySheet.cell_value(i, 0)

        try:
            d = datetime.strptime(firstCell, '%d-%m-%Y')
            # print("time :", d.isoformat())

            p = influxdb_client\
            .Point("operation") \
            .tag("typeCompte", typeCompte.name)\
            .field("montant", mySheet.cell_value(i, 4) )\
            .time(d.isoformat()) \

            write_api.write(bucket=bucket, org=org, record=p)
        except ValueError as err:
            e = 5
            # print(err)


    # print("type : ", type(d))
    # print("date :", d)


    # df = pd.read_excel
    # print("dataframe :")
    # print(df.columns.values.tolist())

    # print(df.head(10))


def main() -> int:
    deleteBucket()

    write_api = importToInfluxdb()
    readXlsFile("/home/gv/Téléchargements/Compte_de_chèques_00000322951.xls", write_api)
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
