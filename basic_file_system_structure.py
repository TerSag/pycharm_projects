from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemObject(ABC):
    def __init__(self, name: str, path: str, size: int = 0):
        self.__name = name
        self.__path = path
        self.__size = size
        self.__creation_date = datetime.now()

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def size(self):
        return self.__size

    @property
    def creation_date(self):
        return self.__creation_date

    @abstractmethod
    def get_info(self) -> str:
        pass


class File(FileSystemObject):
    def __init__(self, name: str, path: str, size: int, extension: str):
        super().__init__(name, path, size)
        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    def get_info(self) -> str:
        date_str = self.creation_date.strftime("%Y-%m-%d %H:%M")
        return f"[Файл] {self.name}.{self.extension} | Шлях: {self.path} | Розмір: {self.size} байт | Створено: {date_str}"


class TextFile(File):
    def __init__(self, name: str, path: str, size: int, extension: str, content: str):
        super().__init__(name, path, size, extension)
        self.__content = content

    @property
    def content(self):
        return self.__content

    def get_info(self) -> str:
        base_info = super().get_info()
        preview = self.__content[:20] + "..." if len(self.__content) > 20 else self.__content
        return f"{base_info} | Вміст: '{preview}'"


class ImageFile(File):
    def __init__(self, name: str, path: str, size: int, extension: str, width: int, height: int):
        super().__init__(name, path, size, extension)
        self.__width = width
        self.__height = height

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} | Роздільна здатність: {self.__width}x{self.__height} px"


class Folder(FileSystemObject):
    def __init__(self, name: str, path: str):
        super().__init__(name, path, 0)
        self.__objects = []

    @property
    def size(self):
        return sum(obj.size for obj in self.__objects)

    def add_object(self, obj: FileSystemObject):
        self.__objects.append(obj)

    def get_info(self) -> str:
        date_str = self.creation_date.strftime("%Y-%m-%d %H:%M")
        info = f"[Папка] {self.name} | Шлях: {self.path} | Об'єктів: {len(self.__objects)} | Загальний розмір: {self.size} байт | Створено: {date_str}"
        if self.__objects:
            info += "\n  Вміст папки:"
            for obj in self.__objects:
                info += f"\n    - {obj.get_info()}"
        return info


if __name__ == "__main__":
    doc_file = TextFile(
        name="notes",
        path="C:/Documents",
        size=1024,
        extension="txt",
        content="Привіт, це мої нотатки для пар!"
    )

    photo_file = ImageFile(
        name="avatar",
        path="C:/Pictures",
        size=5048576,
        extension="png",
        width=1920,
        height=1080
    )

    generic_file = File(
        name="config",
        path="C:/System",
        size=256,
        extension="bin"
    )

    my_folder = Folder(name="MyFiles", path="C:/")
    my_folder.add_object(doc_file)
    my_folder.add_object(photo_file)
    my_folder.add_object(generic_file)

    print(doc_file.get_info())
    print(photo_file.get_info())
    print()
    print(my_folder.get_info())