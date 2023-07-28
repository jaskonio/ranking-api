"""_summary_

Returns:
    _type_: _description_
"""
from datetime import datetime
from typing import List
from pydantic import Field
from app.model.BaseMongoModel import BaseMongoModel
from app.model.OID import OID
from app.model.runner_model import RunnerModel

class RaceBaseModel(BaseMongoModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    id: OID = Field(default_factory=OID)
    name: str
    url: str
    processed: bool = False
    sorted: bool = False
    ranking: List[RunnerModel] = Field(default_factory=list)
    proceesEnabled: bool = False

    def set_ranking(self, runner):
        """_summary_

        Args:
            runner (_type_): _description_
        """
        self.ranking.clear()
        self.ranking.extend(runner)

        if len(self.ranking) == 0:
            return

        self.__sort_ranking__()
        self.processed = True

    def get_ranking(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if not self.sorted:
            self.__sort_ranking__()

        return self.ranking

    def __sort_ranking__(self):
        """_summary_
        """
        format = "%H:%M:%S"

        # Orderna los Runner primero por finished
        # True primero y False segundo
        # tiempos que se tienen en cuenta realTime y officialTime
        runners_finished = sorted(self.ranking,
                                  key=lambda runner: (not runner.finished,
                                                    datetime.strptime(runner.realTime, format),
                                                    datetime.strptime(runner.officialTime, format)),
                                  reverse=False)

        self.ranking = runners_finished

        self.sorted = True
