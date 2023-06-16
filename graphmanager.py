import matplotlib.pyplot as plt


def generate_price_change_graph(timestamps, prices, chat_id):
    # Generate price change graph
    plt.plot(timestamps, prices)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('24-Hour Price Change')
    plt.grid(True)

    # Save the graph to a file
    graph_filename = f'{chat_id}.jpg'
    plt.savefig(graph_filename)
    plt.close()

    return graph_filename
