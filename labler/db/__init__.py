from abc import ABC
from typing import List

from labler.cli.opts import AppSession
from labler.db.rdmbs.repr import LabelRepr, ClaimRepr, ProjectRepr


class IDatabase(ABC):
    def create_project(self, name, app: AppSession) -> None:
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
