"""Small, resettable in-memory SQLite lab for the COMP0178 notebooks."""
import sqlite3

SCHEMA = """
CREATE TABLE Branch(branchNo TEXT PRIMARY KEY, street TEXT, city TEXT);
CREATE TABLE Staff(staffNo TEXT PRIMARY KEY, fName TEXT NOT NULL,
 lName TEXT NOT NULL, position TEXT, salary NUMERIC CHECK(salary >= 0),
 branchNo TEXT REFERENCES Branch(branchNo));
CREATE TABLE Client(clientNo TEXT PRIMARY KEY, fName TEXT, lName TEXT);
CREATE TABLE Property(propertyNo TEXT PRIMARY KEY, street TEXT, city TEXT,
 type TEXT, rooms INTEGER, rent NUMERIC, staffNo TEXT REFERENCES Staff(staffNo));
CREATE TABLE Viewing(clientNo TEXT REFERENCES Client(clientNo),
 propertyNo TEXT REFERENCES Property(propertyNo), viewDate TEXT, comment TEXT,
 PRIMARY KEY(clientNo,propertyNo,viewDate));
INSERT INTO Branch VALUES
 ('B001','1 Main St','London'),('B002','2 High St','Glasgow'),('B003','3 Park St','Bristol');
INSERT INTO Staff VALUES
 ('S001','Ada','Lee','Manager',30000,'B001'),
 ('S002','Ben','Patel','Assistant',18000,'B001'),
 ('S003','Cara','Jones','Manager',24000,'B002'),
 ('S004','Dan','Wu','Assistant',NULL,'B002'),
 ('S005','Eve','Smith','Supervisor',20000,'B002');
INSERT INTO Client VALUES ('C001','Mia','Green'),('C002','Noah','Brown'),('C003','Zoe','White');
INSERT INTO Property VALUES
 ('P001','10 Dawn Rd','London','Flat',2,1200,'S001'),
 ('P002','20 Park Rd','London','House',3,1800,'S002'),
 ('P003','30 Main St','Glasgow','Flat',1,700,'S003'),
 ('P004','40 Park St','Glasgow','House',4,1400,'S005');
INSERT INTO Viewing VALUES
 ('C001','P001','2024-05-01',NULL),('C001','P002','2024-05-02','Nice'),
 ('C002','P002','2024-05-03','Too expensive'),('C002','P004','2024-05-04',NULL);
"""

class Practice:
    def __init__(self):
        self.connection = None
        self.reset()

    def reset(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.executescript(SCHEMA)
        self.last_rows = None
        self.last_columns = None
        print('Fresh practice database: Branch 3, Staff 5, Client 3, Property 4, Viewing 4 rows.')

    def run(self, sql, display=True):
        # One statement per cell keeps results and feedback unambiguous.
        if not any(line.strip() and not line.lstrip().startswith('--') for line in sql.splitlines()):
            self.last_rows = None
            self.last_columns = None
            if display:
                print('Write your SQL below the comments, then run this cell.')
            return
        try:
            cursor = self.connection.execute(sql)
            if cursor.description:
                self.last_columns = [column[0] for column in cursor.description]
                self.last_rows = cursor.fetchall()
                if display:
                    from IPython.display import display as show, HTML
                    from html import escape
                    headers = ''.join('<th>'+escape(x)+'</th>' for x in self.last_columns)
                    rows = ''.join('<tr>'+''.join('<td>'+escape('NULL' if x is None else str(x))+'</td>' for x in row)+'</tr>' for row in self.last_rows)
                    show(HTML('<table><thead><tr>'+headers+'</tr></thead><tbody>'+rows+'</tbody></table>'))
                    print(f'{len(self.last_rows)} row(s)')
            else:
                self.last_rows = self.last_columns = None
                if display:
                    print(f'Statement completed; affected rows: {cursor.rowcount}.')
        except sqlite3.Error as error:
            self.last_rows = self.last_columns = None
            if display:
                print(f'SQL error: {error}')
            else:
                raise

    def check(self, expected, ordered=False):
        if self.last_rows is None:
            print('Run your answer SQL cell immediately before this check.')
            return
        actual = self.last_rows
        match = actual == expected if ordered else sorted(actual, key=repr) == sorted(expected, key=repr)
        print('Correct result for this dataset.' if match else 'Not yet: compare columns, row count, duplicates, NULL handling, and requested order.')
        print('This checks results on the sample data, not correctness on every possible database.')

    def register(self, shell):
        if shell is None:
            raise RuntimeError('Use a Jupyter Python kernel to run %%sql cells.')
        def sql_magic(line, cell):
            if line.strip():
                raise ValueError('Put the SQL statement in the cell body, not the %%sql line.')
            self.run(cell)
        shell.register_magic_function(sql_magic, magic_kind='cell', magic_name='sql')
        print('%%sql ready. One SQL statement per code cell. Run lab.reset() to restore the sample data.')
