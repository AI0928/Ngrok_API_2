import numpy as np
from collections import defaultdict
from http_reqests import *
import argparse


# ユーザー間の類似度を計算する関数を定義します（ここではジャカード類似度を使用します）。
def jaccard_similarity(user_items, user1, user2):
    # ユーザー1とユーザー2のアイテム集合を取得します。
    set1 = set(user_items[user1])
    set2 = set(user_items[user2])
    #-->set1: {'カレーライス', 'ラーメン', 'うどん'}
    #-->set2: {'ラーメン', 'うどん', '鯖の味噌煮'}

    # 2つの集合の積集合を取得します。
    intersection = len(set1.intersection(set2))
    #--> 2 = len(['カレーライス', 'ラーメン', 'うどん'] & ['ラーメン', 'うどん', '鯖の味噌煮'])

    # 2つの集合の和集合を取得します。
    union = len(set1) + len(set2) - intersection
    #--> 4 = len(['カレーライス', 'ラーメン', 'うどん'] + ['ラーメン', 'うどん', '鯖の味噌煮']) - 2

    # Jaccard類似度を計算して返します。
    return intersection / union
    #--> 0.5 = 2 / 4

def recommend_food(target_user):
    #APIからユーザーたちの購入履歴を取得する
    # ユーザーと商品のデータを仮定します。ユーザーごとの購買履歴を辞書で表現します。
    get_items = http_get('http://localhost:4040/employeefood')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--target_user', '-t', type=str)
    # args = parser.parse_args()

    user_items = {}
    for d in get_items:
        user = f"{d['employee_id']}"
        if user not in user_items:
            user_items[user] = []
        user_items[user].append(d['food_name'])

    #print(user_items)


    # 商品ごとのユーザーの購買情報を持つ辞書を作成します。
    item_users = defaultdict(list)
    #print(item_users)
    #print(user_items.items())
    for user, items in user_items.items():
        #print(user, items)
        for item in items:
            item_users[item].append(user)
    #print(item_users)-->{'apple': ['User1', 'User2'], 'banana': ['User1', 'User3']})



    # ユーザーごとに他のユーザーとの類似度を計算します。
    user_similarity = {} #ユーザーをキーにする
    for user1 in user_items.keys(): #user_items.keys() == ['User1', 'User2', 'User3']
        user_similarity[user1] = {}
        #-->{'User1':{}}

        for user2 in user_items.keys():
            #ユーザーが一緒なら処理を行わない
            if user1 == user2:
                continue
            #やりたいこと
            user_similarity[user1][user2] = jaccard_similarity(user_items, user1, user2)
            #-->{'User1':{'User2': -ここに代入-}} = 0.5 //jaccard_similarity('User1', 'User2')
    # 推薦対象のユーザーを指定します。
    #target_user = args.target_user

    # ユーザーに推薦する商品を格納する辞書を作成します。
    recommended_items = defaultdict(float)

    # ユーザーがまだ購入していない商品を抽出し、類似ユーザーの購買履歴から推薦します。
    #item_users-->{'apple': ['User1', 'User2'], 'banana': ['User1', 'User3']})
    for item, users in item_users.items():
        #print(item, users)#-->apple ['User1', 'User2']
        #usersにtarget_userが存在していなければ処理を行う
        #ターゲットユーザーが買っていない商品のとき、処理が行われる
        if target_user not in users:
            #print( user_similarity[target_user])-->{'User1': 0.5, 'User3': 0.0}
            for user, similarity in user_similarity[target_user].items():
                # print(user, similarity)-->User1 0.5
                #                        -->User3 0.0

                #ユーザーが買ったアイテムの中にitemがあるなら処理を行う
                if item in user_items[user]:
                    recommended_items[item] += similarity
                    #{'apple': -ここに代入-} += 0.5 //User1
                    #{'apple': 0.5-ここに足す-} += 0.0 //User3

    # 推薦商品を類似度の降順でソートします。
    recommended_items = dict(sorted(recommended_items.items(), key=lambda x: x[1], reverse=True))

    #推薦された商品を表示します。
    # print(f"{target_user}に推薦された商品:")
    # for item, score in recommended_items.items():
    #     print(f"{item}: スコア {score}")

    # print(user_similarity)

    return {"target_user": target_user, "recommended_items":  recommended_items, "user_similarity": user_similarity}

def recommend_matche(employee_id):
    matchetags = http_get('http://localhost:4040/matchtag')
    employeetags = http_get('http://localhost:4040/employeetag/' + employee_id)
    # Create a dictionary to store the points for each match
    matches = {}

    # Loop through each match in match_tags
    for match in matchetags:
        
        # If the match ID is not already in matches, add it with an empty dictionary
        if match["matche_id"] not in matches:
            
            matches[match["matche_id"]] = {}
        # Add the points for the tag to the dictionary for the match
        matches[match["matche_id"]][match["tags_name"]] = match["Point"]
    
    # Create a dictionary to store the points for each match
    employees = {}

    # Loop through each match in match_tags
    for employee in employeetags:

        # If the match ID is not already in matches, add it with an empty dictionary
        if employee["employee_id"] not in employees:
            
            employees[employee["employee_id"]] = {}
        
        # Add the points for the tag to the dictionary for the match
        employees[employee["employee_id"]][employee["tags_name"]] = employee["Point"]

    result = {}
    
    #print(matches, employees)
    for key, value in matches.items():
        #print(employees[employee["employee_id"]])
        result[key] = []
        value_array = {}
        for key2, value2 in value.items():
            value_array[key2]=value2
            if key2 not in employees[employee["employee_id"]]:
                employees[employee["employee_id"]][key2] = 0
        result[key].append(value_array)
        value_array = {}
        for key3, value3 in employees[employee["employee_id"]].items():
            if key3 in value.keys():
                value_array[key3] = value3
        result[key].append(value_array)

    result2 = {}
    for key4, value4 in result.items():
        value_array_matche = []
        value_array_employee = []
        for key5 in value4[0].keys():
            value_array_matche.append(value4[0][key5])
            value_array_employee.append(value4[1][key5])
        #print(value_array_employee, value_array_matche, cos_sim(value_array_employee, value_array_matche))
        result2[key4] = cos_sim(value_array_employee, value_array_matche)
    return result2

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))