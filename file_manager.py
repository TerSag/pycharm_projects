import copy
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

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, new_path):
        self.__path = new_path

    @property
    def size(self):
        return self.__size

    @property
    def creation_date(self):
        return self.__creation_date

    @abstractmethod
    def get_info(self) -> str:
        pass

    def rename(self, new_name: str):
        self.name = new_name

    def delete(self):
        self.__name = None

    def copy(self):
        copied_obj = copy.deepcopy(self)
        copied_obj.rename(f"{self.name}_copy")
        return copied_obj


class File(FileSystemObject):
    def __init__(self, name: str, path: str, size: int, extension: str):
        super().__init__(name, path, size)
        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    def get_info(self) -> str:
        date_str = self.creation_date.strftime("%Y-%m-%d %H:%M")
        return f"[Файл] {self.name}.{self.extension} | Шлях: {self.path} | Розмір: {self.size} байт"


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

    @property
    def objects(self):
        return self.__objects

    def add_object(self, obj: FileSystemObject):
        for existing in self.__objects:
            if existing.name == obj.name:
                return False

        new_path = f"{self.path}/{self.name}" if self.path != "/" else f"/{self.name}"
        obj.path = new_path
        self.__objects.append(obj)
        return True

    def remove_object(self, name: str):
        for obj in self.__objects:
            if obj.name == name:
                obj.delete()
                self.__objects.remove(obj)
                return True
        return False

    def get_object(self, name: str):
        for obj in self.__objects:
            if obj.name == name:
                return obj
        return None

    def show_contents(self) -> str:
        if not self.__objects:
            return f"Папка '{self.name}' порожня."
        res = f"Вміст папки '{self.name}':\n"
        for obj in self.__objects:
            res += f"  - {obj.get_info()}\n"
        return res.strip()

    def get_info(self) -> str:
        return f"[Папка] {self.name} | Шлях: {self.path} | Об'єктів: {len(self.__objects)} | Загальний розмір: {self.size} байт"


class FileManager:
    def __init__(self):
        self.root = Folder("root", "/")

    def find_folder(self, path: str, current: Folder = None) -> Folder:
        if current is None:
            current = self.root
        if path in ("/", "/root"):
            return self.root

        parts = [p for p in path.split("/") if p and p != "root"]

        curr = self.root
        for part in parts:
            found = False
            for obj in curr.objects:
                if isinstance(obj, Folder) and obj.name == part:
                    curr = obj
                    found = True
                    break
            if not found:
                return None
        return curr

    def create_folder(self, name: str, parent_path: str = "/"):
        parent = self.find_folder(parent_path)
        if not parent:
            print(f"Помилка: Шлях '{parent_path}' не знайдено.")
            return
        if parent.get_object(name):
            print(f"Помилка: Об'єкт '{name}' вже існує у цій папці.")
            return

        new_folder = Folder(name, parent_path)
        parent.add_object(new_folder)
        print(f"Папку '{name}' успішно створено.")

    def create_file(self, file_obj: File, parent_path: str = "/"):
        parent = self.find_folder(parent_path)
        if not parent:
            print(f"Помилка: Шлях '{parent_path}' не знайдено.")
            return
        if parent.get_object(file_obj.name):
            print(f"Помилка: Об'єкт '{file_obj.name}' вже існує.")
            return

        parent.add_object(file_obj)
        print(f"Файл '{file_obj.name}' успішно створено.")

    def delete_object(self, name: str, parent_path: str = "/"):
        parent = self.find_folder(parent_path)
        if not parent:
            print(f"Помилка: Шлях '{parent_path}' не знайдено.")
            return
        if parent.remove_object(name):
            print(f"Об'єкт '{name}' успішно видалено.")
        else:
            print(f"Помилка: Об'єкт '{name}' не знайдено.")

    def rename_object(self, old_name: str, new_name: str, parent_path: str = "/"):
        parent = self.find_folder(parent_path)
        if not parent:
            print(f"Помилка: Шлях '{parent_path}' не знайдено.")
            return

        obj = parent.get_object(old_name)
        if not obj:
            print(f"Помилка: Об'єкт '{old_name}' не знайдено.")
            return

        if parent.get_object(new_name):
            print(f"Помилка: Об'єкт '{new_name}' вже існує.")
            return

        obj.rename(new_name)
        print(f"Об'єкт '{old_name}' перейменовано на '{new_name}'.")

    def move_object(self, name: str, source_path: str, dest_path: str):
        source_folder = self.find_folder(source_path)
        dest_folder = self.find_folder(dest_path)

        if not source_folder or not dest_folder:
            print("Помилка: Неправильний шлях джерела або призначення.")
            return

        obj = source_folder.get_object(name)
        if not obj:
            print(f"Помилка: Об'єкт '{name}' не знайдено.")
            return

        if dest_folder.get_object(name):
            print(f"Помилка: Об'єкт '{name}' вже існує у місці призначення.")
            return

        if isinstance(obj, Folder):
            obj_full_path = f"{source_path}/{name}".replace("//", "/")
            if dest_path == obj_full_path or dest_path.startswith(obj_full_path + "/"):
                print("Помилка: Неможливо перемістити папку саму в себе або в її підпапку.")
                return

        source_folder.remove_object(name)
        dest_folder.add_object(obj)
        print(f"Об'єкт '{name}' переміщено до '{dest_path}'.")

    def copy_object(self, name: str, source_path: str, dest_path: str):
        source_folder = self.find_folder(source_path)
        dest_folder = self.find_folder(dest_path)

        if not source_folder or not dest_folder:
            print("Помилка: Неправильний шлях джерела або призначення.")
            return

        obj = source_folder.get_object(name)
        if not obj:
            print(f"Помилка: Об'єкт '{name}' не знайдено.")
            return

        copied_obj = obj.copy()

        while dest_folder.get_object(copied_obj.name):
            copied_obj.rename(copied_obj.name + "_copy")

        dest_folder.add_object(copied_obj)
        print(f"Об'єкт '{name}' скопійовано до '{dest_path}' під іменем '{copied_obj.name}'.")


if __name__ == "__main__":
    fm = FileManager()

    fm.create_folder("Documents")
    fm.create_folder("Pictures")

    doc = TextFile("notes", "", 1024, "txt", "Важливі нотатки")
    fm.create_file(doc, "/Documents")

    print("\n--- Демонстрація помилок ---")
    fm.create_folder("Documents")
    fm.move_object("Documents", "/", "/Documents")

    print("\n--- Копіювання та Переміщення ---")
    fm.copy_object("notes", "/Documents", "/Pictures")
    fm.rename_object("notes_copy", "photo_notes", "/Pictures")
    fm.move_object("notes", "/Documents", "/")

    print("\n--- Видалення ---")
    fm.delete_object("Documents", "/")

    print("\n--- Вміст кореневої папки ---")
    print(fm.root.show_contents())

    print("\n--- Вміст папки Pictures ---")
    pic_folder = fm.find_folder("/Pictures")
    print(pic_folder.show_contents())