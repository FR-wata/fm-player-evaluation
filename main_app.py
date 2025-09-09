import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as PD
import os

# 自作モジュールをインポート
from data_processor import playerdata, make_pdlist, make_Mypdlist, make_newdf, split_by_position, Adequacy, unit_conversion
from model_handler import train_and_save_models, load_models

class FMApp:
    def __init__(self, master):
        self.master = master
        master.title("FM選手評価ツール")

        self.models, self.posi_dict_for_pred = load_models()
        
        # UIの構築
        self.label = tk.Label(master, text="Football Manager 選手評価ツール", font=("Arial", 16))
        self.label.pack(pady=10)

        # モデル学習セクション
        learn_frame = tk.LabelFrame(master, text="モデル学習")
        learn_frame.pack(pady=10, padx=10, fill="x")
        
        self.learn_button = tk.Button(learn_frame, text="モデルを学習・保存", command=self.learn_models)
        self.learn_button.pack(pady=5)

        # 選手評価セクション
        eval_frame = tk.LabelFrame(master, text="選手評価")
        eval_frame.pack(pady=10, padx=10, fill="x")
        
        self.file_path = tk.StringVar()
        self.file_path_label = tk.Label(eval_frame, textvariable=self.file_path)
        self.file_path_label.pack()
        
        self.select_file_button = tk.Button(eval_frame, text="評価対象HTMLファイルを選択", command=self.select_file)
        self.select_file_button.pack(pady=5)

        # ポジション選択（ドロップダウンメニュー）
        self.position_label = tk.Label(eval_frame, text="評価ポジション:")
        self.position_label.pack(pady=2)
        
        self.positions = ["GK", "DR", "DC", "DL", "WBR", "WBL", "DM", "MR", "MC", "ML", "AMR", "AMC", "AML", "STC"]
        self.position_combobox = ttk.Combobox(eval_frame, values=self.positions)
        self.position_combobox.pack(pady=2)
        self.position_combobox.current(0)
        
        # 適性レベルの選択
        self.adequacy_label = tk.Label(eval_frame, text="ポジション適性:")
        self.adequacy_label.pack(pady=2)
        self.adequacy_levels = ["Natural", "Accomplished", "Others"]
        self.adequacy_combobox = ttk.Combobox(eval_frame, values=self.adequacy_levels)
        self.adequacy_combobox.pack(pady=2)
        self.adequacy_combobox.current(0) # デフォルトで'Natural'を選択

        # 予算上限と単位の選択
        budget_frame = tk.Frame(eval_frame)
        budget_frame.pack(pady=2)

        self.budget_label = tk.Label(budget_frame, text="予算上限:")
        self.budget_label.pack(side="left")

        self.budget_entry = tk.Entry(budget_frame, width=15)
        self.budget_entry.insert(0, "10")
        self.budget_entry.pack(side="left")

        self.unit_combobox = ttk.Combobox(budget_frame, values=["K", "M", "億", "B", "万"], width=5)
        self.unit_combobox.set("M")
        self.unit_combobox.pack(side="left")
        
        # 年齢による絞り込み
        age_frame = tk.Frame(eval_frame)
        age_frame.pack(pady=2)
        
        self.age_label = tk.Label(age_frame, text="年齢:")
        self.age_label.pack(side="left")
        
        self.age_min_entry = tk.Entry(age_frame, width=5)
        self.age_min_entry.insert(0, "16")
        self.age_min_entry.pack(side="left")
        
        self.age_hyphen_label = tk.Label(age_frame, text="-")
        self.age_hyphen_label.pack(side="left")
        
        self.age_max_entry = tk.Entry(age_frame, width=5)
        self.age_max_entry.insert(0, "30")
        self.age_max_entry.pack(side="left")


        # 人数指定
        self.num_label = tk.Label(eval_frame, text="表示人数:")
        self.num_entry = tk.Entry(eval_frame)
        self.num_entry.insert(0, "10")
        
        self.eval_button = tk.Button(eval_frame, text="評価実行", command=self.run_evaluation)
        
        self.num_label.pack(pady=2)
        self.num_entry.pack()
        self.eval_button.pack(pady=5)

        # 結果表示エリア
        self.result_label = tk.Label(master, text="結果:")
        self.result_label.pack()
        
        self.result_text = tk.Text(master, height=15, width=80)
        self.result_text.pack(padx=10, pady=5)

    def learn_models(self):
        """モデル学習ボタンが押されたときの処理"""
        self.models, self.posi_dict_for_pred = train_and_save_models()
        if self.models:
            messagebox.showinfo("完了", "モデルの学習と保存が完了しました。")
        else:
            messagebox.showerror("エラー", "モデル学習に失敗しました。トレーニングデータを確認してください。")

    def select_file(self):
        """ファイル選択ボタンが押されたときの処理"""
        filepath = filedialog.askopenfilename(
            title="HTMLファイルを選択",
            filetypes=[("HTML files", "*.html")]
        )
        if filepath:
            self.file_path.set(filepath)

    def run_evaluation(self):
        """評価実行ボタンが押されたときの処理"""
        if not self.models:
            messagebox.showerror("エラー", "モデルが学習されていません。最初にモデル学習を実行してください。")
            return
            
        filepath = self.file_path.get()
        if not filepath:
            messagebox.showerror("エラー", "評価対象のファイルを選択してください。")
            return
            
        position = self.position_combobox.get()
        adequacy_level = self.adequacy_combobox.get()
        num_to_show = self.num_entry.get()
        budget_value_str = self.budget_entry.get()
        budget_unit = self.unit_combobox.get()
        age_min_str = self.age_min_entry.get()
        age_max_str = self.age_max_entry.get()

        try:
            num_to_show = int(num_to_show)
            budget_value = float(budget_value_str)
            budget = unit_conversion(budget_unit, budget_value)
            age_min = int(age_min_str)
            age_max = int(age_max_str)
        except ValueError:
            messagebox.showerror("エラー", "表示人数、予算、年齢は数字で入力してください。")
            return
            
        if position not in self.models:
            messagebox.showerror("エラー", "選択されたポジションのモデルは存在しません。")
            return
            
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "評価を実行中...\n")

        try:
            # AdequacyのEnumを文字列から取得
            adequacy = Adequacy[adequacy_level]
            
            # データの読み込み
            data_obj = playerdata()
            if "myteam" in filepath.lower():
                make_Mypdlist(filepath, data_obj)
            else:
                make_pdlist(filepath, data_obj, [])
            
            df = make_newdf(data_obj)
            
            # 評価関数の呼び出しと結果の取得
            pre_posi_dict = split_by_position(df, adequacy)
            eval_df = pre_posi_dict[position]
            
            # モデルが学習した特徴量列を正しく取得
            model_features = [col for col in self.posi_dict_for_pred[position].columns if col != '平均']
            
            # 評価対象のDataFrameに必要な特徴量列のみを抽出
            x = eval_df.loc[:, model_features]
            
            # 欠損値の補完
            x = x.fillna(x.mean())
            
            # モデルによる予測
            model = self.models[position]
            pred = model.predict(x)
            
            # 予測結果を元のDataFrameに結合
            res_df = df.loc[eval_df.index].copy()
            res_df['予測評価'] = pred
            
            # 予算と年齢でフィルタリング
            res_df['移籍評価額'] = PD.to_numeric(res_df['移籍評価額'], errors='coerce')
            res_df['年齢'] = PD.to_numeric(res_df['年齢'], errors='coerce')
            
            res_df = res_df[(res_df['移籍評価額'] <= budget) & 
                            (res_df['年齢'] >= age_min) & 
                            (res_df['年齢'] <= age_max)]
            
            res_df = res_df.sort_values(by='予測評価', ascending=False)
            
            result_str = f"【{position}】の評価結果です。\n"
            result_str += f"予算上限: {budget_value_str} {budget_unit}\n"
            result_str += f"年齢範囲: {age_min_str} - {age_max_str}\n\n"
            
            # 上位N名を表示
            top_players = res_df[["名前", "予測評価", "移籍評価額", "年齢", "クラブ"]].head(num_to_show)
            result_str += top_players.to_string(index=False, justify='left')
            
            self.result_text.insert(tk.END, result_str)
            self.result_text.insert(tk.END, "\n\n評価が完了しました。")
        
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {e}")
            self.result_text.insert(tk.END, f"\nエラーが発生しました: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = FMApp(root)
    root.mainloop()