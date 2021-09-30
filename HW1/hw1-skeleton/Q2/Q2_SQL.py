########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "jpineda32"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies (id int, " \
                        "title varchar(255), score float)"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast (movie_id int, " \
                        "cast_id int, " \
                        "cast_name varchar(255)," \
                        "birthday varchar(10)," \
                        "popularity float)"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################

       ######################################################################
        cur = connection.cursor()
        file = open(path)
        rows = csv.reader(file)
        cur.executemany("INSERT INTO movies VALUES (?, ?, ?)", rows)


        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        
        ######################################################################
        cur = connection.cursor()
        file = open(path)
        rows = csv.reader(file)
        cur.executemany("INSERT INTO movie_cast VALUES (?, ?, ?,?,?)", rows)

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio (cast_id int, " \
                        "cast_name varchar(255), " \
                        "birthday varchar(10) )"
        ######################################################################
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = "INSERT INTO cast_bio " \
                               "(cast_id, cast_name, birthday) " \
                               " SELECT DISTINCT c.cast_id, c.cast_name, c.birthday " \
                               "FROM movie_cast c"
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX movie_index on movies(id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index on movie_cast(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX cast_bio_index on cast_bio(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = "SELECT printf('%.2f', COUNT(*) * 100.0/ (SELECT COUNT(*) FROM movies) )" \
                     "  " \
                     " FROM movies " \
                     " WHERE score > 50 " \
                     " AND title LIKE '%war%' "
        # print(part_c_sql)
        #part_c_sql = "SELECT COUNT(*) AS s FROM movies WHERE score >50 AND title LIKE '%WAR%' "
         ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = "SELECT mcast.cast_name, count(m.title) as apperance_count " \
                     " FROM movie_cast as mcast" \
                     " INNER JOIN movies as m ON  m.id = mcast.movie_id" \
                     " WHERE mcast.popularity > 10 " \
                     " GROUP BY mcast.cast_name " \
                     " ORDER BY apperance_count DESC, mcast.cast_name ASC" \
                     " LIMIT 5"
                     # " movies as m WHERE m.id = mcast.movie_id " \
    ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = "SELECT m.title, printf('%.2f', m.score), count(mcast.cast_name) as cast_count" \
                     " FROM movies as m INNER JOIN movie_cast as mcast " \
                     " ON m.id = mcast.movie_id " \
                     " GROUP BY m.title " \
                     " ORDER BY score DESC, cast_count DESC, title ASC" \
                     " LIMIT 5"

        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = " SELECT mcast.cast_id, mcast.cast_name, " \
                     "printf('%.2f', avg(m.score)) as average_score " \
        " FROM " \
        " movies as m INNER JOIN movie_cast as mcast" \
        " ON m.id = mcast.movie_id WHERE m.score >= 25 " \
        " GROUP BY mcast.cast_id " \
        " HAVING count(mcast.cast_name) >2" \
        " ORDER BY average_score DESC, cast_name ASC" \
        " LIMIT 10"
       # " HAVING count(mcast.cast_id) > 2 " \
       #  " ORDER BY average_score DESC, cast_name ASC" \
       #  " LIMIT 10"
      ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        # part_g_sql = "CREATE VIEW good_collaboration AS " \
        #              "SELECT tmp1.cast_id as cast_member_id1, tmp2.cast_id as cast_member_id2, COUNT(tmp1.id) as movie_count,  AVG(tmp_table.score) as average_movie_score FROM good_collaboration" \
        #              "  ( (SELECT * FROM movies INNER JOIN movie_cast on movies.id = movie_cast.movie_id) tmp1 " \
        #              " JOIN " \
        #              " (SELECT * FROM movies INNER JOIN movie_cast on movies.id = movie_cast.movie_id) tmp2 " \
        #              " on tmp2.id = tmp1.id) as tmp_table WHERE  tmp1.cast_id < tmp2.cast_id " \
        #              " GROUP BY tmp1.cast_id, tmp2.cast_id "

        part_g_sql = """CREATE VIEW good_collaboration AS
                        SELECT tmp1.cast_id as cast_member_id1, tmp2.cast_id as cast_member_id2, COUNT(tmp1.id) as movie_count,  AVG(tmp_table.score) as average_movie_score FROM
                       ( (SELECT * FROM movies INNER JOIN movie_cast on movies.id = movie_cast.movie_id) tmp1
                        JOIN
                        (SELECT * FROM movies INNER JOIN movie_cast on movies.id = movie_cast.movie_id) tmp2
                        on tmp2.id = tmp1.id) as tmp_table WHERE  tmp1.cast_id < tmp2.cast_id
                        GROUP BY tmp1.cast_id, tmp2.cast_id
                        HAVING average_movie_score >= 40 AND movie_count >= 3
                       """

        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """SELECT tmp_table.cast_id, movie_cast.cast_name, printf("%.2f", AVG(average_movie_score)) as collaboration_score FROM
                           (SELECT cast_member_id1 as cast_id, average_movie_score FROM good_collaboration UNION ALL
                           SELECT cast_member_id2 as cast_id, average_movie_score FROM good_collaboration) as tmp_table
                           INNER JOIN movie_cast on movie_cast.cast_id = tmp_table.cast_id                            
                           GROUP BY tmp_table.cast_id
                           ORDER BY collaboration_score DESC, cast_name
                           LIMIT 5"""
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE movie_overview USING fts4(id, overview)"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        cur = connection.cursor()
        file = open(path)
        rows = csv.reader(file)
        cur.executemany("INSERT INTO movie_overview VALUES (?, ?)", rows)
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'fight'"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ## Taken from stackoverflow https://stackoverflow.com/questions/35185517/sqlite3-fts-limiting-length-of-items-between-two-words-in-match-request
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program' "
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")
    conn.close()
    #################################################################################
    #################################################################################
  
