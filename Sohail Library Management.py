import datetime # Import datetime for handling dates

class Book:
    def __init__(self, title, author, isbn, location="Shelf A"): 
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
        self.borrowed_by = None 
        self.location = location
        self.due_date = None 

    def __str__(self):
        status = 'Available'
        if self.is_borrowed:
            status = f'Borrowed by Member ID {self.borrowed_by}'
            if self.due_date:
                status += f' (Due: {self.due_date.strftime("%Y-%m-%d")})'
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}, Location: {self.location}) - {status}"

class Member: 
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = [] 

    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}"

class Library:
    def __init__(self):
        self.books = {}
        self.next_book_id = 1
        self.members = {} 
        self.next_member_id = 1

    def add_book(self, title, author, isbn, location="Shelf A"): 
        book = Book(title, author, isbn, location)
        self.books[self.next_book_id] = book
        print(f"\n[Success] Book added: {book.title} (ID: {self.next_book_id}, Location: {book.location})")
        self.next_book_id += 1

    def remove_book(self, book_id):
        if book_id not in self.books:
            print(f"\n[Error] Book with ID {book_id} not found.")
            return

        if self.books[book_id].is_borrowed:
            print(f"\n[Error] Cannot remove Book ID {book_id} as it is currently borrowed by Member ID {self.books[book_id].borrowed_by}.")
            return

        del self.books[book_id]
        print(f"\n[Success] Book with ID {book_id} removed.")

    def add_member(self, name): 
        member = Member(name, self.next_member_id)
        self.members[self.next_member_id] = member
        print(f"\n[Success] Member added: {member.name} (ID: {self.next_member_id})")
        self.next_member_id += 1

    def remove_member(self, member_id):
        if member_id not in self.members:
            print(f"\n[Error] Member with ID {member_id} not found.")
            return

        if self.members[member_id].borrowed_books:
            print(f"\n[Error] Cannot remove Member ID {member_id} as they still have borrowed books.")
            return

        del self.members[member_id]
        print(f"\n[Success] Member with ID {member_id} removed.")

    def borrow_book(self, book_id, member_id, days_to_borrow=7): 
        if book_id not in self.books:
            print(f"\n[Error] Book with ID {book_id} not found.")
            return
        if member_id not in self.members:
            print(f"\n[Error] Member with ID {member_id} not found.")
            return

        book = self.books[book_id]
        member = self.members[member_id]

        if not book.is_borrowed:
            book.is_borrowed = True
            book.borrowed_by = member_id
            book.due_date = datetime.date.today() + datetime.timedelta(days=days_to_borrow) 
            member.borrowed_books.append(book_id)
            print(f"\n[Success] '{book.title}' borrowed by {member.name} successfully. Due date: {book.due_date.strftime('%Y-%m-%d')}")
        else:
            print(f"\n[Error] '{book.title}' is already borrowed by Member ID {book.borrowed_by}.")

    def calculate_fine(self, book_id):
        if book_id not in self.books:
            return 0.0

        book = self.books[book_id]
        if not book.is_borrowed or book.due_date is None:
            return 0.0 

        today = datetime.date.today()
        if today > book.due_date:
            overdue_days = (today - book.due_date).days
            fine_per_day = 0.50 
            fine = overdue_days * fine_per_day
            return fine
        else:
            return 0.0

    def return_book(self, book_id):
        if book_id not in self.books:
            print(f"\n[Error] Book with ID {book_id} not found.")
            return

        book = self.books[book_id]

        if book.is_borrowed:
            fine = self.calculate_fine(book_id) 
            if fine > 0:
                print(f"\n[Fine Alert] Fine for '{book.title}': ${fine:.2f}")

            borrowing_member_id = book.borrowed_by
            if borrowing_member_id is not None and borrowing_member_id in self.members:
                member = self.members[borrowing_member_id]
                if book_id in member.borrowed_books:
                    member.borrowed_books.remove(book_id)

            book.is_borrowed = False
            book.borrowed_by = None
            book.due_date = None 
            print(f"\n[Success] '{book.title}' returned successfully.")
        else:
            print(f"\n[Error] '{book.title}' was not borrowed.")

    def list_all_books(self):
        if not self.books:
            print("\nThe library is empty.")
            return
        print("\n--- Current Library Collection ---")
        for book_id, book in self.books.items():
            print(f"ID: {book_id} | {book}")
        print("----------------------------------")

    def list_all_members(self): 
        if not self.members:
            print("\nNo members registered in the library.")
            return
        print("\n--- Registered Library Members ---")
        for member_id, member in self.members.items():
            print(f"ID: {member_id} | Name: {member.name} | Borrowed Books: {member.borrowed_books}")
        print("----------------------------------")

    def find_book_by_title(self, title):
        found_books = []
        for book_id, book in self.books.items():
            if title.lower() in book.title.lower():
                found_books.append((book_id, book))
        if found_books:
            print(f"\n--- Search Results for '{title}' ---")
            for book_id, book in found_books:
                print(f"ID: {book_id} | {book}")
            print("------------------------------------")
            return found_books
        else:
            print(f"\nNo books found with title '{title}'.")
            return []


# ==========================================
# INTERACTIVE CLI LOOP (The "cin" Part)
# ==========================================

def main():
    my_library = Library()

    # Pre-loading some mock data so the app isn't empty at start
    my_library.add_member("Alice Smith")
    my_library.add_member("Bob Johnson")
    my_library.add_book("1984", "George Orwell", "978-0451524935", "Shelf B")
    my_library.add_book("Dune", "Frank Herbert", "978-0441013593", "Shelf C")

    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Add Member")
        print("4. Remove Member")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. List All Books")
        print("8. List All Members")
        print("9. Search Book by Title")
        print("0. Exit")
        print("=====================================")
        
        choice = input("Enter your choice (0-9): ").strip()

        try:
            if choice == "1":
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                isbn = input("Enter ISBN: ")
                location = input("Enter location (Default 'Shelf A'): ") or "Shelf A"
                my_library.add_book(title, author, isbn, location)

            elif choice == "2":
                book_id = int(input("Enter Book ID to remove: "))
                my_library.remove_book(book_id)

            elif choice == "3":
                name = input("Enter member name: ")
                my_library.add_member(name)

            elif choice == "4":
                member_id = int(input("Enter Member ID to remove: "))
                my_library.remove_member(member_id)

            elif choice == "5":
                book_id = int(input("Enter Book ID: "))
                member_id = int(input("Enter Member ID: "))
                days = input("Enter days to borrow (Default 7): ")
                days = int(days) if days.isdigit() else 7
                my_library.borrow_book(book_id, member_id, days)

            elif choice == "6":
                book_id = int(input("Enter Book ID to return: "))
                my_library.return_book(book_id)

            elif choice == "7":
                my_library.list_all_books()

            elif choice == "8":
                my_library.list_all_members()

            elif choice == "9":
                title = input("Enter title keyword to search: ")
                my_library.find_book_by_title(title)

            elif choice == "0":
                print("\nGoodbye! Shukriya.")
                break
            else:
                print("\nInvalid choice! Please choose between 0 and 9.")
                
        except ValueError:
            print("\n[Input Error] Please enter numbers correctly for IDs/Dates.")

if __name__ == "__main__":
    main()