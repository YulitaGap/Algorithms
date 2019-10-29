class Heap:
    def __init__(self):
        self.heap_size = 0
        self.heap_array = []
        self.heap_length = len(self.heap_array)
        self.heap_max = -1

    def is_empty(self):
        return self.heap_length == 0

    @staticmethod
    def right(i):
        return 2 * i + 2

    @staticmethod
    def left(i):
        return 2 * i + 1


class LowHeap(Heap):
    def MinHeapify(self, i):
        p = self.left(i)
        q = self.right(i)
        if len(self.heap_array) > p and self.heap_array[p] < self.heap_array[i]:
            self.heap_max = p
        else:
            self.heap_max = i
        if len(self.heap_array) > q and self.heap_array[q] < self.heap_array[self.heap_max]:
            self.heap_max = q
        if self.heap_max != i:
            self.heap_array[i], self.heap_array[self.heap_max] = self.heap_array[self.heap_max], \
                                                                 self.heap_array[i]
            self.MinHeapify(self.heap_max)

    def BuildMinHeap(self):
        for i in range(len(self.heap_array) // 2 + 1, -1, -1):
            self.MinHeapify(i)


class HighHeap(Heap):
    def MaxHeapify(self, i):
        p = self.left(i)
        q = self.right(i)
        if len(self.heap_array) > p and self.heap_array[p] > self.heap_array[i]:
            self.heap_max = p
        else:
            self.heap_max = i
        if len(self.heap_array) > q and self.heap_array[q] > self.heap_array[self.heap_max]:
            self.heap_max = q
        if self.heap_max != i:
            self.heap_array[i], self.heap_array[self.heap_max] = self.heap_array[self.heap_max], \
                                                                 self.heap_array[i]
            self.MaxHeapify(self.heap_max)

    def BuildMaxHeap(self):
        for i in range(len(self.heap_array) // 2 + 1, -1, -1):
            self.MaxHeapify(i)


class Median:
    def __init__(self):
        self.UpperH = HighHeap()
        self.LowerH = LowHeap()

    def add_element(self, value):
        if not self.LowerH.heap_array and not self.UpperH.heap_array:
            self.UpperH.heap_array.append(value)
            self.UpperH.BuildMaxHeap()

        elif value < self.UpperH.heap_array[0]:
            self.LowerH.heap_array.append(value)
            self.LowerH.BuildMaxHeap()

        else:
            self.UpperH.heap_array.append(value)
            self.UpperH.BuildMinHeap()

        if len(self.LowerH.heap_array) - len(self.UpperH.heap_array) == 2:
            difference = self.LowerH.heap_array[0]
            self.UpperH.heap_array.append(difference)
            self.LowerH.heap_array.pop(0)
            self.UpperH.BuildMinHeap()
            self.LowerH.BuildMaxHeap()

        elif len(self.UpperH.heap_array) - len(self.LowerH.heap_array) == 2:
            difference = self.UpperH.heap_array[0]
            self.LowerH.heap_array.append(difference)
            self.UpperH.heap_array.pop(0)
            self.LowerH.BuildMaxHeap()
            self.UpperH.BuildMinHeap()

    def get_maxheap_elements(self):
        return self.UpperH.heap_array

    def get_minheap_elements(self):
        return self.LowerH.heap_array

    def get_median(self):
        if len(self.LowerH.heap_array) == len(self.UpperH.heap_array):
            return self.LowerH.heap_array[0], self.UpperH.heap_array[0]
        elif len(self.LowerH.heap_array) < len(self.UpperH.heap_array):
            return self.UpperH.heap_array[0]
        else:
            return self.LowerH.heap_array[0]
