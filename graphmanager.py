import matplotlib.pyplot as plt
import thememanager


def generate_price_change_graph(timestamps, prices, had_price_grown: bool, chat_id: int, language: list[str]):
    theme = thememanager.get_theme(chat_id)

    # Set graph color to green or red depending on price change
    if had_price_grown:
        graph_color = theme["green"]
    else:
        graph_color = theme["red"]

    text_color = theme["text"]
    background_color = theme["base"]

    # Generate price change graph
    fig = plt.figure()
    fig.patch.set_facecolor(background_color)
    plt.plot(timestamps, prices, color=graph_color)

    # Style it
    plt.xlabel(language[15][0])
    plt.xticks([])
    plt.ylabel(language[15][1])
    plt.title(language[15][2], color=text_color)

    ax = plt.gca()
    ax.set_facecolor(background_color)

    ax.xaxis.label.set_color(text_color)
    ax.tick_params(axis="x", colors=text_color)
    ax.yaxis.label.set_color(text_color)
    ax.tick_params(axis="y", colors=text_color)

    plt.grid(True, color=text_color)

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Save the graph to a file
    graph_filename = f"{chat_id}.jpg"
    plt.savefig(graph_filename)
    plt.close()
    return graph_filename
