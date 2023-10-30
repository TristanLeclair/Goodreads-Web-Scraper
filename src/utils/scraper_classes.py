from enum import Enum


class GoodReadsGenres(Enum):
    Art = "Art"
    Biography = "Biography"
    Fantasy = "Fantasy"

    def __str__(self):
        return self.value


class Book:
    def __init__(self, title, author, rating, description, genres):
        self.title = title
        self.author = author
        self.rating = rating
        self.description = description
        self.genres = genres

    def __str__(self):
        # print as dictionary
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def encode(self):
        return {
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
            "description": self.description,
            "genres": self.genres,
        }
