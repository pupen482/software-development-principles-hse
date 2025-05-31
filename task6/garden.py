import threading
import random
import time


class Flower:
    def __init__(self, idx):
        self.idx = idx
        self.wilted = True
        self.lock = threading.Lock()

    def water(self, gardener_id):
        with self.lock:
            if self.wilted:
                print(f"Садовник {gardener_id} поливает цветок {self.idx}")
                self.wilted = False
                time.sleep(0.1)
            else:
                print(
                    f"Садовник {gardener_id} подошел к цветку {self.idx}, но он уже полит.")

    def wilt(self):
        with self.lock:
            self.wilted = True


def gardener(gardener_id, flowers):
    while True:
        idx = random.randint(0, len(flowers) - 1)
        flower = flowers[idx]
        flower.water(gardener_id)
        time.sleep(random.uniform(0.2, 0.5))


def wilting_process(flowers):
    while True:
        idx = random.randint(0, len(flowers) - 1)
        flower = flowers[idx]
        flower.wilt()
        print(f"Цветок {flower.idx} завял!")
        time.sleep(random.uniform(1, 2))


def main():
    while True:
        try:
            N = int(input("Введите количество цветов: "))
            if N <= 0:
                print("Число должно быть положительным!")
                continue
            break
        except ValueError:
            print("Введите целое число!")
    while True:
        try:
            M = int(input("Введите количество садовников: "))
            if M <= 0:
                print("Число должно быть положительным!")
                continue
            break
        except ValueError:
            print("Введите целое число!")

    flowers = [Flower(i) for i in range(N)]

    threading.Thread(target=wilting_process, args=(
        flowers,), daemon=True).start()

    for i in range(M):
        threading.Thread(target=gardener, args=(
            i+1, flowers), daemon=True).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
