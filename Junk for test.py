groups = [{0: 'a', 1: 'a'}, {0: 'a', 1: 'a'}]
groups[0][len(groups[0])] = []
print(groups)
for group_id, group in enumerate(groups):
    if groups[group_id][len(groups[group_id]) - 1]:
        print(groups[group_id])
        print(len(groups[group_id]))
        groups[group_id][2] = []

        groups[group_id][len(groups[group_id])] = []
        print(groups)
