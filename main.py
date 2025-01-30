import multiprocessing

from ttkthemes.themed_tk import ThemedTk

from UI.gui import GUI



def main():
    multiprocessing.freeze_support()
    root = ThemedTk(theme="yaru")
    root.title("Importación masiva de registros del modelo 182")
    gui = GUI(root)

    gui.start()


if __name__ == "__main__":
    main()
