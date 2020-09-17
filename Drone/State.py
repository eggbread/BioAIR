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

    @staticmethod
    def str_to_node_state(nodeState):
        if nodeState == "FREE":
            return NodeState.Free
        if nodeState == "TIP":
            return NodeState.Tip
        if nodeState == "BACKBONE":
            return NodeState.Backbone
        if nodeState == "EXTRA":
            return NodeState.Extra
        if nodeState == "REINFORCE":
            return NodeState.Reinforce
        if nodeState == "ORPHAN":
            return NodeState.Orphan
        if nodeState == "ORIGIN":
            return NodeState.Origin
        if nodeState == "DEST":
            return NodeState.Destination

    @staticmethod
    def node_state_to_str(nodeState):
        if nodeState is NodeState.Free:
            return "FREE"
        if nodeState is NodeState.Tip:
            return "TIP"
        if nodeState is NodeState.Backbone:
            return "BACKBONE"
        if nodeState is NodeState.Extra:
            return "EXTRA"
        if nodeState is NodeState.Reinforce:
            return "REINFORCE"
        if nodeState is NodeState.Orphan:
            return "ORPHAN"
        if nodeState is NodeState.Origin:
            return "ORIGIN"
        if nodeState is NodeState.Destination:
            return "DEST"


class TentacleState(enum.Enum):
    Forming = 1
    Complete = 2
    Damaged = 3
    Reinforcing = 4
    Next_Destination = 5

    @staticmethod
    def str_to_tentacle_state(tentacleState):
        if tentacleState == "FORMING":
            return TentacleState.Forming
        if tentacleState == "COMPLETE":
            return TentacleState.Complete
        if tentacleState == "DAMAGED":
            return TentacleState.Damaged
        if tentacleState == "REINFORCING":
            return TentacleState.Reinforcing
        if tentacleState == "NEXT_DEST":
            return TentacleState.Next_Destination

    @staticmethod
    def tentacle_state_to_str(tentacle_state):
        if tentacle_state is TentacleState.Forming:
            return "FORMING"
        if tentacle_state is TentacleState.Complete:
            return "COMPLETE"
        if tentacle_state is TentacleState.Damaged:
            return "DAMAGED"
        if tentacle_state is TentacleState.Reinforcing:
            return "REINFORCING"
        if tentacle_state is TentacleState.Next_Destination:
            return "NEXT_DEST"
        if tentacle_state is None:
            return "None"
