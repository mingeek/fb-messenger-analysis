import matplotlib.pyplot as plt

def plot_one(x, y, title, ylabel):
    f, ax = plt.subplots()
    ax.plot(x, y, 'b')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='both')
    plt.show()
    
def plot_two(onex, oney, twox, twoy):
    f, ax = plt.subplots()
    ax.plot(onex, oney, 'r')
    ax.plot(twox, twoy, 'b')
    ax.set_title('Relationship Comparison')
    ax.set_ylabel('Sentiment')
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='both')
    plt.show()