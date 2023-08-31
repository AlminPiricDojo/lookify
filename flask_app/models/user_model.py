from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import song_model

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.songs = []
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('lookify-office-hour').query_db(query) # Be sure to have the correct schema name here

        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_user_songs(cls, id):
        query = "SELECT * FROM users LEFT JOIN songs ON users.id=songs.user_id WHERE users.id=%(id)s"
        results = connectToMySQL('lookify-office-hour').query_db(query, {'id':id})
        user = cls(results[0])
        for row in results:
            song_data = {
                'id': row['songs.id'],
                'title': row['title'],
                'artist': row['artist'],
                'rating': row['rating'],
                'created_at': row['songs.created_at'],
                'updated_at': row['songs.updated_at'],
                'user_id': row['user_id']
            }
            user.songs.append(song_model.Song(song_data))
        return user