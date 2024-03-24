class Utils:

    @staticmethod
    def read_int_multy_array_form_file(level_number: int):
        path = "resources/levels/level " + str(level_number)
        try:
            with open(path) as file:
                lst = file.readlines()
                if not lst:
                    raise ValueError("File is empty")
                for line in lst:
                    if not line.strip():
                        raise ValueError("Invalid format: empty lines")
                    try:
                        [int(n) for n in line.split()]
                    except ValueError:
                        raise ValueError("Invalid format: non-integer values")
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        return [[int(n) for n in x.split()] for x in lst]