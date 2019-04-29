from typing import List

from labler import errors
from labler.api import IClaimer
from labler.db import IDatabase, ClaimRepr, LabelRepr
import random
import logging

from labler.db.rdmbs.repr import LabelStatuses
from labler.environ import LablerEnvironment

logger = logging.getLogger(__name__)


class Claimer(IClaimer):
    def __init__(self, env: LablerEnvironment):
        self.env = env
        self.db: IDatabase = env.db

    def claim(self, project: str, user: str) -> List[ClaimRepr]:
        try:
            return self.try_claim(project, user)
        except Exception as e:
            logger.error(f'could not claim: {str(e)}')
            logger.exception(e)
            return list()

    def try_claim(self, project, user) -> List[ClaimRepr]:
        current_claims = self.db.get_claims(project, user)

        if len(current_claims) > 10:
            return current_claims

        unclaimed = self.db.get_unclaimed(project, limit=100)

        k = 10
        if k > len(unclaimed):
            k = len(unclaimed)

        to_claim = random.sample(unclaimed, k)

        self.db.claim_for(to_claim, user)
        return self.db.get_claims(project, user)

    def submit_localization(self, claim_id, content: dict) -> None:
        claim = self.db.get_claim(claim_id)
        if claim is None:
            raise errors.LablerException(f'no claim found for claim ID {claim_id}')

        json_labels = content.get('labels')
        for json_label in json_labels:
            self._submit_localization(claim, json_label)

        self.db.finish_claim(claim_id)

    def _submit_localization(self, claim: ClaimRepr, content: dict) -> None:
        xmin = content.get('xmin', None)
        xmax = content.get('xmax', None)
        ymin = content.get('ymin', None)
        ymax = content.get('ymax', None)

        try:
            map(int, [xmin, xmax, ymin, ymax])
        except ValueError:
            raise errors.LablerException('found non-integer coordinates in data')

        if None in (xmin, xmax, ymin, ymax):
            raise errors.LablerException(f'found null coordinate in data')

        target_class = content.get('target_class', None)
        if target_class is None:
            raise errors.LablerException(f'no target_class in data')

        label = LabelRepr(
            file_path=claim.file_path,
            file_name=claim.file_name,
            project_name=claim.project_name,
            target_class=target_class,
            submitted_by=claim.claimed_by,
            status=LabelStatuses.FINISHED,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax
        )

        self.db.create_label_localization_or_detection(label)

    def submit_segmentation(self, claim_id, content) -> None:
        raise NotImplementedError()

    def submit_classification(self, claim_id, content) -> None:
        raise NotImplementedError()

    def submit_detection(self, claim_id, content) -> None:
        raise NotImplementedError()
