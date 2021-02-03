from app import app


class ModelReg(dict):
    def __init__(self):
        super().__init__()

    def get_all_bars(self):
        return self.get("Bar", {})

    def get_bars(self):
        for model_id in self["Bar"]:
            yield self["Bar"][model_id]

    def get_bar_count(self):
        return len(self["Bar"])

    def get_nodes(self):
        for model_id in self["Node"]:
            yield self["Node"][model_id]

    def get_node_count(self):
        return len(self["Node"])




app.model_reg = ModelReg()


