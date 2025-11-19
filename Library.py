import mysql.connector
from datetime import date

def connection():
    dbconnect = mysql.connector.connect(
        user='root',
        password='Tushar@7168',
        host='localhost',
        port=3306,
        database='Library'
    )
    print("Connection successfully")
    return dbconnect

db = connection()
cursor = db.cursor()

def Create_tables():
    cursor.execute("""
        create table if not exists Books (
            ISBN int primary key,
            title varchar(100),
            author varchar(100),
            quantity int,
            year_published year
        )
    """)
    cursor.execute("""
        create table if not exists Members (
            member_id int primary key,
            name varchar(50),
            email varchar(100) unique
        )
    """)
    cursor.execute("""
        create table if not exists BorrowedBooks (
            borrow_id int primary key,
            ISBN int,
            member_id int,
            borrow_date date,
            return_date date,
            foreign key(ISBN) references Books(ISBN),
            foreign key(member_id) references Members(member_id)
        )
    """)
    db.commit()

def Add_book(ISBN, title, author, quantity, year_published):
    cursor.execute("select * from Books where ISBN = %s", (ISBN,))
    if cursor.fetchone():
        print("Book with this ISBN already exists")
    else:
        cursor.execute("insert into Books (ISBN, title, author, quantity, year_published) values (%s, %s, %s, %s, %s)",
                       (ISBN, title, author, quantity, year_published))
        db.commit()
        print("Book Added Successfully")

def Remove_book(ISBN):
    cursor.execute("select * from Books where ISBN = %s", (ISBN,))
    if cursor.fetchone():
        cursor.execute("delete from Books where ISBN = %s", (ISBN,))
        db.commit()
        print("Book Removed Successfully")
    else:
        print("Book not found")

def Search_books(keyword):
    cursor.execute("select * from Books where title like %s or author like %s", 
                   (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if results:
        for i in results:
            print(f"{i}")
    else:
        print("No books found")

def Add_member(member_id, name, email):
    cursor.execute("select * from Members where member_id = %s", (member_id,))
    if cursor.fetchone():
        print("Member with this ID already exists")
    else:
        cursor.execute("insert into Members (member_id, name, email) values (%s, %s, %s)", 
                       (member_id, name, email))
        db.commit()
        print("Member Added Successfully")

def Remove_member(member_id):
    cursor.execute("select * from Members where member_id = %s", (member_id,))
    if cursor.fetchone():
        cursor.execute("delete from Members where member_id = %s", (member_id,))
        db.commit()
        print("Member Removed Successfully")
    else:
        print("Member not found!")

def Borrow_book(ISBN, member_id, borrow_id):
    cursor.execute("select quantity from Books where ISBN = %s", (ISBN,))
    book = cursor.fetchone()
    if not book:
        print("Book not found!")
        return
    if book[0] <= 0:
        print("Book is out of stock!")
        return

    cursor.execute("select * from Members where member_id = %s", (member_id,))
    if not cursor.fetchone():
        print("Member not found!")
        return

    cursor.execute("select * from BorrowedBooks where borrow_id = %s", (borrow_id,))
    if cursor.fetchone():
        print("Borrow ID already exists!")
        return

    borrow_date = date.today().strftime("%Y-%m-%d")
    cursor.execute("insert into BorrowedBooks(borrow_id, ISBN, member_id, borrow_date) values(%s, %s, %s, %s)",
                   (borrow_id, ISBN, member_id, borrow_date))
    cursor.execute("update Books set quantity = quantity - 1 where ISBN = %s", (ISBN,))
    db.commit()
    print("Book borrowed successfully")

def Return_book(ISBN, member_id):
    cursor.execute("select * from BorrowedBooks where ISBN = %s and member_id = %s and return_date is null", 
                   (ISBN, member_id))
    record = cursor.fetchone()
    if not record:
        print("No active borrow record found!")
        return

    return_date = date.today().strftime("%Y-%m-%d")
    cursor.execute("update BorrowedBooks set return_date = %s where member_id = %s and ISBN = %s and return_date is null",
                   (return_date, member_id, ISBN,))
    cursor.execute("update Books set quantity = quantity + 1 where ISBN = %s", (ISBN,))
    db.commit()
    print("Book Returned Successfully")

def List_borrowed_books():
    cursor.execute("select * from BorrowedBooks")
    results = cursor.fetchall()
    if results:
        for i in results:
            print(f"{i}")
    else:
        print("No books borrowed yet")

def List_available_books():
    cursor.execute("select * from Books where quantity > 0")
    results = cursor.fetchall()
    if results:
        for i in results:
            print(f"{i}")
    else:
        print("No available books!")

def Update_book(ISBN, new_title, new_author, new_quantity, new_year):
    cursor.execute("select * from Books where ISBN = %s", (ISBN,))
    if cursor.fetchone():
        cursor.execute("""
            update Books 
            set title = %s, author = %s, quantity = %s, year_published = %s
            where ISBN = %s
        """, (new_title, new_author, new_quantity, new_year, ISBN))
        db.commit()
        print("Book Details Updated Successfully")
    else:
        print("Book not found")

def main():
    Create_tables()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Books")
        print("4. Add Member")
        print("5. Remove Member")
        print("6. Borrow Book")
        print("7. Return Book")
        print("8. List Borrowed Books")
        print("9. List All Available Books")
        print("10. Update Book Details")
        print("11. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            ISBN = int(input("Enter ISBN: "))
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")
            quantity = int(input("Enter Book Quantity: "))
            year_published = int(input("Enter Year Published (YYYY): "))
            Add_book(ISBN, title, author, quantity, year_published)

        elif choice == "2":
            ISBN = int(input("Enter ISBN: "))
            Remove_book(ISBN)

        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            Search_books(keyword)

        elif choice == "4":
            member_id = int(input("Enter member id: "))
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            Add_member(member_id, name, email)

        elif choice == "5":
            member_id = int(input("Enter member id: "))
            Remove_member(member_id)

        elif choice == "6":
            borrow_id = int(input("Enter borrow id: "))
            ISBN = int(input("Enter ISBN: "))
            member_id = int(input("Enter member id: "))
            Borrow_book(ISBN, member_id, borrow_id)

        elif choice == "7":
            ISBN = int(input("Enter ISBN: "))
            member_id = int(input("Enter member id: "))
            Return_book(ISBN, member_id)

        elif choice == "8":
            List_borrowed_books()

        elif choice == "9":
            List_available_books()

        elif choice == "10":
            ISBN = int(input("Enter ISBN: "))
            new_title = input("Enter new title: ")
            new_author = input("Enter new author: ")
            new_quantity = int(input("Enter new quantity: "))
            new_year = int(input("Enter new year published (YYYY): "))
            Update_book(ISBN, new_title, new_author, new_quantity, new_year)

        elif choice == "11":
            break
        else:
            print("invalid choice try again.")

main()
