import pandas as pd

def get_tidy_df(xls_file, designated_sheet=0):
    """
    Getting tidy dataframe from CEC
    """
    df = pd.read_excel(xls_file, skiprows=2, header=0,
                       sheet_name=designated_sheet)
    n_cols = df.shape[1]
    n_candidates = n_cols - 11
    print("候選人人數：{}".format(n_candidates))
    candidates = list(df.columns[3:(3+n_candidates)])
    numbers = [cand.split("\n")[0] for cand in candidates]
    parties = [cand.split("\n")[2] for cand in candidates]
    parties = ["無黨籍" if x == ' ' else x for x in parties]
    candidates = [cand.split("\n")[1] for cand in candidates]
    candidates = ["{} {} {}".format(number, party, candidate)
                  for number, party, candidate in zip(numbers, parties, candidates)]
    print("候選人姓名：")
    for cand in candidates:
        print("{}".format(cand))
    df = pd.read_excel(xls_file, skiprows=5, header=None,
                       sheet_name=designated_sheet)
    cols_to_drop = [3, 5, 6, 9, 10]
    cols_to_drop = [ctd + n_candidates for ctd in cols_to_drop]
    df.drop(axis=1, columns=cols_to_drop, inplace=True)
    col_names = ["district", "village", "office"] + candidates + ["invalid_votes", "issued_votes", "remaining_votes"]
    df.columns = col_names
    # district imputation
    districts = df["district"].map(lambda x: x.strip())
    for i in range(len(districts)):
        if districts[i] == '':
            districts[i] = districts[i - 1]
    df["district"] = districts
    df.dropna(inplace=True)
    df["office"] = df["office"].astype(int)
    df.reset_index(drop=True, inplace=True)
    print("資料框的列數為：{}，投票所個數為：{}".format(
        df.shape[0], df["office"].values[-1] - df["office"].values[0] + 1))
    if '　　　 　　　' in list(df.columns):
        df.drop(columns='　　　 　　　', inplace=True)
    wide_df = df.copy()
    long_df_tobe = df.copy()
    long_df_tobe.drop(
        axis=1, columns=["invalid_votes", "issued_votes", "remaining_votes"], inplace=True)
    long_df_tobe = long_df_tobe.assign(id=list(long_df_tobe.index))
    long_df = pd.melt(long_df_tobe, id_vars=[
                      'id', 'district', 'village', "office"], value_vars=candidates)
    long_df.drop(axis=1, columns=["id"], inplace=True)
    long_df.columns = ["district", "village", "office", "number_party_candidate", "votes"]
    new = long_df["number_party_candidate"].str.split(expand=True)
    long_df["number"] = new[0].astype('int64')
    long_df["party"] = new[1]
    long_df["candidate"] = new[2]
    long_df.drop(axis=1, columns=["number_party_candidate"], inplace=True)
    long_df = long_df.loc[:, ["district", "village", "office", "number", "party", "candidate", "votes"]]
    return wide_df, long_df

def get_tidy_df_referendum(xls_file, designated_sheet=0):
    """
    Getting tidy dataframe from CEC
    """
    df = pd.read_excel(xls_file, skiprows=2, header=0,
                       sheet_name=designated_sheet)
    n_cols = df.shape[1]
    n_candidates = n_cols - 11
    candidates = list(df.columns[3:(3+n_candidates)])
    candidates = [cand.split("\n")[1] for cand in candidates]
    df = pd.read_excel(xls_file, skiprows=5, header=None,
                       sheet_name=designated_sheet)
    cols_to_drop = [3, 5, 6, 9, 10]
    cols_to_drop = [ctd + n_candidates for ctd in cols_to_drop]
    df.drop(axis=1, columns=cols_to_drop, inplace=True)
    col_names = ["district", "village", "office", "agree",
                 "disagree", "invalid_votes", "issued_votes", "remaining_votes"]
    df.columns = col_names
    # district imputation
    districts = df["district"].map(lambda x: x.strip())
    for i in range(len(districts)):
        if districts[i] == '':
            districts[i] = districts[i - 1]
    df["district"] = districts
    df.dropna(inplace=True)
    df["office"] = df["office"].astype(int)
    df.reset_index(drop=True, inplace=True)
    print("資料框的列數為：{}，投票所個數為：{}".format(
        df.shape[0], df["office"].values[-1] - df["office"].values[0] + 1))
    return df