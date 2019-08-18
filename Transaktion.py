class Transaction:

    def __init__(self, from_: str, to: str, amount: float):
        self.from_ = from_
        self.to = to
        self.amount = amount

    def __str__(self):
        return "{} überweist {} {:.2f}€".format(self.from_, self.to, self.amount)
