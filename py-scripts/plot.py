def save_plot(
    plt,
    title,
    xlabel,
    ylabel,
    filename,
):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename, bbox_inches="tight", pad_inches=0.1)
