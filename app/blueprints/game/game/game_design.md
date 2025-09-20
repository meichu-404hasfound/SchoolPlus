# 遊戲設計文件

## 遊戲流程
1. **主畫面 (Main Menu)**:
   - 顯示遊戲標題。
   - 提供「開始遊戲」、「關卡選擇」、「離開遊戲」等選項。

2. **關卡選擇畫面 (Level Selection)**:
   - 顯示可選擇的關卡列表。
   - 玩家選擇一個關卡進入遊戲。

3. **遊玩畫面 (Gameplay Screen)**:
   - 顯示當前問題及四個選項。
   - 玩家選擇一個選項作答。
   - 答對：分數增加，顯示正確提示。
   - 答錯：分數減少，顯示錯誤提示。
   - 顯示當前分數和剩餘題目數。
   - 關卡結束時，進入結算畫面。

4. **結算畫面 (Result Screen)**:
   - 顯示關卡總分、答對題數、答錯題數。
   - 根據分數判斷是否通關。
   - 根據分數發放「貢丸」獎勵幣。
   - 提供「返回主畫面」、「重玩本關」等選項。

## 題目資料結構
每個題目將以字典形式儲存，包含以下欄位：
- `question`: 題目的文字內容 (string)
- `options`: 包含四個選項的列表 (list of strings)
- `answer`: 正確答案的索引 (integer, 0-3)
- `score_correct`: 答對時增加的分數 (integer)
- `score_wrong`: 答錯時扣除的分數 (integer)

## 範例題目資料
```python
questions = [
    {
        "question": "Python 的創始人是誰？",
        "options": ["Guido van Rossum", "James Gosling", "Brendan Eich", "Bjarne Stroustrup"],
        "answer": 0,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "以下哪個不是Python的資料型別？",
        "options": ["List", "Tuple", "Dictionary", "Array"],
        "answer": 3,
        "score_correct": 10,
        "score_wrong": -5
    },
    {
        "question": "在Python中，如何表示註解？",
        "options": ["//", "/* */", "#", "<!-- -->"],
        "answer": 2,
        "score_correct": 10,
        "score_wrong": -5
    }
]
```

