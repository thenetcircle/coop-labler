from labler.db import IDatabase
import random


class Claimer(object):
    def __init__(self, env):
        self.env = env
        self.db: IDatabase = env.db

    def claim(self, project: str, user: str):
        current_claims = self.db.get_claims(project, user)

        if len(current_claims) > 10:
            return current_claims

        unclaimed = self.db.get_unclaimed(project, limit=100)
        to_claim = random.sample(unclaimed, 10)

        claims = self.db.claim_for(to_claim, user)
        current_claims.extend(claims)

        return [claim.to_dict() for claim in current_claims]
