class Utils:

    @staticmethod
    def read_int_multy_array_form_file(level_number: int):
        path = "resources/levels/level " + str(level_number)
        with open(path) as file:
            lst = file.readlines()
        return [[int(n) for n in x.split()] for x in lst]