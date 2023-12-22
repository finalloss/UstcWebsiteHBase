import csv
import happybase
import secrets

class csv2hbase:
    def __init__(self, port, csv_path) -> None:
        self.port = port
        self.csv_path = csv_path
        self.conn = happybase.Connection(port=port)

    def migrate(self):
        with open(self.csv_path, encoding="utf-8") as csvfile:
            self.conn.open()
            table = self.conn.table("resource")
            reader = csv.reader(csvfile)
            for title, link, date in reader:
                table.put(
                    row=(title[:4] + secrets.token_hex(5)).encode(),
                    data={
                        "info:title".encode():title.encode(),
                        "info:link".encode(): link.encode(),
                        "info:date".encode(): date.encode(),
                    },
                )
            self.conn.close()

csv2hbaser = csv2hbase(9090, "../data/file_list.csv")
csv2hbaser.migrate()
