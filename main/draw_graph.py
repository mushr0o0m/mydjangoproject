import os
import matplotlib.pyplot as plt


def draw_hor_bar_graph(graph_data: (int, str, int), graph_title: str) -> str:
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white', dpi=80)
    index, x_data, y_data = [], [], []
    for item in graph_data:
        index.append(item[0])
        x_data.append(item[1])
        y_data.append(item[2])
    ax.vlines(x=index, ymin=0, ymax=y_data,
              color='firebrick', alpha=0.7, linewidth=20)
    s, e = plt.gca().get_xlim()
    plt.xlim(s, e)
    ax.grid(axis='y', color='black', alpha=0.8, linewidth=0.5)
    ax.set_title(graph_title, fontdict={'size': 22}, pad=10)
    plt.xticks(index, x_data, rotation=60, horizontalalignment='right', fontsize=12)
    plt.tight_layout()
    fig.savefig(os.path.join('media', 'img', 'statistics_graphs', graph_title))
    return os.path.join('img', 'statistics_graphs', graph_title) + '.png'


def draw_vert_bar_graph(graph_data: (int, str, int), graph_title: str) -> str:
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white', dpi=80)
    indexes, x_data, y_data = [], [], []
    for item in graph_data:
        indexes.append(item[0])
        x_data.append(item[1])
        y_data.append(item[2])

    sep_graph_title = graph_title.split(' ')
    sep_graph_title = ' '.join(sep_graph_title[0:(round(len(sep_graph_title)/2))]) + \
                      '\n' + ' '.join(sep_graph_title[(round(len(sep_graph_title)/2)):])
    ax.set_title(sep_graph_title, loc="center", pad=10, fontsize=18)
    plt.barh([i + 1 for i in indexes], y_data, alpha=0.7, label='First', color='firebrick')
    plt.yticks([i + 1.4 for i in indexes], x_data, fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join('media', 'img', 'statistics_graphs', graph_title))
    return os.path.join('img', 'statistics_graphs', graph_title) + '.png'


def draw_pie_graph(graph_data: (str, int), graph_title: str, legend_title: str) -> str:
    labels, values = [], []
    for item in graph_data:
        labels.append(item[0])
        values.append(item[1])
    labels += ['Другие']
    values += [1 - sum(values)]
    fig1, ax1 = plt.subplots(figsize=(16, 10), dpi=80)
    explode = [0] * (len(values) - 1) + [0.2]
    plt.title(graph_title, loc="center", pad=10, fontsize=22)
    wedges, texts, titles = ax1.pie(values, labels=labels, labeldistance=None, shadow=False, autopct='%1.1f%%',
                                    startangle=360, explode=explode)
    ax1.axis('equal')
    ax1.legend(wedges, labels, title=legend_title, loc='upper left', fontsize=15, title_fontsize=16)
    plt.setp(titles, size=15, weight=500)
    plt.tight_layout()
    plt.savefig(os.path.join('media', 'img', 'statistics_graphs', graph_title))
    return os.path.join('img', 'statistics_graphs', graph_title) + '.png'
