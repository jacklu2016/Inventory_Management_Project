import pandas as pd

from matplotlib import rcParams

penalty = True
# 设置中文字体
rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# Create a TimeSeries, specifying the time and value columns

import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 2, figsize=(12, 8), sharex=False, sharey=False)

if not penalty:
    algos = [{"name":'n=3,ps=50,mp=0.1,cp=0.6'},{"name":'n=5,ps=50,mp=0.1,cp=0.6'},{"name":'n=8,ps=80,mp=0.05,cp=0.6'},{"name":'n=10,ps=50,mp=0.1,cp=0.6'}]
else:
    algos = [{"name":'n=3,ps=80,mp=0.1,cp=0.6'},{"name":'n=5,ps=80,mp=0.05,cp=0.6'},{"name":'n=8,ps=50,mp=0.05,cp=0.6'},{"name":'n=10,ps=80,mp=0.1,cp=0.6'}]
fig_no = ['a','b','c','d']
#加载预测值
for i in range(4):
    #ax.plot(dates, values)
    ax_row = i // 2
    ax_col = i % 2
    #real_data.index = real_data.index - pd.Timedelta(days=1329)
    if penalty:
        df = pd.read_csv(algos[i]['name'] + f'_penalty_{penalty}.csv')
    else:
        df = pd.read_csv(algos[i]['name'] + '.csv')

    if penalty:
        ax[ax_row, ax_col].plot(df.iloc[:, 0] * 6.203980766, color='#005BAA')
    else:
        ax[ax_row, ax_col].plot(df.iloc[:, 0] * 5.533864377, color='#005BAA')

    ax[ax_row, ax_col].legend()
    #ax[ax_row, ax_col].grid(False)
    ax[ax_row, ax_col].set_xlabel('迭代次数')
    ax[ax_row, ax_col].set_ylabel('适应度(Fitness)')

    ax[ax_row, ax_col].set_title(f"({fig_no[i]})：{algos[i]['name'].replace('ps','N')}",
                 y=-0.20,  # 负值下移标题
                                 #pad = 10,
                 verticalalignment='top')  # 文本顶部对齐坐标轴



plt.legend()
plt.xlabel("", fontsize=12)
#plt.xticks(series[-60:], [f'第 {i+1}周' for i in series[-60:]])
# 设置为每周一刻度，显示ISO周编号
plt.tight_layout()
#plt.show()
plt.savefig(f'plot_best_result_iteration_penalty_{penalty}.svg',format='svg',bbox_inches='tight')

