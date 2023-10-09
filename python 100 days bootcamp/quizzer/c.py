word = "PROGRAM"
length = len(word)

# Ensure the word has an odd number of letters
if length % 2 == 0:
    print("Word must have an odd number of letters.")
else:
    # Calculate the middle index
    mid = length // 2

    # Print the top half of the diamond
    for i in range(mid + 1):
        for j in range(mid - i + 1):
            print(" ", end="")
        print(word[mid - i], end=" ")
        for j in range(2 * i):
            print(" ", end="")
        if i != 0:  # Avoid printing the middle letter twice
            print(word[mid + i], end="")
        print()

    # Print the bottom half of the diamond
    for i in range(mid - 1, -1, -1):
        for j in range(mid - i + 1):
            print(" ", end="")
        print(word[mid - i], end=" ")
        for j in range(2 * i):
            print(" ", end="")
        if i != 0:  # Avoid printing the middle letter twice
            print(word[mid + i], end="")
        print()
