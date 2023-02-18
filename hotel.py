import sqlite3

class Room:
    def __init__(self, id, beds, category, price, state):
        self.id = id
        self.beds = beds
        self.category = category
        self.price = price
        self.state = state
        self.room = {"ID": self.id, "BEDS": self.beds, "CATEGORY": self.category, "PRICE": self.price, "STATE": self.state}
    
    def info(self):
        return self.room
    
    def __str__(self):
        return "Room {} has {} bed(s), is a {}, costs {}$ and it is {}".format(self.id, self.beds, self.category, self.price, self.state)

class DB:
    def __init__(self, db="roomData.db"):
        self.db=db
        self.conn=sqlite3.connect(db, check_same_thread=False)
        self.c=self.conn.cursor()
        try:
            print(f"[*] [HOTEL LIB] Creating new table '{self.db}'...")
            # create a table
            self.c.execute("""CREATE TABLE roomdata (id real, beds real, category text, price real, state real)""")
            print("[*] [HOTEL LIB] Table successfully created ")
        except:
            print("[!] [HOTEL LIB] Database already exists")
        self.conn.commit()

    def add_room(self, r):
        self.c.execute("SELECT * FROM roomdata WHERE ("
                       "id=? "
                       "AND beds=? "
                       "AND category=? "
                       "AND price=? "
                       "AND state=?)",(r.id, r.beds, r.category, r.price, r.state))
        entry = self.c.fetchone()
        if entry is None:
            print(f'[!] [HOTEL LIB] No entry found. Adding room {r.id}')
            self.c.execute("INSERT INTO roomdata VALUES (?, ?, ?, ?, ?)", (r.id, r.beds, r.category, r.price, r.state))
        else: print(f'[*] [SQLITE LIB] Entry found for {r.id}. In order to change something, use DB.update_room_state')
        self.conn.commit()

    def get_data_by_id(self, id, t="l"):
        self.id = id
        self.c.execute(f"SELECT * FROM roomdata  WHERE id={self.id}")
        return [Room(id, beds, category, price, state) if t=="o" else [id, beds, category, price, state] for id, beds, category, price, state in self.c.fetchall()] # return [row for row in self.c.fetchall()]

    def get_all(self, t="l"):
        self.c.execute(f"SELECT * FROM roomdata")
        return [Room(id, beds, category, price, state) for id, beds, category, price, state in self.c.fetchall()] # if t=="o" else [id, beds, category, price, state]  

    def update_room_availability(self, id, state):
        self.id = id
        self.state = state
        self.c.execute(f"SELECT * FROM roomdata  WHERE id={self.id}")
        entry = self.c.fetchone()
        if entry is None:
            print(f'[!] [HOTEL LIB] No entry found.')
            raise Exception(f"Room with id {self.id} not found")
        else:
            self.c.execute(f"UPDATE roomdata SET state = {state} WHERE id = {id}")
        #return [Room(id, beds, category, price, state) for id, beds, category, price, state in self.c.fetchall()]
    
    def delete_room_by_id(self, id):
        self.id = id
        self.c.execute(f"SELECT * FROM roomdata  WHERE id={self.id}")
        entry = self.c.fetchone()
        if entry is None:
            print(f'[!] [HOTEL LIB] No entry found.')
            raise Exception(f"Room with id {self.id} not found")
        else:
            self.c.execute(f"DELETE FROM roomdata WHERE id={self.id}")

# if __name__ == "__main__":
#     r1 = Room(32, 2, "Vila", 450.85, 0)
#     r2 = Room(6, 3, "Vila", 640.90, 0)
#     print(r1)
#     print(r2)
#     mydb = DB()
#     mydb.add_room(r1)
#     mydb.add_room(r2)
#     for room in mydb.get_all(): print(room)
#     mydb.update_room_availability(32, 1)
#     print(mydb.get_all()[0].id)
#     for room in  mydb.get_data_by_id(32): print(room)