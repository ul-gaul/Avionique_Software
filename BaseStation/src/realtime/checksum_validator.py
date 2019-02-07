class ChecksumValidator:

    @staticmethod
    def validate(data_array: bytes):
        checksum = sum(data_array) % 256
        if checksum == 255:
            return True
        else:
            print("Invalid Checksum : expected = 255, calculated = {}".format(checksum))
            return False
