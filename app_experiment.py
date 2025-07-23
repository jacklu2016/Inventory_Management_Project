
import pickle
import numpy as np
import random
import matplotlib
matplotlib.use('TkAgg')  # 或 'QtAgg', 'Qt5Agg'

import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体（Windows 示例，SimHei = 黑体）
matplotlib.rcParams['font.family'] = 'SimHei'

# 避免负号显示为乱码
matplotlib.rcParams['axes.unicode_minus'] = False

arr=[2927.9375457565484,3055.8750915130963,3183.8126372696447,3311.750183026193]

def experiment_ga():

    #print(int_features[2])
    penalty = True
    days = 1
    demand_mean = arr[days-1]/30
    # print(df[1][0])
    # demand_mean=101.8625
    demand_sd = 10
    lead_time_max = 1
    lead_time_min = 1

    #service level 服务满足率
    asl = 95

    kk = 0

    if not 0<asl<100: #data validation on ASL
        while kk == 0:
            print("required service level has to be between 0 to 100")
            asl = float(input("What is the required service level (e.g. 95.0) : "))
            if not 0<asl<100:
                kk=0
            else:
                kk=1


    days = days + 2*lead_time_max      # adding extra days to stabilise the simulation
    days2 = days*2                     
    print(days2)
    def stoch_inv_sim(X): #Stochastic model defined as a function called stoch_inv_sim([Order qty, Reorder point])
        
        obj =0      #objective function for Genetic algorithm
        
        for k in range(10):  #Every strategy will be tested for 10 times since we are generating demand using random function,to be more exhaustive, you can increase the number to a higher value.
            tot_demand =0
            tot_sales=0
            
            a = [max(0,np.random.normal(demand_mean,demand_sd,1)) for i in range(days)] #Generating a random Demand
            stkout_count = 0
            inv =[]                 # array to store daily inventory
            pip_inv=[]

            in_qty = [0 for i in range(days2)]     #array indicating receipt of goods
            order_qty = X[0]
            reorder_pt = X[1]

            for i in range(days):

                if i == 0:
                    beg_inv = reorder_pt            #day 0 assigning reorder point as begining inventory
                    in_inv = 0
                    stock_open = beg_inv + in_inv
                else:
                    beg_inv = end_inv
                    in_inv = in_qty[i]              #incoming inventory on i'th day
                    stock_open = beg_inv + in_inv

                demand = a[i]                     #calling demand of i'th day from demand array a
                
                lead_time = random.randint(lead_time_min,lead_time_max)    #lead time of replenishment
                
                if demand < stock_open:
                    end_inv = stock_open - demand     #formula to calculate ending inventory
                else:
                    end_inv = 0
                inv.append(0.5*stock_open+0.5*end_inv)     #storing the average of opening stock and ending inventory as cycle inventory

                if i==0:
                    pipeline_inv = 0
                else:
                    pipeline_inv = sum(in_qty[j] for j in (i+1,days2-1))   #calculating the piepline inventory as on i'th day

                if pipeline_inv + end_inv <= reorder_pt:
                    if i+lead_time <days:
                        in_qty[i+lead_time] = in_qty[i+lead_time]+order_qty   #ordering new stock and adding to the incoming inventory list
                        #obj += order_qty #计算成本，1个订单单位成本1
                if i>=2*lead_time_max:                            #the start of simulation performance monitoring
                    tot_sales = tot_sales + stock_open - end_inv  #total sales during the simulation length
                    tot_demand = tot_demand + demand              #total demand during the simulation length
                    

            cycle_inv = 0
            for n in range(len(inv)):
                cycle_inv = cycle_inv + inv[n]              #calculating the averge cycle inventory
            #cycle_inv = cycle_inv/len(inv)
            #obj += cycle_inv * 0.3 #库存单位成本时0.3

            
            if tot_sales*100/(tot_demand+0.000001) <asl:
                if penalty:
                    aa = cycle_inv+ 3 * (tot_demand-tot_sales)#Imposing a penatly when ASL is not met the requirement
                else:
                    aa = cycle_inv + (tot_demand-tot_sales)
            else:
                aa = cycle_inv
                
            obj = obj + aa      #objective function i.e. cycle inventory calculation

        return obj/10


    print()
    print("Model created, Proceeding to Optimisation with GA.")
    print()
    print("Optimal [Order Quantity, Reorder point] & Estimated Cycle Inventory level will be printed below...")
    print()

    #Below is the gentic Algorithm code

    from geneticalgorithm import geneticalgorithm as ga

    varbound=np.array([[0,demand_mean*lead_time_max*5]]*2)

    algorithm_param = {'max_num_iteration': 1000,
                    'population_size':15,
                    'mutation_probability':0.1,
                    'elit_ratio': 0.05,
                    'crossover_probability': 0.5,
                    'parents_portion': 0.3,
                    'crossover_type':'uniform',
                    'max_iteration_without_improv':200}

    experiment_stores = [3,5,8,10]
    experiment_stores_best_result_param_indexs = []
    experiment_params = [{'population_size': 50, 'mutation_probability':0.1, 'crossover_probability': 0.5},
                         {'population_size': 80, 'mutation_probability':0.1, 'crossover_probability': 0.5},
                         {'population_size': 50, 'mutation_probability':0.05, 'crossover_probability': 0.5},
                         {'population_size': 80, 'mutation_probability':0.05, 'crossover_probability': 0.5},
                         {'population_size': 50, 'mutation_probability': 0.1, 'crossover_probability': 0.6},
                         {'population_size': 80, 'mutation_probability': 0.1, 'crossover_probability': 0.6},
                         {'population_size': 50, 'mutation_probability': 0.05, 'crossover_probability': 0.6},
                         {'population_size': 80, 'mutation_probability':0.05, 'crossover_probability': 0.6}]

    all_results = []
    all_reports = []
    all_variables = []
    for i in range(len(experiment_stores)):
        n = experiment_stores[i]
        store_results = []
        store_reports = []
        store_variables = []
        best_result = 100000000
        best_result_index = 0
        for j in range(len(experiment_params)):
            model_results = []
            model_report = []
            model_variable = []
            for k in range(n):
                algorithm_param['population_size'] = experiment_params[j]['population_size']
                #algorithm_param['population_size'] = 10
                algorithm_param['mutation_probability'] = experiment_params[j]['mutation_probability']
                algorithm_param['crossover_probability'] = experiment_params[j]['crossover_probability']
                print(algorithm_param)
                model = ga(function=stoch_inv_sim,dimension=2,variable_type='real',variable_boundaries=varbound,algorithm_parameters=algorithm_param, convergence_curve=False)
                model.run()

                temp=min(model.report)
                model_results.append(temp)
                model_variable.append(model.best_variable)
                print(temp)
                #print(np.array(model.report))
                model_report.append(np.array(model.report))

            model_report_sum = [sum(x) for x in zip(*model_report)]
            model_result_sum = np.sum(model_results,axis=0)
            store_results.append(model_result_sum)
            store_reports.append(model_report_sum)
            store_variables.append(model_variable)
            if best_result > model_result_sum:
                best_result = model_result_sum
                best_result_index = j
        # print(model_report_sum)
        # plt.plot(model_report_sum)
        # plt.xlabel('Iteration')
        # plt.ylabel('Objective function Sum')
        # plt.title('Genetic Algorithm')
        # plt.show()show
        experiment_stores_best_result_param_indexs.append(best_result_index)
        all_results.append(store_results)
        all_reports.append(store_reports)
        all_variables.append(store_variables)

    print("All Results:")
    print(all_results)
    import pandas as pd
    df = pd.DataFrame(all_results)
    df.to_csv(f"all_results_penalty_{penalty}.csv", index=False, header=False)  # 不保存行号和列名

    df1 = pd.DataFrame(all_variables)
    df1.to_csv(f"best_variables_penalty_{penalty}.csv", index=False, header=False)  # 不保存行号和列名
    print("All Reports:")
    print(all_reports)

    #保存图片
    for i in range(len(experiment_stores)):
        best_report = all_reports[i][experiment_stores_best_result_param_indexs[i]]
        print(best_report)
        plt.clf()  # 清除当前 figure 的所有内容
        plt.plot(best_report)
        plt.xlabel('迭代次数')
        plt.ylabel('目标值')
        experiment_param = experiment_params[experiment_stores_best_result_param_indexs[i]]

        params = f'n={experiment_stores[i]},ps={experiment_param["population_size"]},mp={experiment_param["mutation_probability"]},cp={experiment_param["crossover_probability"]}'
        plt.title(params)
        plt.savefig(params + '.svg', format='svg', bbox_inches='tight', transparent=True)

        best_report_arr = np.array(best_report)
        np.savetxt(f"{params}_penalty_{penalty}.csv", best_report_arr.reshape(-1, 1), delimiter=",")  # 保存

if __name__ == '__main__':
    experiment_ga()