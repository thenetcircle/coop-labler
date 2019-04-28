from abc import ABC
from typing import List, Tuple, Set

from labler.cli.opts import AppSession
from labler.db.rdmbs.repr import LabelRepr, ClaimRepr, ProjectRepr, ExampleRepr


class IDatabase(ABC):
    def create_project(self, name, app: AppSession) -> None:
        raise NotImplementedError()

    def add_data_dir(self, name, app: AppSession) -> None:
        raise NotImplementedError()

    def get_data_dirs(self, project_name) -> Set[str]:
        raise NotImplementedError()

    def add_examples(self, project_name: str, app: AppSession, examples: List[Tuple[str, str, int, int]]) -> None:
        """
        :param project_name:
        :param app:
        :param examples: [(base_path, file_name, width, height)]
        :return:
        """

    def get_examples(self, project_name: str, file_path: str = None, disabled: bool = False) -> List[ExampleRepr]:
        raise NotImplementedError()

    def disable_example(self, example: ExampleRepr) -> None:
        raise NotImplementedError()

    def update_project(self, name, app: AppSession) -> None:
        raise NotImplementedError()

    def project_exists(self, name) -> bool:
        raise NotImplementedError()

    def get_claims(self, name=None, user=None) -> List[ClaimRepr]:
        raise NotImplementedError()

    def get_labels(self, project_name) -> List[LabelRepr]:
        raise NotImplementedError()

    def get_projects(self) -> List[ProjectRepr]:
        raise NotImplementedError()

    def get_project_names(self) -> List[str]:
        raise NotImplementedError()

    def get_unclaimed(self, project, limit=10, session=None) -> List[LabelRepr]:
        raise NotImplementedError()

    def get_claim(self, claim_id: int) -> ClaimRepr:
        raise NotImplementedError()

    def finish_claim(self, claim_id: int) -> None:
        raise NotImplementedError()

    def create_label_localization_or_detection(self, label: LabelRepr) -> None:
        raise NotImplementedError()

    def claim_for(self, to_claim: List[LabelRepr], user: str, session=None) -> None:
        raise NotImplementedError()
