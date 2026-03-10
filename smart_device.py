class Device:
    def __init__(self):
        print("Device initialized")

    def __del__(self):
        print("Device destroyed")


class Camera(Device):
    def __init__(self):
        print("Camera initialized")
        super().__init__()

    def __del__(self):
        print("Camera destroyed")
        super().__del__()


class Microphone(Device):
    def __init__(self):
        print("Microphone initialized")
        super().__init__()

    def __del__(self):
        print("Microphone destroyed")
        super().__del__()


class Speaker(Device):
    def __init__(self):
        print("Speaker initialized")
        super().__init__()

    def __del__(self):
        print("Speaker destroyed")
        super().__del__()


class VoiceModule(Microphone, Speaker):
    def __init__(self):
        print("VoiceModule initialized")
        super().__init__()

    def __del__(self):
        print("VoiceModule destroyed")
        super().__del__()


class SmartAssistant(Camera, VoiceModule):
    def __init__(self):
        print("SmartAssistant initialized")
        super().__init__()

    def __del__(self):
        print("SmartAssistant destroyed")
        super().__del__()


# Головна частина програми
if __name__ == "__main__":
    print("--- Створення об'єкта ---")
    assistant = SmartAssistant()

    print("\n--- MRO (Method Resolution Order) ---")
    print(SmartAssistant.__mro__)

    print("\n--- Видалення об'єкта ---")
    del assistant
