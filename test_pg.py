import psycopg2

passwords = ["1234", "postgres", "admin", "password", "root", "12345", "123456", ""]
success = False
for pwd in passwords:
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password=pwd, host="localhost", port=5432)
        print(f"SUCCESS_PASSWORD={pwd}")
        conn.close()
        success = True
        break
    except Exception as e:
        pass

if not success:
    print("ALL_FAILED")
