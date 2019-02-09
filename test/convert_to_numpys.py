import pandas as pd
import pickle


class DataHandler:
    def __init__(self, player_pkl, club_pkl, transfer_pkl):
        self.player_pkl = player_pkl
        self.club_pkl = club_pkl
        self.transfer_pkl = transfer_pkl

    def get_pickle(self, filename):
        all_dicts = []
        with open(filename, 'rb') as handle:
            try:
                while True:
                    all_dicts.append(pickle.load(handle, encoding='utf-8'))
            except EOFError:
                print("------- End of file -------")
        return all_dicts

    def format_player_data_frame(self, df):
        temp_data_frame = df
        df = df.drop('teams_played_for', 1)
        df = pd.get_dummies(df, columns=['position', 'age'])
        teams_played_for_df = temp_data_frame['teams_played_for'].str.join(sep='*').str.get_dummies(sep='*')
        df = pd.concat([df, teams_played_for_df], axis=1)
        return df

    def get_data_frames(self):
        players = self.get_pickle(self.player_pkl)
        clubs = self.get_pickle(self.club_pkl)
        transfers = self.get_pickle(self.transfer_pkl)

        player_data_frame = pd.DataFrame(players)
        clubs_data_frame = pd.DataFrame(clubs)
        transfers_data_frame = pd.DataFrame(transfers)
        transfers_data_frame.rename(columns={'rumoured_club': 'club'}, inplace=True)
        player_data_frame = self.format_player_data_frame(player_data_frame)
        # clubs_data_frame = pd.get_dummies(clubs_data_frame, columns=['capacity'])
        return player_data_frame, clubs_data_frame, transfers_data_frame

    def merge_df(self, first_df, second_df, key):
        return pd.merge(left=first_df, right=second_df, left_on=key, right_on=key)

    def drop_column(self, df, column):
        return df.drop(column, 1)










