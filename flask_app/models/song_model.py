from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user_model

class Song:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] # NEW
        self.user = None # NEW

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM songs LEFT JOIN users ON songs.user_id=users.id;"
        results = connectToMySQL('lookify-office-hour').query_db(query) # Be sure to have the correct schema name here

        # Create an empty list to append our instances of friends
        songs = []
        # Iterate over the db results and create instances of friends with cls.
        for row in results:
            this_song = cls(row)

            user_data = {
                'id': row['user_id'],
                'name': row['name'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_song.user = user_model.User(user_data)

            songs.append(this_song)
        return songs
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO songs (title, artist, rating, user_id, created_at, updated_at) VALUES (%(title)s, %(artist)s, %(rating)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('lookify-office-hour').query_db(query, data)
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM songs LEFT JOIN users ON songs.user_id=users.id WHERE songs.id=%(id)s"
        results = connectToMySQL('lookify-office-hour').query_db(query, {'id':id})
        this_song = cls(results[0])
        print(this_song)
        user_data = {
                'id': results[0]['user_id'],
                'name': results[0]['name'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at']
            }
        this_song.user = user_model.User(user_data)
        return this_song
    
    @classmethod
    def update(cls, data):
        query = "UPDATE songs SET title=%(title)s, artist=%(artist)s, rating=%(rating)s, user_id=%(user_id)s WHERE id=%(id)s"
        return connectToMySQL('lookify-office-hour').query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM songs WHERE id=%(id)s"
        return connectToMySQL('lookify-office-hour').query_db(query, {"id":id})