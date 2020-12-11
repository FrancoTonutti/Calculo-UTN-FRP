from app import app


class ModelReg(dict):
    def __init__(self):
        super().__init__()

    def get_all_bars(self):
        return self.get("Bar", {})

    def get_bars(self):
        for model_id in self["Bar"]:
            yield self["Bar"][model_id]




app.model_reg = ModelReg()


