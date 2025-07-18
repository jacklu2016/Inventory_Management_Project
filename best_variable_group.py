import pandas as pd
import ast
import numpy as np

# 假设 CSV 文件中每一行都是一个字符串形式的数组列表，没有列名
df = pd.read_csv('best_variables.csv', header=None)
result_df = pd.read_csv('all_results.csv', header=None)
# 默认列编号为 0，所以我们访问 df[0]
#df[0] = df[0].apply(ast.literal_eval)  # 字符串转为列表

#df[0] = df[0].apply(lambda x: eval(x, {'array': np.array}))  # 列表中每个元素转为 numpy.array

#print(result_df)

table_df = pd.DataFrame({
    '0': [],
    '1': [],
    '2': [],
    '3': []
})

for col in df:
    #print(col)
    col_data = df[col]
    #print(col_data)
    col_data = col_data.apply(lambda x: eval(x, {'array': np.array}))  # 列表中每个元素转为 numpy.array
    for i in range(len(col_data)):
        data = col_data[i]
        result = [list(x) for x in zip(*data)]
        formatted = ";".join(
            "[" + ",".join(f"{x:.0f}" for x in row) + "]" for row in result
        ) + f";{result_df[col][i]:.0f}"
        # print(result)
        # print(result_df[col][i])
        table_df.loc[col, str(i)] = formatted
        print(formatted)
    #print('===========================')
    #print(np.array2string(result, precision=0, separator=", ", suppress_small=True))
table_df.to_csv('best_variables_group.csv')