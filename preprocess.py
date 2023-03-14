import pandas as pd
import numpy as np
import datetime


pd.options.display.float_format = '{:.4f}'.format
np.set_printoptions(precision=3, suppress=True)

def make_category(g: pd.Series):
    label = ""
    for c in g.item_category.values:
        
        if label not in item_dict.keys():    
            label = c
            continue
            
        if item_dict[label] > item_dict[c]:
            label = c
            
    return label


if __name__ == '__main__':

    ############# 데이터 경로 설정 ############
    data_path = './Data/'
    items_path = data_path + 'items.csv'
    user_info = data_path + 'user_info.csv'
    item_code = data_path + 'item_code.csv'
    #######################################


    # 데이터 읽기
    raw_items = pd.read_csv(items_path)
    raw_user_info = pd.read_csv(user_info)
    raw_item_code = pd.read_csv(item_code)

    # User 정보 전처리
    user_info = raw_user_info[['아이디', '나이',  '회원등급']]
    user_info.columns = ['user_id', 'age', 'user_class']

    # 컬럼명 변경
    raw_items.columns = ['item_id', 'user_id', 'timestamp', 'cancel_type']
    raw_item_code.columns = ['item_category', 'item_id', 'price', 'priority']
    

    # tab 및 공백 제거
    raw_item_code['item_id'] = [str(c).replace('\t', '') for c in raw_item_code['item_id']]
    raw_item_code['item_id'] = [str(c).replace(' ', '') for c in raw_item_code['item_id']]
    raw_item_code['item_category'] = [str(c).replace('\t', '') for c in raw_item_code['item_category']]    
    raw_item_code['item_category'] = [str(c).replace(' ', '') for c in raw_item_code['item_category']] # 공백 제거
    

    # 멀티 라벨 처리 (우선순위는 데이터로 임의 설정)
    item_dict = {}
    for i in range(len(raw_item_code)):
        row = raw_item_code.loc[i]
        
        if row['item_category'] in item_dict.keys():
            continue
        item_dict[row['item_category']] = row['priority']

    item_code = raw_item_code.groupby(['item_id','price'])
    item_code = item_code.apply(lambda g: make_category(g)).reset_index()
    item_code.columns = ['item_id', 'price' , 'item_category']



    # 데이터 합치기
    items = pd.merge(raw_items, item_code, on='item_id', how='left')
    items['timestamp'] = pd.to_datetime(items['timestamp'], format='%Y.%m.%d %H:%M')

  

    
    # item 및 user 전처리
    item_output = item_code[['item_id', 'price', 'item_category']]
    user_output = user_info


    # inter 전처리
    print("inter before:", items.shape)
    
    inter_output = items.loc[items['cancel_type'].isna()]
    inter_output = inter_output[['user_id', 'item_id', 'timestamp']]
    inter_output = inter_output.dropna(axis=0)
    inter_output = inter_output.loc[inter_output['timestamp'] < "2022-10-01 00:00:00"]
    inter_output['timestamp'] = inter_output['timestamp'].astype(np.int64) // 10 ** 9
    inter_output = inter_output.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=True)
    
    print("inter after:", inter_output.shape)

    # 결측치 확인
    for col in inter_output.columns:
        msg = 'column: {:>10}\t Percent of NaN Value: {:.2f}%'.format(col, 100 * (inter_output[col].isnull().sum() / inter_output[col].shape[0]))
        print(msg)   

    # 컬럼명 설정
    inter_output.columns = ['user_id:token', 'item_id:token', 'timestamp:float']
    item_output.columns = ['item_id:token', 'price:token','class:token']
    user_output.columns = ['user_id:token', 'age:token', 'type:token']


    # 결과 저장
    inter_output.to_csv(data_path + 'rovigos/rovigos_t.inter', sep='\t', header=True, index=False)
    item_output.to_csv(data_path + 'rovigos/rovigos_t.item', sep='\t', header=True, index=False)
    user_output.to_csv(data_path + 'rovigos/rovigos_t.user', sep='\t', header=True, index=False, float_format='%.0f')