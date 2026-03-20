data = {}
file_path = 'info.log'
with open(file_path, "r") as f:
    for line in f:
        key, value, v2 = line.strip().split('|', 2)
        data[key.strip()] = value.strip()
        print(data)
        break
        

    #rows = [r for r in reader if any(field.strip() for field in r)]
