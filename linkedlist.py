import time
from random import randint


class LinkedList:
    # The __Node class is used internally by the LinkedList class. It is
    # invisible from outside this class due to the two underscores
    # that precede the class name. Python mangles names so that they
    # are not recognizable outside the class when two underscores
    # precede a name but aren't followed by two underscores at the
    # end of the name (i.e. an operator name).
    class __Node:
        def __init__(self, item, next=None):
            self.item = item
            self.next = next

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

    def __init__(self, contents=None):
        # Here we keep a reference to the first node in the linked list
        # and the last item in the linked list. The both point to a
        # dummy node to begin with. This dummy node will always be in
        # the first position in the list and will never contain an item.
        # Its purpose is to eliminate special cases in the code below.
        if contents is None:
            contents = []
        self.first = LinkedList.__Node(None, None)
        self.last = self.first
        self.numItems = 0

        for e in contents:
            self.append(e)

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext()
            for i in range(index):
                cursor = cursor.getNext()

            return cursor.getItem()

        raise IndexError("LinkedList index out of range")

    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext()
            for i in range(index):
                cursor = cursor.getNext()

            cursor.setItem(val)
            return

        raise IndexError("LinkedList assignment index out of range")

    def insert(self, index, item):
        cursor = self.first

        if index < self.numItems:
            for i in range(index):
                cursor = cursor.getNext()

            node = LinkedList.__Node(item, cursor.getNext())
            cursor.setNext(node)
            self.numItems += 1
        else:
            self.append(item)

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Concatenate undefined for " + \
                            str(type(self)) + " + " + str(type(other)))

        result = LinkedList()

        cursor = self.first.getNext()

        while cursor != None:
            result.append(cursor.getItem())
            cursor = cursor.getNext()

        cursor = other.first.getNext()

        while cursor != None:
            result.append(cursor.getItem())
            cursor = cursor.getNext()

        return result

    def __contains__(self, item):
        for i in self:
            if i == item:
                return True
        return False

    def __delitem__(self, index):
        cursor = self.first.getNext()
        for i in range(index - 1):
            cursor = cursor.getNext()
        cursor.setNext(cursor.getNext().getNext())
        self.numItems -= 1

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if self.numItems != other.numItems:
            return False

        cursor1 = self.first.getNext()
        cursor2 = other.first.getNext()
        while cursor1 != None:
            if cursor1.getItem() != cursor2.getItem():
                return False
            cursor1 = cursor1.getNext()
            cursor2 = cursor2.getNext()

        return True

    def __iter__(self):
        cursor = self.first.getNext()
        while cursor is not None:
            yield cursor.getItem()
            cursor = cursor.getNext()

    def __len__(self):
        return self.numItems

    def append(self, item):
        node = LinkedList.__Node(item)
        self.last.setNext(node)
        self.last = node
        self.numItems += 1

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        # This is left as an exercise for the reader.
        return f"LinkedList({list(self).__repr__()})"

    def split(self, index):
        new_lst = LinkedList()

        cursor = self.first

        for i in range(index):
            cursor = cursor.getNext()

        new_lst.first.setNext(cursor.getNext())
        cursor.setNext(None)

        new_lst.numItems = self.numItems - index
        self.numItems = index

        return new_lst

    def merge(self, lst, by=lambda a, b: a < b):
        self_cursor = self.first.getNext()
        lst_cursor = lst.first.getNext()
        new_lst = LinkedList()

        while (self_cursor is not None) and (lst_cursor is not None):
            if by(self_cursor.getItem(), lst_cursor.getItem()):
                new_lst.append(self_cursor.getItem())
                self_cursor = self_cursor.getNext()
            else:
                new_lst.append(lst_cursor.getItem())
                lst_cursor = lst_cursor.getNext()

        while self_cursor is not None:
            new_lst.append(self_cursor.getItem())
            self_cursor = self_cursor.getNext()

        while lst_cursor is not None:
            new_lst.append(lst_cursor.getItem())
            lst_cursor = lst_cursor.getNext()

        self.first = new_lst.first
        self.last = new_lst.last
        self.numItems = new_lst.numItems

    def merge_sort(self):
        if self.numItems == 1:
            return list

        other = self.split(self.numItems // 2)

        self.merge_sort()
        other.merge_sort()

        self.merge(other)


def generate_random_list(length):
    return LinkedList([randint(0, length) for i in range(length)])


def main():
    li = generate_random_list(20000)
    li.merge_sort()
    print(li)

    results = []
    for length in range(100, 100000 + 100, 100):
        random_list = generate_random_list(length)
        print(f"Generating list of length {length}")
        t = time.perf_counter()
        random_list.merge_sort()
        results.append((length, time.perf_counter() - t))

    with open('results.csv', 'w') as f:
        f.write("length,time\n")
        for result in results:
            f.write(f"{result[0]},{result[1]}\n")

    # lst = LinkedList()
    #
    # for i in range(100):
    #     lst.append(i)
    #
    # lst2 = LinkedList(lst)
    #
    # print(len(lst))
    # print(len(lst2))
    #
    # if lst == lst2:
    #     print("Test 1 Passed")
    # else:
    #     print("Test 1 Failed")
    #
    # lst3 = lst + lst2
    #
    # if len(lst3) == len(lst) + len(lst2):
    #     print("Test 2 Passed")
    # else:
    #     print("Test 2 Failed")
    #
    # if 1 in lst3:
    #     print("Test 3 Passed")
    # else:
    #     print("Test 3 Failed")
    #
    # if 2 in lst3:
    #     print("Test 4 Passed")
    # else:
    #     print("Test 4 Failed")
    #
    # del lst[1]
    #
    # if 1 in lst:
    #     print("Test 5 Failed")
    # else:
    #     print("Test 5 Passed")
    #
    # if len(lst) == 99:
    #     print("Test 6 Passed")
    # else:
    #     print("Test 6 Failed")
    #
    # if lst == lst2:
    #     print("Test 7 Failed")
    # else:
    #     print("Test 7 Passed")
    #
    # del lst2[2]
    #
    # if lst == lst2:
    #     print("Test 8 Failed")
    # else:
    #     print("Test 8 Passed")
    #
    # lst4 = LinkedList(lst)
    # lst.insert(0, 100)
    # lst4 = LinkedList([100]) + lst4
    #
    # if lst == lst4:
    #     print("Test 9 Passed")
    # else:
    #     print("Test 9 Failed")
    #
    # lst.insert(1000, 333)
    # lst4.append(333)
    #
    # if lst == lst4:
    #     print("Test 10 Passed")
    # else:
    #     print("Test 10 Failed")
    #
    # print(lst)
    # print(lst4)


if __name__ == "__main__":
    main()
