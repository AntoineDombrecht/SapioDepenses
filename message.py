

class Message:
    def display(self, out, message):
        with out:
            out.clear_output()
            print(message)