import enum

class NodeState(enum.Enum):
    Free = 1
    Tip = 2
    Backbone = 3
    Extra = 4
    Reinforce = 5
    Orphan = 6
    Origin = 7
    Destination = 8
    Target = 9


class TentacleState(enum.Enum):
    Forming = 1
    Complete = 2
    Damaged = 3
    Reinforcing = 4
    Next_Destination = 5
