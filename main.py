import ExaminationsPy as ex
import pymysql.cursors
import pdb

levels = ["Higher Level", "Ordinary Level"]

def add_papers(connection, exam):
    subjects = Examinations.subjects(exam)
    for subject in subjects:
        pdb.set_trace()
        table = exam + "_papers_"  + subject.replace(" ", "_").lower()
        try:
            with connection.cursor() as cursor:
                sql = "CREATE Table lc_papers_accounting (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, year INT(20) UNSIGNED, level VARCHAR(100) NOT NULL, type VARCHAR(200) NOT NULL, url VARCHAR(400) NOT NULL)"
                cursor.execute(sql)
            connection.commit()
            for level in levels:
                papers = Examinations.papers(exam = "lc", subject = subject, level = level)
                for paper in papers:
                    paper.fetch()
                    with connection.cursor() as cursor:
                        cursor.execute("Insert INTO " + table + " (year, level, type, url) VALUES ({0}, '{1}', '{2}', '{3}')".format(paper.year, paper.title, "exampapers", paper.url))
                    connection.commit()
        except:
            print("Error")

def main():
    connection = pymysql.connect(host = "localhost", user = "root", password = "", db = "LearnFocused", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    add_papers(connection, "lc")
    connection.close()

if __name__ == "__main__":
    Examinations = ex.Examinations()
    main()
