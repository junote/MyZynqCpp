def hexdump(start, value_list):
    """hexdump

    Args:
        start (uint8): start addr
        value_list (list): value list
    """
    print()
    print("\t ", end="")
    for i in range(16):
        print("%02x" % i, end=" ")
    print()
    print("=" * 60)
    if start % 16 != 0:
        print(" 0x%02x" % ((int(start/16))*0x10), " :", end=" ")
        for i in range(start % 16):
            print("  ", end=" ")
    for i, v in enumerate(value_list):
        if (i+start) % 16 == 0:
            print("\n", "0x%02x" % (i+start), " :", end=" ")
        print("%02x" % v, end=" ")
    print()
    print("=" * 60)
