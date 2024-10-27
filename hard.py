import random

key = (2*random.randint(0, 2**79) + 1)
flag = 'ctfcup{'+ hex(key) +'}'
print(flag)

M = 2**80
t = lambda x: (148*x + 337)*x
f = lambda x0,x1,x2,x3: (x0*x1 + x1*x3 + x0*x1*x3 + x3 + x0*x2) % 2

stream = []
for i in range(700):
    key = t(key) % M
    hint_index = random.choice(range(0, 80, 4))
    for i in range(0, 80, 4):
        sub = (key >> i) % 2**4
        if i == hint_index:
            stream.append(sub)
        else:
            x0, x1, x2, x3 = sub&1, (sub>>1)&1, (sub>>2)&1, (sub>>3)&1
            stream.append(f(x0,x1,x2,x3))

open('output.txt','w').write(f'{stream = }\n')

# Восстановление ключа
def recover_key(hex_value):
    return int(hex_value, 16)

# Восстановление потока
def reverse_stream(key, stream):
    M = 2**80
    t = lambda x: (148 * x + 337) * x
    f = lambda x0, x1, x2, x3: (x0 * x1 + x1 * x3 + x0 * x1 * x3 + x3 + x0 * x2) % 2

    recovered_stream = []
    hint_index = random.choice(range(0, 80, 4))

    for _ in range(700):
        key = t(key) % M
        for i in range(0, 80, 4):
            sub = (key >> i) % 2**4
            if i == hint_index:
                recovered_stream.append(sub)
            else:
                x0, x1, x2, x3 = sub & 1, (sub >> 1) & 1, (sub >> 2) & 1, (sub >> 3) & 1
                # Обратное вычисление f
                # Поскольку f — это функция, обратную не найти просто,
                # но можно оценить значения x0, x1, x2, x3, чтобы получить sub
                recovered_sub = (x0 * x1 + x1 * x3 + x0 * x1 * x3 + x3 + x0 * x2) % 2
                recovered_stream.append(recovered_sub)

    return recovered_stream

# Пример использования
hex_key = "0x123456789abcdef"  # Замените на ваш hex ключ
key = recover_key(hex_key)

# Пример стрима, замените на ваш поток
stream = [1, 0, 0, 1, 1, 0]  # Замените на фактические значения стрима
recovered_stream = reverse_stream(key, stream)

# Запись результата
with open('recovered_output.txt', 'w') as f:
    f.write(f'{recovered_stream}\n')

print("Recovered stream:", recovered_stream)
