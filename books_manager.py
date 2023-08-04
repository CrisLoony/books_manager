import psycopg2

dbname = "postgres"
user = "postgres"
password = "987456321"
host = "localhost" 
port = "5432" 

conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
cursor = conn.cursor()

# Creating table 'books'
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    pages INTEGER,
                    company TEXT,
                    release INTEGER
                 )''')

# Defining functions


def verify_answer(options: list, answer: str):
    if answer not in options:
        return False
    return True


def continue_navigating(answer):
    yes = ["y", "ye", "yes"]
    no = ["n", "no", "not"]

    if answer in yes:
        return True
    return False


def register_book(title, author, pages, company, release):
    title = title.replace("'", "\'")
    data = {"title": title,
            "author": author,
            "pages": pages,
            "company": company,
            "release": release}

    insert_query = (
        "INSERT INTO books (title, author, pages, company, release) "
        "VALUES (%(title)s, %(author)s, %(pages)s, %(company)s, %(release)s)"
    )
    cursor.execute(insert_query, data)
    conn.commit()

options = ["1", "2", "3"]
access_type = None
manager_action = None

print("+" * 30)
print(f"|{'Python Library':^29}|")
print("+" * 30)

while True:
    print("What you want to do?")
    print("[1] Manage books")
    print("[2] See the collection")
    print("[3] Search for a book")
    answer = input("-> ").strip()
    print()

    if verify_answer(options, answer):
        if answer == "1":
            access_type = "manage"
        elif answer == "2":
            access_type = "collection"
        else:
            access_type = "search"

    if access_type == "manage":
        print("Choose an option:")
        print("[1] Register new book")
        print("[2] Delete book")
        answer = input("-> ").strip()
        print()

        options = ["1", "2"]
        if verify_answer(options, answer):
            if answer == "1":
                manager_action = 'register'
            else:
                manager_action = 'delete'

        if manager_action == 'register':
            print("On the next steps you're going to fill some information about the book you want to register. Let's go!")
            title = input("Title: ").title().strip()
            author = input("Author: ").title().strip()
            pages = input("How many pages: ").strip()
            publishing_company = input("Publishing Company: ").title().strip()
            release_year = input("Release Year: ").strip()

            while True:
                try:
                    pages = int(pages)
                    release_year = int(release_year)
                    break
                except:
                    print(
                        "The number of pages and the release year inserteds aren't valid, please try again.")
                    pages = input("How many pages: ").strip()
                    release_year = input("Release Year: ").strip()
                    continue

            register_book(title, author, pages,
                          publishing_company, release_year)
            print(f"The book '{title}' was added to the collection!")

        else:  
            title_to_delete = input(
                "What title you want to delete? ").title().strip()
            query = "SELECT * FROM books WHERE title = (%s)"
            cursor.execute(query, (title_to_delete,))
            row = cursor.fetchall()

            if not row:
                print("We can't find any book with this title.")
            else:
                for collumn in row:
                    titl_to_delete = collumn[1]
                    author_to_delete = collumn[2]
                    pages_to_delete = collumn[3]
                    company_to_delete = collumn[4]
                    release_to_delete = collumn[5]

                    print(
                        f"Title: {titl_to_delete}\nAuthor: {author_to_delete}\nPages: {pages_to_delete}\nPublishing Company: {company_to_delete}\nRelease Year: {release_to_delete}")
                    print('-' * 30)

                confirm = input("Do you have sure you want to delete [y/n]? ")
                if continue_navigating(confirm):
                    delete_query = "DELETE FROM books WHERE title = (%s)"
                    cursor.execute(delete_query, (titl_to_delete,))
                    conn.commit()
                    print("The book was deleted successfully!")
                else:
                    print("Deletion has been canceled.")

    elif access_type == "collection":
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        print('-' * 30)
        if not rows:
            print("We don't have any book in our collection.")
        else:
            for row in rows:
                title_db = row[1]
                author_db = row[2]
                pages_db = row[3]
                company_db = row[4]
                release_db = row[5]

                print(
                    f"Title: {title_db}\nAuthor: {author_db}\nPages: {pages_db}\nPublishing Company: {company_db}\nRelease Year: {release_db}")
                print('-' * 30)

    else: 
        search_term = input("Insert the keyword? ").title()
        query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR company LIKE %s"
        cursor.execute(query, ('%' + search_term + '%', '%' +
                       search_term + '%', '%' + search_term + '%'))
        search_rows = cursor.fetchall()

        print("The result of you search is: ")
        if not search_rows:
            print("We can't find anything like this in our collection.")
        else:
            print('-' * 30)
            for search_row in search_rows:
                searched_title = search_row[1]
                searched_author = search_row[2]
                searched_pages = search_row[3]
                searched_company = search_row[4]
                searched_release = search_row[5]

                print(
                    f"Title: {searched_title}\nAuthor: {searched_author}\nPages: {searched_pages}\nPublishing Company: {searched_company}\nRelease Year: {searched_release}")
                print('-' * 30)

    answer = input("Do you want to keep navigating [y/n]? ").lower().strip()
    if continue_navigating(answer):
        access_type = None
        continue
    else:
        conn.close()
        print('Thanks for the preference!')
        break
