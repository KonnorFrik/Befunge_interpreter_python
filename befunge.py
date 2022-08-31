from random import randint
from sys import argv
from actions import Action
from modes import Mode


class Befunge93:
    DEBUG = Mode.DEBUG_OFF

    def __init__(self, program_string: str = ""):
        self.work_mode = Mode.work_normal

        self.is_modified = False
        self.is_work = True

        self.row = 0
        self.column = 0
        self.program_pointer = [self.row, self.column]
        self.program_strings = [list(row) for row in list(program_string.split('\n'))]
        self.current_char = None
        self.move_direction = Action.Right
        self.stack = list()
        self.result = str()

        self.actions = {
            Action.Right: self.change_move_direction,
            Action.Left: self.change_move_direction,
            Action.Up: self.change_move_direction,
            Action.Down: self.change_move_direction,
            Action.Random: self.random_move,
            Action.Right_if: self.compare_and_change_move,
            Action.Down_if: self.compare_and_change_move,
            Action.Add: self.math,
            Action.Sub: self.math,
            Action.Mul: self.math,
            Action.Div: self.math,
            Action.Module_div: self.math,
            Action.Log_not: self.logical,
            Action.Greater_then: self.compare,
            Action.String_mode: self.get_all_string,
            Action.Duplicate: self.duplicate,
            Action.Swap: self.swap_two,
            Action.Discard: self.discard,
            Action.Print_int: self.output_add,
            Action.Print_char: self.output_add,
            Action.Skip_next: self.skip_next,
            Action.Ask_number: self.ask_user,
            Action.Ask_char: self.ask_user,
            Action.Nothing: self.nothing,
            Action.Exit: self.exit,
            Action.Put: self.put,
            Action.Get: self.get,
            Action.Jump: self.jump,
        }
        self.message = {
            Action.Ask_char: "Enter a one character",
            Action.Ask_number: "Enter a one number",
        }

    def get_output(self):
        return self.result

    def run(self):
        try:
            while self.is_work:

                self.current_char = self.program_strings[self.program_pointer[0]][self.program_pointer[1]]

                if self.DEBUG == Mode.DEBUG_FULL:
                    print(f"\n\n\n[*] Main Cycle")
                    print(f"Choose a new char is: {self.current_char}")

                elif self.DEBUG == Mode.DEBUG_STACK:
                    print(f"\n\n\n[*] For Action: {self.current_char}")
                    print(f"Stack state is: {self.stack}")

                if self.current_char.isdigit():
                    if self.DEBUG == Mode.DEBUG_FULL:
                        print(f"Chose char is a digit")
                    self._push(int(self.current_char))
                    self.move()
                    continue

                try:
                    if self.DEBUG == Mode.DEBUG_FULL:
                        print(f"Choose an Action: {self.actions[self.current_char]}")
                    self.actions[self.current_char]()
                except KeyError:
                    print(f"\n\t[!!!]ERROR in call action")
                    print(f"Current char is: {self.current_char}")

                self.move()

        except IndexError:
            if self.DEBUG == Mode.DEBUG_ERROR:
                print(f"ERROR: Last pointer value: {self.program_pointer}")
        except Exception as e:
            if self.DEBUG == Mode.DEBUG_ERROR:
                print(f"Found Some Error: {e}")

    @staticmethod
    def step_wait():
        input("Wait..")

    def reinit_data(self):
        self.row = 0
        self.column = 0
        self.program_pointer = [self.row, self.column]
        self.move_direction = Action.Right
        self.result = ""
        self.stack.clear()
        self.current_char = None

    def load_new_program(self, program_strings: str):
        self.program_strings = [list(row) for row in list(program_strings.split('\n'))]
        self.reinit_data()

    def move(self):
        if self.work_mode == Mode.work_step:
            self.step_wait()

        if self.move_direction == Action.Right:
            self.move_right()
        elif self.move_direction == Action.Left:
            self.move_left()
        elif self.move_direction == Action.Up:
            self.move_up()
        elif self.move_direction == Action.Down:
            self.move_down()

        self._update_pointer()

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Move Func")
            print(f"After move new pos\trow: {self.row}\tcolumn: {self.column}")

    def move_right(self):
        self.column += 1

    def move_left(self):
        self.column -= 1

    def move_down(self):
        self.row += 1

    def move_up(self):
        self.row -= 1

    def change_move_direction(self):
        if self.current_char == Action.Right:
            self.move_direction = Action.Right

        elif self.current_char == Action.Left:
            self.move_direction = Action.Left

        elif self.current_char == Action.Up:
            self.move_direction = Action.Up

        elif self.current_char == Action.Down:
            self.move_direction = Action.Down

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Change move direction Func")
            print(f"Direction now is: {self.move_direction}")

    def random_move(self):
        direction_num = randint(1, 4)
        if direction_num == 1:
            self.move_direction = Action.Up

        elif direction_num == 2:
            self.move_direction = Action.Right

        elif direction_num == 3:
            self.move_direction = Action.Down

        elif direction_num == 4:
            self.move_direction = Action.Left

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Random move Func")
            print(f"Direction now is: {self.move_direction}")

    def _update_pointer(self):
        self.program_pointer = self.row, self.column

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n\t[->] Program pointer updated")

    def _push(self, obj: int):
        self.stack.append(obj)

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Push Func")
            print(f"Item for push: {obj}\titem type: {type(obj)}")
            print(f"Stack state is: {self.stack}")

        elif self.DEBUG == Mode.DEBUG_STACK:
            print(f"\n[*] Push item: {obj}")

    def _pop(self) -> int:
        try:
            value = self.stack.pop()
        except IndexError:
            value = 0

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Pop Func")
            print(f"\n[*] Pop item: {value}")
            print(f"Stack state is: {self.stack}")

        elif self.DEBUG == Mode.DEBUG_STACK:
            print(f"\n[*] Pop item: {value}")

        return value

    def _look_stack_top(self) -> int:
        try:
            value = self.stack[-1]
        except IndexError:
            value = 0

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Look stack top Func")
            print(f"Stack state is: {self.stack}")
            print(f"Stack top is: {value}")

        elif self.DEBUG == Mode.DEBUG_STACK:
            print(f"\n[*] Stack top is: {value}")

        return value

    def compare_and_change_move(self):
        value = self._pop()
        if self.current_char == Action.Right_if:
            if value == 0:
                self.move_direction = Action.Right
            else:
                self.move_direction = Action.Left

        elif self.current_char == Action.Down_if:
            if value == 0:
                self.move_direction = Action.Down
            else:
                self.move_direction = Action.Up

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Compare and change move Func")
            print(f"Value for compare: {value}")
            print(f"Move direction after compare is: {self.move_direction}")

    def compare(self):
        first = self._pop()
        second = self._pop()

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Compare Func")
            print(f"First value: {first}")
            print(f"Second value: {second}")
            print(f"Make compare: {second} > {first}")

        if second > first:
            self._push(1)
        else:
            self._push(0)

    def math(self):
        first = self._pop()
        second = self._pop()
        result_ = None

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Math Func")
            print(f"First value: {first}")
            print(f"Second value: {second}")

        if self.current_char == Action.Add:
            result_ = int(first) + int(second)

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Make: {first} + {second} = {result_}")

        elif self.current_char == Action.Sub:
            result_ = int(second) - int(first)

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Make: {second} - {first} = {result_}")

        elif self.current_char == Action.Mul:
            result_ = int(first) * int(second)

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Make: {first} * {second} = {result_}")

        elif self.current_char == Action.Div:
            result_ = round(int(second) / int(first))

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Make: {second} / {first} = {result_}")

        elif self.current_char == Action.Module_div:
            result_ = int(second) % int(first)

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Make: {second} % {first} = {result_}")

        self._push(result_)

    def logical(self):
        if self.current_char == Action.Log_not:
            value = self._pop()

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"\n[*] Logical Func")
                print(f"Value for action: {value}")
                print(f"Make: not {value} = {not value}")

            if value == 0:
                self._push(1)
            else:
                self._push(0)

    def get_all_string(self):
        self.move()

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Get all string Func")

        while self.program_strings[self.program_pointer[0]][self.program_pointer[1]] != Action.String_mode:
            self.current_char = self.program_strings[self.program_pointer[0]][self.program_pointer[1]]

            if self.DEBUG == Mode.DEBUG_FULL:
                print(f"Get char: {self.current_char}")

            self._push(ord(self.current_char))
            self.move()

    def duplicate(self):
        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Duplicate Func")

        self._push(self._look_stack_top())

    def swap_two(self):
        first = self._pop()
        second = self._pop()

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*]Swap two Func")
            print(f"First value: {first}")
            print(f"Second value: {second}")

        self._push(first)
        self._push(second)

    def discard(self):
        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Discard Func")

        self._pop()

    def output_add(self):
        value = None

        if self.current_char == Action.Print_char:
            value = chr(self._pop())

        elif self.current_char == Action.Print_int:
            value = str(self._pop())

        self.result += value

        if value == '\n':
            print(self.result)
            self.result = ''

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Output add Func")
            print(f"Get char") if self.current_char == Action.Print_char else print(f"Get int")
            print(f"Value from stack: {value}")
            print(f"Output is: {self.result}")

    def skip_next(self):
        self.move()

    def ask_user(self):
        print(self.message[self.current_char])
        value = input("~>")

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Ask user Func")
            print(f"Need character") if self.current_char == Action.Ask_char else print(f"Need int")
            print(f"Get input: {value} - {type(value)}")

        if self.current_char == Action.Ask_char:
            self._push(ord(value))
        elif self.current_char == Action.Ask_number:
            self._push(int(value))

    def put(self):
        row = self._pop()
        column = self._pop()
        ascii_symbol = chr(self._pop())

        previous = self.program_strings[row][column]    # just for debug

        self.program_strings[row][column] = ascii_symbol

        self.is_modified = True

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Put Func")
            print(f"The symbol: '{previous}' on coords: {row=}, {column=} changed to: {ascii_symbol}")

    def get(self):
        row = self._pop()
        column = self._pop()
        ascii_code = ord(self.program_strings[row][column])
        self._push(ascii_code)

        self.is_modified = True

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Get Func")
            print(f"The symbol: '{self.program_strings[row][column]}' on coords: {row=}, {column=} pushed to stack")
            print(f"Ascii code of symbol: {ascii_code}")

    def jump(self):
        row = self._pop()
        column = self._pop()
        self.row = row
        self.column = column
        self._update_pointer()

        if self.DEBUG == Mode.DEBUG_FULL:
            print(f"\n[*] Jump Func")
            print(f"Make jump to coords: {row=}, {column=}")
            print(f"On symbol: {self.program_strings[row][column]}")
            print(f"With direction: {self.move_direction}")
            print(f"Program pointer now is: {self.program_pointer}")

    def nothing(self):
        pass

    def exit(self):
        if self.is_modified:
            self.new_code = '\n'.join([''.join(symb) for symb in self.program_strings])
        print(self.get_output())
        self.is_work = False


def start_work(mode_: str, program_code: str):
    file_name = None
    if mode_ == Mode.file_input:
        file_name = program_code
        with open(program_code, 'r') as file:
            program_code = file.read()
    elif mode_ == Mode.string_input:
        file_name = 'New_Code.bf'

    interpreter = Befunge93(program_string=program_code)
    interpreter.run()

    if interpreter.is_modified:
        new_file_name = file_name.split('.')
        new_file_name[0] = new_file_name[0] + '_output'
        new_file_name = '.'.join(new_file_name)

        with open(new_file_name, 'w') as file:
            file.write(interpreter.new_code)

        print(f"Program was modified")
        print(f"Write it to: {new_file_name}")
        print(f"New program:\n{interpreter.new_code}")


if __name__ == "__main__":
    mode = argv[1]
    code = argv[2]
    start_work(mode, code)
