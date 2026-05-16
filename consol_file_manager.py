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

    @size.setter
    def size(self, new_size):
        self.__size = new_size

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
        date_str = self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        return f"[Файл] {self.name}.{self.extension} | Шлях: {self.path} | Розмір: {self.size} байт"


class TextFile(File):
    def __init__(self, name: str, path: str, extension: str = "txt", content: str = ""):
        super().__init__(name, path, len(content), extension)
        self.__content = content

    @property
    def content(self):
        return self.__content

    def read(self) -> str:
        return self.__content

    def write(self, text: str, append: bool = False):
        if append:
            self.__content += text
        else:
            self.__content = text
        self.size = len(self.__content.encode('utf-8'))

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
        new_path = new_path.replace("//", "/")
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
            return f"Папка порожня."
        res = ""
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

    def search(self, keyword: str, current_folder: Folder = None, results: list = None) -> list:
        if current_folder is None:
            current_folder = self.root
        if results is None:
            results = []

        for obj in current_folder.objects:
            if keyword.lower() in obj.name.lower():
                results.append(obj)
            if isinstance(obj, Folder):
                self.search(keyword, obj, results)

        return results


def main():
    fm = FileManager()

    while True:
        print("\n=== ФАЙЛОВИЙ МЕНЕДЖЕР ===")
        print("1. Створити папку")
        print("2. Створити текстовий файл")
        print("3. Переглянути вміст папки")
        print("4. Пошук об'єктів")
        print("5. Перейменувати об'єкт")
        print("6. Видалити об'єкт")
        print("7. Копіювати об'єкт")
        print("8. Перемістити об'єкт")
        print("9. Читати текстовий файл")
        print("10. Записати у текстовий файл")
        print("0. Вийти")

        choice = input("Оберіть дію: ").strip()

        try:
            if choice == "0":
                print("Вихід з програми...")
                break

            elif choice == "1":
                parent_path = input("Введіть шлях батьківської папки (наприклад, /): ").strip()
                name = input("Введіть назву нової папки: ").strip()
                parent = fm.find_folder(parent_path)
                if not parent:
                    print("Помилка: Шлях не знайдено.")
                    continue
                if parent.get_object(name):
                    print("Помилка: Об'єкт з такою назвою вже існує.")
                    continue
                parent.add_object(Folder(name, parent_path))
                print(f"Папку '{name}' створено.")

            elif choice == "2":
                parent_path = input("Введіть шлях (наприклад, /): ").strip()
                name = input("Введіть назву файлу (без розширення): ").strip()
                parent = fm.find_folder(parent_path)
                if not parent:
                    print("Помилка: Шлях не знайдено.")
                    continue
                if parent.get_object(name):
                    print("Помилка: Об'єкт з такою назвою вже існує.")
                    continue
                tf = TextFile(name, parent_path)
                parent.add_object(tf)
                print(f"Файл '{name}.txt' створено.")

            elif choice == "3":
                path = input("Введіть шлях до папки (наприклад, /): ").strip()
                folder = fm.find_folder(path)
                if not folder:
                    print("Помилка: Папку не знайдено.")
                else:
                    print(f"\n{folder.get_info()}")
                    print(folder.show_contents())

            elif choice == "4":
                keyword = input("Введіть назву для пошуку (повну або часткову): ").strip()
                results = fm.search(keyword)
                if results:
                    print("\nЗнайдені об'єкти:")
                    for res in results:
                        print(f"  - {res.get_info()}")
                else:
                    print("Об'єктів не знайдено.")

            elif choice == "5":
                path = input("Введіть шлях до папки, де лежить об'єкт: ").strip()
                old_name = input("Стара назва: ").strip()
                new_name = input("Нова назва: ").strip()
                folder = fm.find_folder(path)
                if folder and folder.get_object(old_name):
                    folder.get_object(old_name).rename(new_name)
                    print("Успішно перейменовано.")
                else:
                    print("Помилка: Об'єкт або шлях не знайдено.")

            elif choice == "6":
                path = input("Введіть шлях до папки: ").strip()
                name = input("Назва об'єкта для видалення: ").strip()
                folder = fm.find_folder(path)
                if folder and folder.remove_object(name):
                    print("Об'єкт видалено.")
                else:
                    print("Помилка: Об'єкт не знайдено.")

            elif choice == "7":
                src_path = input("Введіть шлях, де лежить об'єкт: ").strip()
                name = input("Назва об'єкта: ").strip()
                dst_path = input("Введіть шлях, куди копіювати: ").strip()
                src_folder = fm.find_folder(src_path)
                dst_folder = fm.find_folder(dst_path)

                if src_folder and dst_folder:
                    obj = src_folder.get_object(name)
                    if obj:
                        copied = obj.copy()
                        while dst_folder.get_object(copied.name):
                            copied.rename(copied.name + "_copy")
                        dst_folder.add_object(copied)
                        print("Об'єкт скопійовано.")
                    else:
                        print("Помилка: Об'єкт не знайдено.")
                else:
                    print("Помилка: Неправильний шлях.")

            elif choice == "8":
                src_path = input("Введіть шлях, де лежить об'єкт: ").strip()
                name = input("Назва об'єкта: ").strip()
                dst_path = input("Введіть шлях, куди перемістити: ").strip()
                src_folder = fm.find_folder(src_path)
                dst_folder = fm.find_folder(dst_path)

                if src_folder and dst_folder:
                    obj = src_folder.get_object(name)
                    if obj:
                        if isinstance(obj, Folder) and (
                                dst_path == f"{src_path}/{name}".replace("//", "/") or dst_path.startswith(
                                f"{src_path}/{name}/".replace("//", "/"))):
                            print("Помилка: Неможливо перемістити папку саму в себе.")
                            continue
                        src_folder.remove_object(name)
                        dst_folder.add_object(obj)
                        print("Об'єкт переміщено.")
                    else:
                        print("Помилка: Об'єкт не знайдено.")
                else:
                    print("Помилка: Неправильний шлях.")

            elif choice == "9":
                path = input("Введіть шлях до папки: ").strip()
                name = input("Назва файлу: ").strip()
                folder = fm.find_folder(path)
                if folder:
                    obj = folder.get_object(name)
                    if isinstance(obj, TextFile):
                        print(f"\n--- Вміст файлу '{name}' ---")
                        print(obj.read())
                        print("------------------------------")
                    else:
                        print("Помилка: Це не текстовий файл або його не знайдено.")
                else:
                    print("Помилка: Шлях не знайдено.")

            elif choice == "10":
                path = input("Введіть шлях до папки: ").strip()
                name = input("Назва файлу: ").strip()
                folder = fm.find_folder(path)
                if folder:
                    obj = folder.get_object(name)
                    if isinstance(obj, TextFile):
                        mode = input("Ввести новий текст (1) чи додати до існуючого (2)? ").strip()
                        text = input("Введіть текст: ")
                        if mode == "1":
                            obj.write(text, append=False)
                        else:
                            obj.write(text, append=True)
                        print("Текст успішно записано. Розмір файлу оновлено.")
                    else:
                        print("Помилка: Це не текстовий файл або його не знайдено.")
                else:
                    print("Помилка: Шлях не знайдено.")
            else:
                print("Невідома команда. Спробуйте ще раз.")

        except Exception as e:
            print(f"Сталася непередбачена помилка: {e}")


if __name__ == "__main__":
    main()