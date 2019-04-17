from abc import ABC
from typing import List

from labler.cli import AppSession
from labler.db.rdmbs.repr import LabelRepr, ClaimRepr


class IDatabase(ABC):
    def create_project(self, name, app: AppSession) -> None:
        raise NotImplementedError()

    def update_project(self, name, app: AppSession) -> None:
        raise NotImplementedError()

    def project_exists(self, name) -> bool:
        raise NotImplementedError()

    def get_claims(self, name=None, user=None) -> List[ClaimRepr]:
        raise NotImplementedError()

    def get_projects(self) -> List[dict]:
        raise NotImplementedError()

    def get_project_names(self) -> List[str]:
        raise NotImplementedError()

    def get_unclaimed(self, project, limit=10, session=None) -> List[LabelRepr]:
        raise NotImplementedError()

    def claim_for(self, to_claim: List[LabelRepr], user: str, session=None) -> None:
        raise NotImplementedError()
