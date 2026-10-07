def connect_to_database(
    host: str, port: int, db_name: str, db_con_uri: str, *args, **kwargs
) -> list[str]:
    # Connect to the DB
    connection: list[str] = []
    print("Connecting to ", host, "on port:", port)
    return connection


def some_other_fun(y, a, b, c):
    y("33.45.66.112", "5432", "appdb", "postgres://appdb")
    return None


# x = connect_to_database
# x("33.45.66.112", "5432", "appdb", "postgres://appdb")

# some_other_fun(connect_to_database, 1, 2, 3)

# list_of_names = ["Mr.A", "Mr.B", connect_to_database, connect_to_database, "Mr.Z"]
# list_of_names[2]("33.45.66.112", "5432", "appdb", "postgres://appdb")
