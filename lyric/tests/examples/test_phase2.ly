def main() {
    # Collections
    arr mylist = [1, 2, 3, 4, 5]
    print("List:", mylist)
    print("Index 0:", mylist[0])
    print("Index 2:", mylist[2])

    map mymap = {"name": "Lyric", "version": "1.0.4"}
    print("Map:", mymap)
    print("Name:", mymap["name"])

    tup mytup = (10, 20, 30)
    print("Tuple:", mytup)
    print("Tuple[1]:", mytup[1])

    # Slicing
    arr sliced = mylist[1:3]
    print("Sliced:", sliced)

    # Typed declarations
    int x = 42
    str name = "Lyric"
    flt pi = 3.14
    print("Typed:", x, name, pi)

    # In operator
    print("3 in list:", 3 in mylist)
    print("9 in list:", 9 in mylist)
    print("name in map:", "name" in mymap)

    # String operations
    str greeting = "Hello" + " " + "World"
    print(greeting)
    print("Repeat:", "ab" * 3)
}
