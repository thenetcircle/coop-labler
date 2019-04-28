from abc import ABC

from labler.cli import AppSession


class IDataHandler(ABC):
    def add_data_dir(self, project_name: str, app: AppSession, data_dir: str) -> None:
        raise NotImplementedError()

    def sync_data_dir(self, project_name: str, app: AppSession, data_dir: str) -> None:
        raise NotImplementedError()
