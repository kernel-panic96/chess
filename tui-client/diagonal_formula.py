for i in range(8):
    print(' '.join(map(str, ((i + j) for j in range(8)))))

for i in range(8):
    print(' '.join(map(str, ((i - j) for j in range(8)))))
