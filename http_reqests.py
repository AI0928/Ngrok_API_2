import requests
import argparse

def http_get(url):
    get_url = url
    return requests.get(get_url).json()

def http_post(url, data):
    return requests.post(url, json=data).json()

def http_put(url, data):
    return requests.put(url, json=data)

def http_delete(url, id):
    delete_url = url + '/' + str(id)
    return requests.delete(delete_url)

def food2local(url, num):
    food_url = 'https://script.google.com/macros/s/AKfycbx7WZ-wdIBLqVnCxPwzedIdjhC3CMjhAcV0MufN2gJd-xsO3xw/exec?'
    weight = "150"
    food = http_get(food_url + 'num=' + num + '&weight=' + str(weight))
    food_json = {"id": int(num), 
                "name": food['食品名'],
                "energy": food["エネルギー（kcal）"],
                "protein": food["たんぱく質"],
                "lipid": food["脂質"],
                "cholesterol": food["コレステロール"],
                "carbohybrates": food["炭水化物"]}

    http_post(url, food_json)
    return http_get(url)

def post_EmployeeFood(url, employee_id, food_id):
    data = {"employee_id": int(employee_id),
            "food_id": int(food_id), 
            "date":'2023-08-31'}
    return http_post(url, data)

def send_http_request(method, url, employee_id=None, food_id=None, food_num=None):
    if method == 'GET':
        return http_get(url)
    elif method == 'POST':
        data = {
                    "employee_id": 2,
                    "name": "Mission 5",
                    "description": "Mission 5 description",
                    "start_date": "2023-12-01",
                    "end_date": "2023-12-31",
                    "status": "In progress"
                }
        return http_post(url, data)
    elif method == 'PUT':
        data = http_get(url)
        data['description'] = '更新テスト'
        return http_put(url, data)
    # elif method == 'DELETE':
    #     return http_delete(url)
    elif method == 'food2local':
        return food2local(url, food_num)
    elif method == 'post_EmployeeFood':
        return post_EmployeeFood(url, employee_id, food_id)
    else:
        raise ValueError('Invalid HTTP method')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', type=str)
    parser.add_argument('--requests', '-r', type=str)
    parser.add_argument('--employee_id', '-e', type=str)
    parser.add_argument('--food_id', '-f', type=str)
    parser.add_argument('--food_num', '-n', type=str)
    args = parser.parse_args()

    result = ""

    # Example usage
    ##############
    if args.food_num != None:
        response = send_http_request(args.requests, args.url, args.food_num)
    elif args.employee_id != None and args.food_id != None:
        response = send_http_request(args.requests, args.url, args.employee_id, args.food_id)
    else :
        response = send_http_request(args.requests, args.url)
    print(response)