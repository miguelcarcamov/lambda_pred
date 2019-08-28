def visualization():
    path = input("Enter file path: ")

    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]
        print(row)
