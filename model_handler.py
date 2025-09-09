import pandas as PD
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from data_processor import playerdata, make_pdlist, make_newdf, split_by_position
from data_processor import Adequacy
from data_processor import heap_sort, heapify, contain_league


MODELS_FILE = 'models.pkl'

def train_and_save_models():
    """トレーニングデータからモデルを学習し、ファイルに保存する"""
    print("モデルを学習して保存しています...")
    
    leagues = []
    pd_ls = playerdata()
    data_dir = "training_data"
    
    html_files = [f for f in os.listdir(data_dir) if f.endswith(".html")]
    if not html_files:
        print("エラー: 'training_data'フォルダにHTMLファイルが見つかりません。")
        return None, None

    for filename in html_files:
        filepath = os.path.join(data_dir, filename)
        make_pdlist(filepath, pd_ls, leagues)
            
    newdf = make_newdf(pd_ls)

    cols = ["平均", "時間"]
    for ab in pd_ls.ab_ls :
        cols.append(ab)
    
    newdf[cols] = newdf[cols].apply(PD.to_numeric, errors='coerce')
    newdf = newdf.dropna(subset=cols)
    newdf = newdf[(newdf['平均'] >= 0.1) & (newdf['ディビジョン'] != "-") & (newdf['時間'] >= 500)]

    EPAL = []
    for L in leagues:
        total = 0
        altdf = newdf[newdf['ディビジョン'] == L]
        numofp = len(altdf)
        if(numofp < 200):
            newdf = newdf[(newdf['ディビジョン'] != L)]
            continue
        for ab in pd_ls.ab_ls:
            total += altdf[ab].sum()
        if total == 0:
            continue
        EPAL.append([L,(altdf["平均"].sum() - numofp * 5.5) / total])
    
    if EPAL:
        heap_sort(EPAL)
        standard = EPAL[0][1]
        for ls in EPAL:
            condition = newdf['ディビジョン'] == ls[0]
            newdf.loc[condition, '平均'] = (newdf.loc[condition, '平均'] - 5.5) * standard / ls[1] + 5.5
    
    posi_dict = split_by_position(newdf, Adequacy.Natural)
    models = {}
    posi_dict_for_pred = {}
    for posi, df in posi_dict.items():
        if df.empty or '平均' not in df.columns:
            print(f"警告: ポジション {posi} には学習するのに十分なデータがありません。")
            continue
        
        df_copy = df.copy()

        df_corr = df_copy.corr()["平均"]
        lowest = 0.1
        columns_drop = df_corr[df_corr <= lowest].index
        
        df_copy.drop(columns=columns_drop, inplace=True)
        df_copy.fillna(df_copy.mean(), inplace=True)
        
        if df_copy.drop("平均", axis=1).empty:
            print(f"警告: ポジション {posi} の特徴量が不足しているため、モデルは作成されません。")
            continue

        x_train, _, y_train, _ = train_test_split(df_copy.drop("平均", axis=1), df_copy["平均"], test_size=0.2, random_state=0)
        
        model = LinearRegression()
        model.fit(x_train, y_train)
        models[posi] = model
        posi_dict_for_pred[posi] = df_copy
        
    if not models:
        print("エラー: 学習可能なモデルが一つも作成されませんでした。")
        return None, None
        
    with open(MODELS_FILE, 'wb') as f:
        # modelsとposi_dict_for_predを辞書にまとめて保存
        pickle.dump({'models': models, 'posi_dict_for_pred': posi_dict_for_pred}, f)
    
    print("モデルの学習と保存が完了しました。")
    return models, posi_dict_for_pred

def load_models():
    """保存されたモデルと特徴量辞書を読み込む"""
    if os.path.exists(MODELS_FILE):
        with open(MODELS_FILE, 'rb') as f:
            data = pickle.load(f)
            print("学習済みのモデルと特徴量情報を読み込んでいます。")
            return data['models'], data['posi_dict_for_pred']
    else:
        print("エラー: 学習済みのモデルファイルが見つかりません。")
        return None, None