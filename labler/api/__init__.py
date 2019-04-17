from typing import List

from labler.db import ClaimRepr


class IClaimer(object):
    def claim(self, project: str, user: str) -> List[ClaimRepr]:
        raise NotImplementedError()

    def submit_classification(self, claim_id, content) -> None:
        raise NotImplementedError()

    def submit_detection(self, claim_id, content) -> None:
        raise NotImplementedError()

    def submit_localization(self, claim_id, content) -> None:
        raise NotImplementedError()

    def submit_segmentation(self, claim_id, content) -> None:
        raise NotImplementedError()


class IImager(object):
    def load_b64(self, file_path, file_name) -> str:
        pass
