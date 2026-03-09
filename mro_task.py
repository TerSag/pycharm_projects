# Базовий клас
class Core:
    def boot(self):
        print("Core boot")

# 4 проміжні класи
class PowerModule(Core):
    def boot(self):
        print("PowerModule boot")
        super().boot()

class SensorsModule(Core):
    def boot(self):
        print("SensorsModule boot")
        super().boot()

class CommsModule(Core):
    def boot(self):
        print("CommsModule boot")
        super().boot()

class LoggerModule(Core):
    def boot(self):
        print("LoggerModule boot")
        super().boot()

# Складніші проміжні класи
class SafetyModule(SensorsModule, LoggerModule):
    def boot(self):
        print("SafetyModule boot")
        super().boot()

class DiagnosticsModule(CommsModule, LoggerModule):
    def boot(self):
        print("DiagnosticsModule boot")
        super().boot()

# Фінальний клас для пунктів 1 та 2
class Robot(PowerModule, SafetyModule, DiagnosticsModule):
    pass

print("=== Пункт (1): Виклик r.boot() ===")
r = Robot()
r.boot()
# Точний порядок рядків:
# 1. PowerModule boot
# 2. SafetyModule boot
# 3. SensorsModule boot
# 4. DiagnosticsModule boot
# 5. CommsModule boot
# 6. LoggerModule boot
# 7. Core boot

print("\n=== Пункт (2): Вивід Robot.__mro__ та пояснення ===")
for cls in Robot.__mro__:
    print(cls.__name__)

# ПОЯСНЕННЯ ДЛЯ ЗВІТУ (Пункт 2):
# MRO (Method Resolution Order) формується за алгоритмом C3 Linearization.
# Python обходить дерево класів зліва направо, але гарантує дві речі:
# 1. Діти завжди перевіряються перед батьками.
# 2. Зберігається порядок базових класів, вказаний при оголошенні.
#
# Чому саме такий порядок:
# - Robot шукає boot() у себе. Його немає.
# - Йде у першого батька зліва: PowerModule. (Друкує PowerModule boot).
# - super() у PowerModule передає естафету наступному класу в MRO Робота, а не своєму батьку (Core)!
# - Наступний в MRO - SafetyModule. (Друкує SafetyModule boot).
# - SafetyModule передає виклик своєму першому батьку - SensorsModule.
# - Після SensorsModule черга доходить до DiagnosticsModule, а потім до його батька CommsModule.
# - LoggerModule є спільним батьком для SafetyModule та DiagnosticsModule, тому алгоритм відкладає
#   його виклик доти, поки не будуть пройдені всі його "нащадки". Тому він викликається передостаннім.
# - Core - загальний предок усіх, викликається останнім.

print("\n=== Пункт (3): Зміна LoggerModule ===")
# Вносимо зміну (перевизначаємо клас)
class LoggerModuleDirect(Core): # Назвемо інакше для наочності в скрипті
    def boot(self):
        print("LoggerModule boot")
        Core.boot(self) # Прямий виклик замість super()

# Щоб зміна запрацювала, перезберемо класи, які від нього залежать
class SafetyModuleMod(SensorsModule, LoggerModuleDirect):
    def boot(self):
        print("SafetyModule boot")
        super().boot()

class DiagnosticsModuleMod(CommsModule, LoggerModuleDirect):
    def boot(self):
        print("DiagnosticsModule boot")
        super().boot()

class RobotMod(PowerModule, SafetyModuleMod, DiagnosticsModuleMod):
    pass

r_mod = RobotMod()
r_mod.boot()

# ПОЯСНЕННЯ ДЛЯ ЗВІТУ (Пункт 3):
# Якщо ми порівняємо вивід, ми побачимо, що ВІН НЕ ЗМІНИВСЯ. Жодні методи НЕ перестали виконуватись.
# Чому так вийшло:
# Прямий виклик Core.boot(self) "ламає" ланцюжок super(), оскільки він жорстко викликає метод
# конкретного класу і не йде далі по MRO.
# АЛЕ, у нашому конкретному MRO клас LoggerModule стоїть ПЕРЕДОСТАННІМ, одразу перед Core.
# Тому його super().boot() і так викликав би Core.boot().
# Якби ми замінили super() на прямий виклик, наприклад, у PowerModule, тоді б ми пропустили
# і Safety, і Sensors, і Diagnostics, бо ланцюжок MRO обірвався б на самому початку.

print("\n=== Пункт (4): Зміна порядку базових класів у Robot ===")

class RobotReordered(SafetyModule, PowerModule, DiagnosticsModule):
    pass

r_reordered = RobotReordered()
r_reordered.boot()

print("\nНовий MRO:")
for cls in RobotReordered.__mro__:
    print(cls.__name__)

# ПОЯСНЕННЯ ДЛЯ ЗВІТУ (Пункт 4):
# Ми змінили порядок наслідування на: class Robot(SafetyModule, PowerModule, DiagnosticsModule).
# Оскільки порядок зліва направо змінився, C3 Linearization будує новий маршрут:
# 1. RobotReordered
# 2. SafetyModule (тепер він перший зліва)
# 3. SensorsModule (перший батько SafetyModule)
# 4. PowerModule (другий у списку наслідування Robot)
# 5. DiagnosticsModule (третій у списку наслідування Robot)
# 6. CommsModule (перший батько DiagnosticsModule)
# 7. LoggerModule (спільний батько, відкладений на кінець)
# 8. Core
# 9. object
#
# Результат виводу r.boot() відповідно змінився: спочатку виконується гілка SafetyModule
# (Safety -> Sensors), потім PowerModule, потім гілка DiagnosticsModule (Diag -> Comms),
# і в кінці загальні бази (Logger -> Core).