import pymysql
from datetime import datetime
class DatabaseHandler(object):
	"""docstring for DatabaseHandler"""
	def __init__(self, hostname, username, password, databasename):
		super(DatabaseHandler, self).__init__()
		try:
			self.db = pymysql.connect(hostname,username,password,databasename)
			self.cursor = self.db.cursor()
			print("Done.")
		except Exception as e:
			print(type(e))
			print(e)
			exit(1)
	def setupDatabase(self):
		create_table_posts = """
			CREATE TABLE IF NOT EXISTS posts (
				id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
				message VARCHAR(5000) NOT NULL,
				bot_response VARCHAR(10000) DEFAULT NULL
			);
		"""
		try:
			self.cursor.execute(create_table_posts)
		except Exception as e:
			print(type(e))
			print(e)
			exit(1)

	def insertPost(self,msg, response):
		# print("Inserting/Updating post")
		sql_insert_post = (
			"INSERT INTO posts "
			"(message, bot_response)"
			"VALUES (%s, %s)"
			)
		post_info = [
			msg,
			response
			]

		try:
			result = self.cursor.execute(sql_insert_post,post_info)
			self.db.commit()
		except pymysql.err.IntegrityError as e:
			print("Duplicate Post. Updating existing post.")
			self.db.rollback()
			sql_delete_post="DELETE FROM posts WHERE fb_post_id=%s;"
			self.cursor.execute(sql_delete_post,post['id'])
			self.cursor.execute(sql_insert_post,post_info)
			self.db.commit()
		except Exception as e:
			print(type(e))
			print(e)
			self.db.rollback()
	
	
	def getPosts(self):
		sql_select_post = "SELECT * from posts;"
		
		results = []
		try:
			self.cursor.execute(sql_select_post)
			data = self.cursor.fetchall()
			if data is not None:
				for row in data:
					# print(row)
					results.append(row)
		except Exception as e:
			print(type(e))
			print(e)
		return results
	