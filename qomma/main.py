import argparse
from qomma.Handlers.PathHandler import PathHandler
from qomma.Controllers.Controller import Controller
from qomma.Readers.ReaderFactory import ReaderFactory


def main(path_handler: PathHandler, controller: Controller) -> None:
    """
    Entry point of the project. Receives a path right from command line, inits Database object creation and send it
    to controller.
    """
    parser = argparse.ArgumentParser(description='Qomma project')

    parser.add_argument('path', action="store", help="Path to the folder with CSV files")

    args = parser.parse_args()
    database = path_handler.handle(args.path)
    if database.has_error():
        print('Error occurred while trying to read folder you provided')

    controller.init(database)


if __name__ == '__main__':
    main(PathHandler(ReaderFactory()), Controller())
