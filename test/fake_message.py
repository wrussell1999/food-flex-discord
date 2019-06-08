class FakeMessage:

    def __init__(self, author, clean_content):
        self.author = author
        self.clean_content = clean_content


class FakeAuthor:

    def __init__(self, id, nick):
        self.id = id
        self.nick = nick
