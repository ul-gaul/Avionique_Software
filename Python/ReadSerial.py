import serial

ser = serial.Serial(
    port = "/dev/ttyUSB0",
)
while True:
    data = str(ser.readline())
    """code_data = []
    for letter in data:

        code_data += [letter]

        for alpha in code_data:
            if alpha.isalpha() == True:
                code_data.remove(alpha)

            elif alpha == "\'":
                code_data.remove(alpha)

            elif alpha == "\\":
                code_data.remove(alpha)

            num = ""

            for i in code_data:
                num += i
    print(float(num))"""
    print(data)