import pyodbc
from django.conf import settings



def stproc(query,params=None):
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    connection_string = (
        f"DRIVER={settings.DATABASES['mssql']['DRIVER']};"
        f"SERVER={settings.DATABASES['mssql']['SERVER']};"
        f"DATABASE={settings.DATABASES['mssql']['DATABASE']};"
        f"Trusted_Connection={settings.DATABASES['mssql']['Trusted_Connection']};"
    )
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute(query,params or [])


def execute_query(query, params=None):
    connection_string = (
        f"DRIVER={settings.DATABASES['mssql']['DRIVER']};"
        f"SERVER={settings.DATABASES['mssql']['SERVER']};"
        f"DATABASE={settings.DATABASES['mssql']['DATABASE']};"
        f"Trusted_Connection={settings.DATABASES['mssql']['Trusted_Connection']};"
    )
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()


def getdata(query, params=None):
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    connection_string = (
        f"DRIVER={settings.DATABASES['mssql']['DRIVER']};"
        f"SERVER={settings.DATABASES['mssql']['SERVER']};"
        f"DATABASE={settings.DATABASES['mssql']['DATABASE']};"
        f"Trusted_Connection={settings.DATABASES['mssql']['Trusted_Connection']};"
    )

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            if len(columns) == 1 and len(rows) == 1:
                return rows[0][0]
            return [dict(zip(columns, row)) for row in rows]

    except pyodbc.Error as e:
        raise ValueError(f"Error executing query: {str(e)}")