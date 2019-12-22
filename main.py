import ExaminationsPy as ex
import pymysql.cursors
import pdb

def setup_tables():
    subjectsSql = "CREATE Table IF NOT EXISTS subjects (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, exam VARCHAR(200) NOT NULL, subject INT(11) NOT NULL, name VARCHAR(100) NOT NULL)"
    papersSql = "CREATE Table IF NOT EXISTS papers (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, subject VARCHAR(200) NOT NULL, exam VARCHAR(200) NOT NULL, year INT(20) UNSIGNED, level VARCHAR(100) NOT NULL, url VARCHAR(400) NOT NULL)"
    schemesSql = "CREATE Table IF NOT EXISTS schemes (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, subject VARCHAR(200) NOT NULL, exam VARCHAR(200) NOT NULL, year INT(20) UNSIGNED, level VARCHAR(100) NOT NULL, url VARCHAR(400) NOT NULL)"
    try:
        with connection.cursor() as cursor:
            cursor.execute(subjectsSql)
            cursor.execute(papersSql)
            cursor.execute(schemesSql)
        connection.commit()
        return True
    except:
        return False

def insert_materials(connection, table, materials):
    for material in materials:
        with connection.cursor() as cursor:
            sql = "Insert INTO " + table + " (year, subject, exam, level, url) VALUES ({0}, '{1}', '{2}', '{3}', '{4}')".format(material.year, material.subject, material.exam, material.title, material.url)
            cursor.execute(sql)
        connection.commit()

def insert_subject(connection, exam, subject, name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO subjects (exam, subject, name) VALUES ('{0}', {1}, '{2}')".format(exam, subject, name)
        cursor.execute(sql)
    connection.commit()

def subject_exists(connection, subject_id, exam):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM papers WHERE subject = {0} AND exam = '{1}' LIMIT 1".format(subject_id, exam)
            cursor.execute(sql)
            results = cursor.fetchall()
        if(len(results) > 0):
            return True
        else:
            return False
    except:
        return False

def add_materials(connection, exam):
    Examinations = ex.Examinations(exam)
    subjects = Examinations.subjects()
    for subject in subjects:
        # not subject_exists(connection, subject[1], exam)
        if(True):
            print("Now adding: " + exam + "'s " + subject[0])
            #Add the subject to subjects table
            insert_subject(connection, exam, subject[1], subject[0])
            #Add all the papers and marking schemes
            papers = Examinations.papers(subject[0])
            insert_materials(connection, "papers", papers)
            schemes = Examinations.schemes(subject[0])
            insert_materials(connection, "schemes", schemes)
        else:
            print("Exists already")

if __name__ == "__main__":
    #Setup our interfaces
    connection = pymysql.connect(host = "localhost", user = "root", password = "", db = "learnfocused", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    #Add tables if they do not exist
    if(setup_tables()):
        #Add all the subjects
        print("Hello")
        #Add materials for each exam
        exams = ["jc", "lc", "lb"]
        for exam in exams:
            add_materials(connection, exam)
        connection.close()
    else:
        print("Error creating tables")
