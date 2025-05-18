import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]  # yield the age value only

    cursor.close()
    connection.close()

def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average}")
    else:
        print("No users found.")

