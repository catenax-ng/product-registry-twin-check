from tqdm import tqdm
from time import sleep

if __name__ == '__main__':
    for i in tqdm(range(10)):
        print(i)
        sleep(3)