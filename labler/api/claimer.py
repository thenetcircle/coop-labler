from labler.db import IDatabase
import random
import logging

logger = logging.getLogger(__name__)


class Claimer(object):
    def __init__(self, env):
        self.env = env
        self.db: IDatabase = env.db

    def claim(self, project: str, user: str):
        try:
            return self.try_claim(project, user)
        except Exception as e:
            logger.error(f'could not claim: {str(e)}')
            logger.exception(e)
            return list()

    def try_claim(self, project, user):
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
