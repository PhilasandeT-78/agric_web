import sqlite3


db_path = 'site.db'


conn = sqlite3.connect(db_path)
cursor = conn.cursor()


with open('site_backup.sql', 'w') as f:
    for line in conn.iterdump():
        f.write('%s\n' % line)


conn.close()

print("SQL dump saved to site_backup.sql")
