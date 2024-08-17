from decouple import config
import psycopg2


class DbConnector:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            # Load environment variables
            postgres_host = config("POSTGRES_HOST", "db")
            print("Wha is the host :", [postgres_host])
            postgres_port = config("POSTGRES_PORT", 5432)
            postgres_user = config("POSTGRES_USER", "admin")
            postgres_password = config("POSTGRES_PASSWORD", "admin")
            postgres_db = config("POSTGRES_DB", "dbt-anime")

            # Construct the connection string
            connection_string = f"dbname={postgres_db} user={postgres_user} password={postgres_password} host={postgres_host} port={postgres_port}"

            # Establish a connection
            self.connection = psycopg2.connect(connection_string)
            print("Connection to the database successful!")

        except psycopg2.Error as e:
            print("Unable to connect to the database.")
            print(e)

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Error: Database connection not established.")
            return None

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result

            except psycopg2.Error as e:
                print(f"Error executing query: {query}")
                print(e)
                return None

    def save(self):
        if self.connection:
            self.connection.commit()
            print("Transaction committed.")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
