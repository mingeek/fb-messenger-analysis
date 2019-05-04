import matplotlib.pyplot as plt

def plot_one(x, y, title, ylabel):
    f, ax = plt.subplots()
    ax.plot(x, y, 'b')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='both')
    plt.show()

#Input: Graphs, which is a list of objects
def plot_multi(graphs, title='Relationship Comparison', ylabel='Sentiment'):
    f, ax = plt.subplots()
    for i in range(len(graphs)): 
        ax.plot(graphs[i]['x'], graphs[i]['y'], 'C'+ str(i), label=graphs[i]['label'])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='both')
    plt.figlegend(loc=2)
    plt.show()

#Input: Graphset, which is a list of lists (size 2), with each inner list holding a JSON used to plot the figure
def plot_multi_two(graphset, title='Relationship Comparison', ylabel='sentiment'):
    f, ax = plt.subplots()
    if(len(graphset) == 2):
        axes = [
            ax,
            ax.twinx() #this lets you print the other axis on the opposite side
        ]
    else:
        return
    color_counter = 0
    for n in range(len(graphset)):
        axes[n].set_ylabel(graphset[n][0]['ylabel'])
        #graphs will have its own info on ylabel
        for i in range(len(graphset[n])): 
            axes[n].plot(graphset[n][i]['x'], graphset[n][i]['y'], 'C'+ str(color_counter), label=graphset[n][i]['label'])
            color_counter += 1
    handles, labels = ax.get_legend_handles_labels()
    f.legend(handles, labels, loc=2)
    ax.set_title(title)
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='both')
    plt.figlegend(loc=2)
    plt.show()
    