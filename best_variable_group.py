import pandas as pd
import ast
import numpy as np

# 假设 CSV 文件中每一行都是一个字符串形式的数组列表，没有列名
df = pd.read_csv('best_variables.csv', header=None)
result_df = pd.read_csv('all_results.csv', header=None)
# 默认列编号为 0，所以我们访问 df[0]
#df[0] = df[0].apply(ast.literal_eval)  # 字符串转为列表

df[0] = df[0].apply(lambda x: eval(x, {'array': np.array}))  # 列表中每个元素转为 numpy.array

#print(result_df)
for col in df:
    #print(col)
    col_data = df[col]
    for i in range(len(df[0])):
        data = df[0][i]
        result = [list(x) for x in zip(*data)]
        formatted = "[" + ",\n ".join(
            "[" + ",".join(f"{x:.0f}" for x in row) + "]" for row in result
        ) + "]"

        print(formatted)
        print('fitvalue:')
        print(f"{result_df[col][i]:.0f}")
    print('===========================')
    #print(np.array2string(result, precision=0, separator=", ", suppress_small=True))
