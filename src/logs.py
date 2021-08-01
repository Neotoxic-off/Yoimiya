class LOGS:
    data = {
        "reset" : "0",
        "red" : "31",
        "green" : "32",
        "yellow" : "33",
        "blue" : "34",
        "purple" : "35",
        "cyan" : "36",
        "white" : "37"
    }

    @classmethod
    def colors(cls, color, font):
        if (cls.data.get(color) != None and (font >= 0 and font <= 5)):
            return ("\033[{};{}m".format(font, cls.data.get(color)))
        return (None)

    @classmethod
    def status(cls, data, status, color, font, mod):
        if (mod == 0):
            print("{}{}{}{}".format(
                cls.colors(color, font),
                status,
                data,
                cls.colors("reset", 0)
            ))
        if (mod == 1):
            print("{}[ {} ]{} {}".format(
                cls.colors(color, font),
                status,
                cls.colors("reset", 0),
                data
            ))
        if (mod == 2):
            print("{}{}{}".format(
                cls.colors(color, font),
                data,
                cls.colors("reset", 0)
            ))


    @classmethod
    def ok(cls, data):
        cls.status("==> {}".format(data), "  OK  ", "white", 0, 2)

    @classmethod
    def ko(cls, data):
        cls.status(data, "  KO  ", "red", 0, 2)

    @classmethod
    def done(cls, data):
        cls.status(data, " DONE ", "green", 0, 2)

    @classmethod
    def fail(cls, data):
        cls.status(data, " FAIL ", "red", 0, 2)

    @classmethod
    def warning(cls, data):
        cls.status("   missing: {}".format(data), " WARN ", "purple", 0, 2)

    @classmethod
    def missing(cls, data):
        cls.status(data, "CONFIG", "purple", 0, 2)

    @classmethod
    def load(cls, data):
        cls.status("{}::{} {}".format(cls.colors("cyan", 1), cls.colors("white", 1), data), " ---- ", "yellow", 0, 2)

    @classmethod
    def display(cls, data):
        cls.status(data, "=====>", "green", 0, 2)
    
    @classmethod
    def item_load(cls, data):
        cls.status("\t{}".format(data), '-->', "white", 1, 2)

    @classmethod
    def item_method(cls, data):
        cls.status("\t    ---> {}".format(data), '-->', "cyan", 0, 2)

    @classmethod
    def item(cls, data):
        cls.status("\t{}".format(data), "-->", "green", 0, 2)

    @classmethod
    def empty_item(cls, data):
        cls.status("\t{}".format(data), "-->", "red", 0, 2)

