import pickle


with open('transfer_tup.pickle', 'rb') as handle:
    transfers = []
    try:
        while True:
            transfers.append(pickle.load(handle, encoding='utf-8'))
    except EOFError:
        print("------- End of file -------")

no_of_transfers = len(transfers)
max_no_transfers = 1546
total_transfers = max_no_transfers * 2
no_of_trues = 0
no_of_false = 0
dict_iterator = 0
with open('transfer_new.pickle', 'wb') as writer:
    while no_of_trues + no_of_false < total_transfers:
        if transfers[dict_iterator]['successful'] & no_of_trues < max_no_transfers:
            pickle.dump(transfers[dict_iterator], writer, protocol=pickle.HIGHEST_PROTOCOL)
            no_of_trues += 1
        elif not transfers[dict_iterator]['successful'] & no_of_false < max_no_transfers:
            pickle.dump(transfers[dict_iterator], writer, protocol=pickle.HIGHEST_PROTOCOL)
            no_of_false += 1
        dict_iterator += 1
