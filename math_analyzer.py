from scipy.stats import pearsonr


def correlation_analysis(user_data):
    corr, _ = pearsonr([row['times_visited_courses']
                       for row in user_data], [row['grade'] for row in user_data])
    corr = abs(corr)
    return f"{format(corr*100, '.2f')}% Pearson correlation"
