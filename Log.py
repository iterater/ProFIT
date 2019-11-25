import pandas as pd

class Log(object):
    
    def __init__(self, data_path, cols=(0,1), *args, **kwargs):
        log = pd.read_csv(data_path, usecols=cols, *args, **kwargs)
        log.columns = ['case_id', 'activity']
        log.set_index('case_id', drop=True, inplace=True)
        self.flat_log = dict(log.activity.groupby(level=0).agg(tuple))
        self.cases = set(log.index)
        self.activities = set(log.activity)
    
    def transit_matrix(self):
        T = dict()
        to_add = dict()
        for case_id in self.flat_log:
            for i in range(len(self.flat_log[case_id]) - 1):
                a_i = self.flat_log[case_id][i]
                a_j = self.flat_log[case_id][i+1]
                if a_i not in T:
                    T[a_i] = dict()
                    to_add[a_i] = dict()
                if a_j not in T[a_i]:
                    T[a_i][a_j] = [0, 0]
                    to_add[a_i][a_j] = True
                T[a_i][a_j][0] += 1
                if to_add[a_i][a_j]:
                    T[a_i][a_j][1] += 1
                    to_add[a_i][a_j] = False
            for a_i in to_add:
                for a_j in to_add[a_i]:
                    to_add[a_i][a_j] = True
        for a_i in T:
            for a_j in T[a_i]:
                T[a_i][a_j] = tuple(T[a_i][a_j])
        return T