class Entry:
    def __init__(self, key, value):
        self.key = key  # the unique ID used to find this record
        self.value = value  # the data being stored (e.g. a Product object)


DELETED = object()  # Marker for slot whose record was deleted


class HashTable:
    MAX_LOAD = 0.7  # grow the table when it reaches 70% full

    def __init__(self, size=101):
        self.size = size  # number of slots in the table
        self.slots = [None] * size  # None means the slot has never been used
        self.count = 0  # number of records currently stored

    def _hash(self, key):
        """Turn a key into a slot number between 0 and size -1."""
        if isinstance(key, int):
            return key % self.size

        if isinstance(key, str):
            h = 0  # start at 0
            for char in key:
                # ord(char) = the character's number code ('A' -> 65)
                # Multiplying by 31 makes the order of letters matter,
                # so "AB" and "BA" usually land in different slots.
                h = (h * 31 + ord(char)) % self.size
            return h

        raise TypeError("Key must be an integer or a string.")

    def _probe(self, key):
        """Give slot numbers to try, in linear-probing order"""
        index = self._hash(key)
        for _ in range(self.size):
            yield index  # hand back one slot number
            index = (index + 1) % self.size  # move to the next slot

    def _find(self, key):
        """Return slot number holding 'key', or None if key is not stored."""
        for index in self._probe(key):
            slot = self.slots[index]
            if slot is None:  # empty slot -> key not in table
                return None
            if slot is not DELETED and slot.key == key:
                return index  # found it
            # otherwise: a different key or a tombstone -> keep probing
        return None

    def insert(self, key, value):
        """Add a record (or update it if the key exists). Returns its slot."""
        index = self._find(key)
        if index is not None:
            self.slots[index].value = value
            return index

        # Grow first if this insert would make the table too full.
        if (self.count + 1) / self.size > self.MAX_LOAD:
            self._resize()

        # Use the first free slot: never used (None) or deleted (DELETED).
        for index in self._probe(key):
            slot = self.slots[index]
            if slot is None or slot is DELETED:
                self.slots[index] = Entry(key, value)
                self.count = self.count + 1
                return index

        # Can't happen, because _resize keeps the table below 70% full.
        raise RuntimeError("Hash table is full")

    def search(self, key):
        """Return the value stored for 'key', or None if not found."""
        index = self._find(key)
        if index is None:
            return None
        return self.slots[index].value

    def delete(self, key):
        """Remove 'key'. Returns True if removed, False if it wasn't there."""
        index = self._find(key)
        if index is None:
            return False
        self.slots[index] = DELETED  # tombstone keeps the probe chain intact
        self.count = self.count - 1
        return True

    def _resize(self):
        """Roughly double the size and re-insert every record (rehashing)."""
        old_slots = self.slots
        self.size = self.size * 2 + 1  # 5 -> 11 -> 23 -> 47 ...
        self.slots = [None] * self.size
        self.count = 0
        for slot in old_slots:
            if slot is not None and slot is not DELETED:
                # Slot numbers change because _hash uses the new size.
                self.insert(slot.key, slot.value)

    def load_factor(self):
        """How full the table is, from 0.0 (empty) to 1.0 (full)."""
        return self.count / self.size

    def display(self):
        """Print every slot so collisions and probing are easy to see."""
        print(f"  Table size: {self.size} | Records: {self.count} | "
              f"Load factor: {self.load_factor():.2f}")
        for i, slot in enumerate(self.slots):
            if slot is None:
                text = "-"  # never used
            elif slot is DELETED:
                text = "<DELETED>"  # tombstone
            else:
                home = self._hash(slot.key)  # where it wanted to go
                moved = "" if home == i else f"   (home {home}, moved by probing)"
                text = f"{slot.key} -> {slot.value}{moved}"
            print(f"  [{i:>2}] {text}")

    def items(self):
        """Give back (key, value) for every real record, skipping empty and deleted slots."""
        for slot in self.slots:
            if slot is not None and slot is not DELETED:
                yield slot.key, slot.value


if __name__ == "__main__":
    ht = HashTable(5)

    print("=== TEST 1: Insert with collisions ===")
    print("1042, 1047 and 1052 all have home slot 2 (ID % 5 = 2)")
    for key, med in [(1042, "Panadol"), (1047, "Ibuprofen"), (1052, "Aspirin")]:
        slot = ht.insert(key, med)
        print(f"  Inserted {key} ({med}) into slot {slot}")
    ht.display()

    print("\n=== TEST 2: Search ===")
    for key in [1047, 9999]:
        result = ht.search(key)
        print(f"  Search {key}: {result if result is not None else 'Not found'}")

    print("\n=== TEST 3: Text keys ===")
    for key in ["MED001", "MED002", "DEM001"]:
        print(f"  Home slot of {key} (in the {ht.size}-slot table): {ht._hash(key)}")

    print("\n=== TEST 4: Table grows when over 70% full ===")
    print(f"  Before: size {ht.size}, {ht.count} records")
    for code in ["MED001", "MED002", "MED003", "MED004"]:
        ht.insert(code, "Medicine " + code)
    print(f"  After inserting 4 more: size {ht.size}, {ht.count} records")
    ht.display()

    print("\n=== TEST 5: Delete keeps the probe chain working ===")
    print("  In the 11-slot table, 1047 is in slot 2 (its home slot).")
    print("  MED002 also has home slot 2, so it was probed to slot 3.")
    print("  If we delete 1047, can search still find MED002?")
    print(f"  Delete 1047: {'Deleted' if ht.delete(1047) else 'Not found'}")
    result = ht.search('MED002')
    status = "still found" if result is not None else "LOST - tombstone not working!"
    print(f"  Search MED002 after delete: {result}  <- {status}")
    print(f"  Delete 1047 again: {'Deleted' if ht.delete(1047) else 'Not found'}")
    ht.display()