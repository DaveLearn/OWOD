import random
from collections import deque

class StoreRandomSample:
    def __init__(self, total_num_classes, items_per_class, shuffle=False):
        self.shuffle = shuffle
        self.items_per_class = items_per_class
        self.total_num_classes = total_num_classes
        self.store = [list() for _ in range(self.total_num_classes)]
        self.seen = [0 for _ in range(self.total_num_classes)]

    def add(self, items, class_ids):
    
        for idx, class_id in enumerate(class_ids):
            if class_id >= self.total_num_classes:
                continue        
            save_this_sample_prob = min(1, self.items_per_class / self.seen[class_id])
            save_this_sample = random.random() < save_this_sample_prob
            
            if not save_this_sample:
                continue
            
            class_store = self.store[class_id]
            if (len(class_store)) < self.items_per_class:
                class_store.append(items[idx])
            else:
                # replace one randomly
                class_store[random.randint(0, self.items_per_class - 1)] = items[idx]

    def retrieve(self, class_id):
        if class_id != -1:
            items = []
            for item in self.store[class_id]:
                items.extend(list(item))
            if self.shuffle:
                random.shuffle(items)
            return items
        else:
            all_items = []
            for i in range(self.total_num_classes):
                items = []
                for item in self.store[i]:
                    items.append(list(item))
                all_items.append(items)
            return all_items

    def reset(self):
        self.store = [deque(maxlen=self.items_per_class) for _ in range(self.total_num_classes)]

    def __str__(self):
        s = self.__class__.__name__ + '('
        for idx, item in enumerate(self.store):
            s += '\n Class ' + str(idx) + ' --> ' + str(len(list(item))) + ' items'
        s = s + ' )'
        return s

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return sum([len(s) for s in self.store])


if __name__ == "__main__":
    store = StoreWithReplace(10, 3)
    store.add(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'i'), (1, 1, 9, 1, 0, 1, 1))
    store.add(('h',), (4,))
    # print(store.retrieve(1))
    # print(store.retrieve(3))
    # print(store.retrieve(9))
    print(store.retrieve(-1))
    # print(len(store))
    # store.reset()
    # print(len(store))

    print(store)