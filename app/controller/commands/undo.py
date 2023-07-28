from app import app
from app.controller.console import command
from app.model.transaction import TM, Transaction


@command(name="undo", shortcut="ctrl+z")
def undo():
    print("--- UNDO ---")


    last_transaction: Transaction = TM.get_history()[-1]

    for transaction in TM.get_history():
        print("Transaction: {}".format(transaction.name))

    actions = last_transaction.get_actions()

    print("Actions: {}".format(len(actions)))
    for action in actions:
        print(action)

    TM.history_undo()
