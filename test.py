
experiment_params = [{'population_size': 80, 'mutation_probability':0.1, 'crossover_probability': 0.5},
                         {'population_size': 100, 'mutation_probability':0.1, 'crossover_probability': 0.5},
                         {'population_size': 80, 'mutation_probability':0.05, 'crossover_probability': 0.5},
                         {'population_size': 100, 'mutation_probability':0.05, 'crossover_probability': 0.5},
                         {'population_size': 80, 'mutation_probability': 0.1, 'crossover_probability': 0.6},
                         {'population_size': 100, 'mutation_probability': 0.1, 'crossover_probability': 0.6},
                         {'population_size': 80, 'mutation_probability': 0.05, 'crossover_probability': 0.6},
                         {'population_size': 100, 'mutation_probability':0.05, 'crossover_probability': 0.6}]






import pandas as pd
all_results = [[114.60375502644463, 108.77904198121942, 116.89820984493039, 112.2340086586488, 114.20866716033653, 110.53905060639785, 114.59488782266118, 110.10609785258151], [193.87922806536045, 184.06056126965032, 197.69075393335362, 185.98859602909596, 187.52776029495027, 183.8133554545646, 218.16959957159656, 184.97769751311156], [305.85712396499866, 288.78218667798853, 304.1115375663411, 299.69738802287975, 306.54978390924924, 296.6219137293193, 306.9448085210281, 327.6554720085245], [369.61669999931877, 366.44072364036117, 411.04146107603435, 368.3693440747572, 371.6597462454027, 365.1009920715759, 381.61128334375604, 391.88372056800375]]
df = pd.DataFrame(all_results)
df.to_csv("output.csv", index=False, header=False)  # 不保存行号和列名