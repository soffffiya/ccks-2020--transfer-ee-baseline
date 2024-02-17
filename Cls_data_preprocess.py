import json
import pandas as pd

def check_num_type():
    lst = []
    in_file = open('dataset/train.json','r')
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        #print(line)
        ids = line['id']
        content = line['content']
        for k in line['events']:
            evn_type = k['type']
            lst.append(evn_type)
    lst = set(lst)
    print(lst)
    
# def change_data():  #原来的只能读取到第一个元素
#     i=0
#     in_file = open('dataset/train.json','r')  
#     final_lst = []
#     # with open('dataset/test.json', 'r',encoding='utf-8') as in_file:
#     for line in in_file:
#         org_lst = ['质押','股份股权转让','起诉','投资','减持']
#         line = line.strip()
#         line = json.loads(line)
#         # print(line)
#         line = [eval(item) for item in line]  # 使用 eval() 函数将字符串转换为字典类型
#         ids = line[i]['doc_id']  #报错，TypeError: list indices must be integers or slices, not str
#         content = line[i]['content']
#         lst = []
#         for k in line[i]['events']:
#             # print(k.keys())  #dict_keys(['受理法院', 'event_type', 'event_id', '公司名称', '裁定时间', '公告时间'])
#             evn_type = k['event_type']
#             lst.append(evn_type)
#         # print(ids,content,lst)
#         i+=1 #我希望i每次循环都自增1，该怎么改代码
#         print('现在打印的是：%d'%(i))
#         label_lst = []
#         label_lst.append(ids)
#         label_lst.append(content)
#         for i in org_lst:
#             if i in lst:
#                 label_lst.append(1)
#             else:
#                 label_lst.append(0)
#         #print(label_lst)
#         final_lst.append(label_lst)
        
#     return final_lst
    
def change_data():  #更改后能遍历全部的样本
    final_lst = []
    org_lst = ['质押', '股份股权转让', '起诉', '投资', '减持']
    with open('dataset/train.json', 'r') as in_file:
        for line in in_file:
            line = line.strip()
            line = json.loads(line)
            line = [eval(item) for item in line]  # 使用 eval() 函数将字符串转换为字典类型
            for idx, item in enumerate(line):  # 使用 enumerate() 函数同时获取索引值和元素
                ids = item['doc_id']
                content = item['content']
                lst = [event['event_type'] for event in item['events']]
                label_lst = [ids, content] + [1 if event_type in lst else 0 for event_type in org_lst]
                final_lst.append(label_lst)
    return final_lst


def get_cls_train_data():
    final_lst = change_data()
    df = pd.DataFrame()
    df = df.append(final_lst,ignore_index=True)
    print(df)
    df.columns = ['id','content','zy','gfgqzr','qs','tz','ggjc']  #结果可视化——表格，但是报错 Length mismatch: Expected axis has 0 elements, new values have 7 elements
    df.to_csv('dataset/train_sample.csv',index=0)
    print('分类模型训练集已转换完成！')
    
def get_cls_test_data():  
    test_df = open('dataset/test.json')
    lst=[]
    for line in test_df:
        line = line.strip()
        line = json.loads(line)
        #print(line)
        lst.append(line)
    df = pd.DataFrame(lst)
    df.columns = ['id','content']   #KeyError: "None of [Index(['id', 'content'], dtype='object')] are in the [columns] 所以加了这两句
    # print(df.head())  # 打印 DataFrame 的前几行，以便查看数据结构
    df = df[['id','content']]
    df.to_csv('dataset/test.csv',index=0)
    print('分类模型测试集已转换完成！')
    
if __name__ == '__main__':
    get_cls_train_data()
    get_cls_test_data()