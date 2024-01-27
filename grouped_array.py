def group_by_pattern(array, pattern):
    grouped_array = []
    group = []

    for element in array:
        if element.startswith(pattern):
            if group:
                grouped_array.append(group)
                group = []
            group.append(element)
        else:
            group.append(element)

    if group:
        grouped_array.append(group)

    return grouped_array

# Test the function
array = ['BRK1', 'item1', 'item2', 'BRK2', 'item3', 'BRK3', 'item4', 'item5']
pattern = 'BRK'
print(group_by_pattern(array, pattern))