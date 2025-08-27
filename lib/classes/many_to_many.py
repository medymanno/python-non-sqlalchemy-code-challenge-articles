# lib/classes/many_to_many.py

from typing import List, Optional


class Author:
    def __init__(self, name: str):
        # initial validation (raise on bad input)
        if not isinstance(name, str):
            raise Exception("name must be a string")
        if len(name) == 0:
            raise Exception("name must be longer than 0 characters")
        # set private attribute
        self._name = name

    @property
    def name(self) -> str:
        # read-only behavior from outside; setter will ignore later attempts
        return self._name

    @name.setter
    def name(self, value: str):
        # Immutable after initialization: ignore any reassignment attempts
        # (do nothing; keep original _name)
        return

    def articles(self) -> List["Article"]:
        # single source of truth: Article.all
        return [a for a in Article.all if a.author is self]

    def magazines(self) -> List["Magazine"]:
        mags = []
        for a in self.articles():
            if a.magazine not in mags:
                mags.append(a.magazine)
        return mags

    def add_article(self, magazine: "Magazine", title: str) -> "Article":
        # creates and returns a new Article associated with this author
        return Article(self, magazine, title)

    def topic_areas(self) -> Optional[List[str]]:
        mags = self.magazines()
        if not mags:
            return None
        cats = []
        for m in mags:
            if m.category not in cats:
                cats.append(m.category)
        return cats

    def __repr__(self):
        return f"<Author name={self.name!r}>"


class Magazine:
    _all: List["Magazine"] = []

    def __init__(self, name: str, category: str):
        # initial validation (raise on bad input)
        if not isinstance(name, str):
            raise Exception("name must be a string")
        if not (2 <= len(name) <= 16):
            raise Exception("name must be between 2 and 16 characters")
        if not isinstance(category, str):
            raise Exception("category must be a string")
        if len(category) == 0:
            raise Exception("category must be longer than 0 characters")

        # set via private attributes (use setters semantics by direct assignment)
        self._name = name
        self._category = category

        Magazine._all.append(self)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        # accept change only if valid; otherwise ignore (no exception)
        if isinstance(value, str) and (2 <= len(value) <= 16):
            self._name = value
        # else ignore invalid assignment

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        # accept change only if valid; otherwise ignore
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # else ignore invalid assignment

    def articles(self) -> List["Article"]:
        return [a for a in Article.all if a.magazine is self]

    def contributors(self) -> List[Author]:
        authors = []
        for a in self.articles():
            if a.author not in authors:
                authors.append(a.author)
        return authors

    def article_titles(self) -> Optional[List[str]]:
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self) -> Optional[List[Author]]:
        arts = self.articles()
        if not arts:
            return None
        counts = {}
        for a in arts:
            counts[a.author] = counts.get(a.author, 0) + 1
        result = [author for author, cnt in counts.items() if cnt > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls) -> Optional["Magazine"]:
        if not Article.all:
            return None
        best = None
        best_count = 0
        for mag in cls._all:
            count = len([a for a in Article.all if a.magazine is mag])
            if count > best_count:
                best = mag
                best_count = count
        return best

    def __repr__(self):
        return f"<Magazine name={self.name!r} category={self.category!r}>"


class Article:
    all: List["Article"] = []

    def __init__(self, author: Author, magazine: Magazine, title: str):
        # initial validation (raise on bad input)
        if not isinstance(author, Author):
            raise Exception("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("magazine must be a Magazine instance")
        if not isinstance(title, str):
            raise Exception("title must be a string")
        if not (5 <= len(title) <= 50):
            raise Exception("title must be between 5 and 50 characters")

        # store private attributes
        self._title = title
        self._author = author
        self._magazine = magazine

        # register in single source-of-truth list
        Article.all.append(self)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value):
        # immutable after init: ignore any reassignment attempts
        return

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, value):
        # mutable, accept only Author instances; ignore invalid assignment
        if isinstance(value, Author):
            self._author = value
        # else ignore

    @property
    def magazine(self) -> Magazine:
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # mutable, accept only Magazine instances; ignore invalid assignment
        if isinstance(value, Magazine):
            self._magazine = value
        # else ignore

    def __repr__(self):
        return f"<Article title={self.title!r} author={self.author.name!r} magazine={self.magazine.name!r}>"
