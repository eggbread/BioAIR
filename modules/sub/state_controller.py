import time
from drone.state import NodeState,TentacleState

class StateController(object):
    def __init__(self):
        pass

    def check_damaged_conditions(self, hyper_params, situation_params, node_params):
        '''
        :return: return whether next_tentacle_state is damaged
        '''
        # condition 19,20,21
        # 19. When it is determined that there is no communication with the adjacent node
        # 20. When it is determined that there is no communication with the origin node
        # 21. When it is determined that there is no communication with the destination node
        present_tentacle_state = node_params.tentacle_state
        if present_tentacle_state is TentacleState.Complete or present_tentacle_state is TentacleState.Reinforcing:
            if not (situation_params.origin_connection and situation_params.dest_connection):
                return True
        return False

    def check_orphan_conditions(self,hyper_params, situation_params, node_params):
        '''
        :return: whether next_node_state is damaged
        '''
        # hold_timer == 0 means that the node's tentacle is not damaged.
        if situation_params.hold_timer == 0:
            return False

        # condition 6 - After 30 seconds of holding and if there is no adjacent node, change from free to orphan
        if time.time()-situation_params.hold_timer > 30 and len(situation_params.adj_nodes) == 0:
            return True

        # condition 7 - After 30 seconds of holding, node can't communicate with Origin
        if time.time()-situation_params.hold_timer > 30 and situation_params.origin_connection is False:
            return True

        return False

    def get_next_state(self, hyper_params, situation_params, node_params, my_node_status):
        '''
        Based on updated SDP on the function - calculate_profile_and_update_situation_params,
        Decide next_state
        :return: next_tentacle_statem, next_node_state
        '''
        present_tentacle_state = node_params.tentacle_state
        present_node_state = node_params.node_state
        next_tentacle_state = present_tentacle_state
        next_node_state = present_node_state

        #change tentacle state from propaganta tentacle state
        if situation_params.latest_tentacle_state is not None and present_tentacle_state is not situation_params.latest_tentacle_state:
            next_tentacle_state = situation_params.latest_tentacle_state
            situation_params.latest_tentacle_state = None
            return next_tentacle_state, next_node_state

        if present_node_state is NodeState.Free:
            if present_tentacle_state is TentacleState.Forming:
                # sensor

                # condition sensor-1 - When a sensor node that has already been tip, and a free state normal node meets the tip node, the normal node becomes tip
                if situation_params.adj_tip == 1 and node_params.has_sensor is False:
                    adj_tips = [node_id for node_id in situation_params.adj_nodes if
                                     my_node_status[node_id]['node_state'] is NodeState.Tip]
                    is_tip_having_sensor = my_node_status[adj_tips[0]]['has_sensor']
                    if is_tip_having_sensor:
                        situation_params.tentacle_within_pos = my_node_status[adj_tips[0]]['tentacle_within_pos']
                        next_node_state = NodeState.Tip
                        return next_tentacle_state, next_node_state

                # condition sensor-2 - When there are multiple free nodes, one of them is sensor nodes.
                if situation_params.adj_free >= 1 and node_params.has_sensor is False:
                    adj_frees = [node_id for node_id in situation_params.adj_nodes if
                                     my_node_status[node_id]['node_state'] is NodeState.Free]
                    frees = adj_frees
                    frees_having_sensor = [node_id for node_id in adj_frees if my_node_status[node_id]['has_sensor'] is True]
                    if(len(frees_having_sensor) == 0):
                        pass
                    else:
                        frees_not_having_sensor = [node_id for node_id in frees if my_node_status[node_id]['has_sensor'] is False]
                        frees_not_having_sensor.append(node_params.node_id)
                        frees_not_having_sensor.sort()

                        if frees_not_having_sensor[0] == node_params.node_id:
                            situation_params.tentacle_within_pos = situation_params.next_attractor + 1
                            next_node_state = NodeState.Tip
                            return next_tentacle_state, next_node_state
                # sensor

                # condition 1 - Node has reached at the end of the tentacle, and also reached equilibrium
                if situation_params.equilibrium > 5 and (
                        situation_params.adj_tip + situation_params.adj_origin + situation_params.adj_backbone == 1):
                    situation_params.tentacle_within_pos = situation_params.next_attractor + 1
                    next_node_state = NodeState.Tip
                    return next_tentacle_state, next_node_state

                if situation_params.adj_tip == 1 and situation_params.adj_free == 1 and situation_params.tentacle_within_pos != -9999:
                    situation_params.tentacle_within_pos -= 1
                    next_node_state = NodeState.Tip
                    return next_tentacle_state, next_node_state

                if situation_params.adj_origin == 1 and situation_params.adj_free == 1 and situation_params.tentacle_within_pos != -9999:
                    situation_params.tentacle_within_pos -= 1
                    next_node_state = NodeState.Tip
                    return next_tentacle_state, next_node_state

                # condition 4 - When adjacent nodes both sides are tip (Damaged repaired - scenario 11)
                if situation_params.adj_tip == 2 and situation_params.tentacle_within_pos == -9999 and node_params.has_sensor is False:
                    adj_nodes = situation_params.adj_nodes
                    adj_tips = [node_id for node_id in adj_nodes if
                                     my_node_status[node_id]['node_state'] is NodeState.Tip]
                    adj_tip_pos_1 = my_node_status[adj_tips[0]]['tentacle_within_pos']
                    adj_tip_pos_2 = my_node_status[adj_tips[1]]['tentacle_within_pos']
                    if abs(adj_tip_pos_1-adj_tip_pos_2) > 1:
                        situation_params.tentacle_within_pos = int(( adj_tip_pos_1 + adj_tip_pos_2 ) / 2)
                        situation_params.origin_connection = True
                        situation_params.dest_connection = True
                        situation_params.global_count += 1
                        next_node_state = NodeState.Backbone
                        next_tentacle_state = TentacleState.Complete
                        return next_tentacle_state, next_node_state
                    else:
                        pass


                # condition 2 - Node connects to Destination
                if situation_params.origin_connection and situation_params.dest_connection and situation_params.adj_dest == 1:
                    situation_params.tentacle_within_pos = situation_params.next_attractor + 1
                    next_node_state = NodeState.Backbone
                    next_tentacle_state = TentacleState.Complete
                    return next_tentacle_state, next_node_state

                # condition 18 - When received latest Complete message from adjacent backbone
                if situation_params.origin_connection and situation_params.dest_connection:
                    next_node_state = NodeState.Backbone
                    next_tentacle_state = TentacleState.Complete
                    return next_tentacle_state, next_node_state

            # condition 5 - Self is remainder(or extra) free node
            if present_tentacle_state is TentacleState.Complete:
                next_node_state = NodeState.Extra
                return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Damaged:
                pass

            # condition 5 - Self is remainder(or extra) free node
            if present_tentacle_state is TentacleState.Reinforcing:
                next_node_state = NodeState.Extra
                return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        if present_node_state is NodeState.Tip:

            # sensor

            # condition sensor-3 - When a sensor node that has already been tip, and meets a free state normal node, the sensor node becomes free again.
            if node_params.has_sensor:
                if situation_params.adj_free or situation_params.adj_tip:
                    situation_params.tentacle_within_pos = -9999
                    next_node_state = NodeState.Free
                    return next_tentacle_state, next_node_state
            # sensor


            if present_tentacle_state is TentacleState.Forming:

                # condition 8 - By a new adjacent tip
                if situation_params.is_new_tip and node_params.has_sensor is False:
                    situation_params.is_new_tip = False
                    next_node_state = NodeState.Backbone
                    return next_tentacle_state, next_node_state

                #condition 10 - If in communication with Origin and Dest
                if situation_params.origin_connection and situation_params.dest_connection:
                    next_node_state = NodeState.Backbone
                    next_tentacle_state = TentacleState.Complete
                    return next_tentacle_state, next_node_state

                # condition 2 - Node connects to Destination
                if situation_params.origin_connection and situation_params.dest_connection and situation_params.adj_dest == 1:
                    next_node_state = NodeState.Backbone
                    next_tentacle_state = TentacleState.Complete
                    return next_tentacle_state, next_node_state

                # condition 4 - When adjacent nodes both sides are tip (Damaged repaired - scenario 11)
                if situation_params.adj_tip == 2 and node_params.has_sensor is False:
                    adj_nodes = situation_params.adj_nodes
                    adj_tips = [node_id for node_id in adj_nodes if
                                     my_node_status[node_id]['node_state'] is NodeState.Tip]
                    adj_tip_pos_1 = my_node_status[adj_tips[0]]['tentacle_within_pos']
                    adj_tip_pos_2 = my_node_status[adj_tips[1]]['tentacle_within_pos']
                    if abs(adj_tip_pos_1-adj_tip_pos_2) > 1:
                        situation_params.tentacle_within_pos = int(( adj_tip_pos_1 + adj_tip_pos_2 ) / 2)
                        situation_params.origin_connection = True
                        situation_params.dest_connection = True
                        situation_params.global_count += 1
                        next_node_state = NodeState.Backbone
                        next_tentacle_state = TentacleState.Complete
                        return next_tentacle_state, next_node_state
                    else:
                        pass

            # condition 18 - When received latest Complete message from adjacent backbone
            if present_tentacle_state is TentacleState.Complete:
                next_node_state = NodeState.Backbone
                return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Damaged:

                # condition 13 - If in communication only with Origin
                if situation_params.origin_connection:
                    next_tentacle_state = TentacleState.Forming
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Reinforcing:
                pass

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        if present_node_state is NodeState.Backbone:
            if present_tentacle_state is TentacleState.Forming:

                #condition 10 - If in communication with Origin and Dest
                if situation_params.origin_connection and situation_params.dest_connection:
                    next_node_state = NodeState.Backbone
                    next_tentacle_state = TentacleState.Complete
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Complete:
                pass

            if present_tentacle_state is TentacleState.Damaged:

                # condition 11 - When Node is  at the end backbone of the tentacle in a Damaged Tentacle
                if situation_params.adj_origin == 0 and situation_params.adj_dest == 0 and situation_params.adj_backbone == 1 and situation_params.adj_tip == 0 \
                        or (situation_params.adj_origin == 1 and situation_params.adj_backbone == 0 and situation_params.adj_tip ==0) \
                        or (situation_params.adj_dest == 1 and situation_params.adj_backbone == 0 and situation_params.adj_tip ==0):
                    next_node_state = NodeState.Tip
                    return next_tentacle_state, next_node_state

                # condition 13 - If in communication only with Origin
                if situation_params.origin_connection:
                    next_tentacle_state = TentacleState.Forming
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Reinforcing:
                pass

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        if present_node_state is NodeState.Extra:
            if present_tentacle_state is TentacleState.Forming:
                pass

            # condition 12 - When Node has good signal quality with the backbone being be backed up by it
            if present_tentacle_state is TentacleState.Complete:
                if situation_params.complete_reinforce > 5 :
                    situation_params.complete_reinforce = 0
                    situation_params.reinforcing = situation_params.anchoring
                    situation_params.anchoring = -9999
                    situation_params.hold = True
                    situation_params.global_count = situation_params.global_count + 1
                    next_node_state = NodeState.Reinforce
                    next_tentacle_state = TentacleState.Reinforcing

                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Damaged:
                pass

            # condition 12 - When Node has good signal quality with the backbone being be backed up by it
            if present_tentacle_state is TentacleState.Reinforcing:
                if situation_params.complete_reinforce > 5:
                    situation_params.complete_reinforce = 0
                    situation_params.reinforcing = situation_params.anchoring
                    situation_params.anchoring = -9999
                    situation_params.hold = True
                    next_node_state = NodeState.Reinforce
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        if present_node_state is NodeState.Reinforce:
            if present_tentacle_state is TentacleState.Forming:
                pass

            if present_tentacle_state is TentacleState.Complete:
                pass

            # condition 15 - The exploded backbone is (not) my backup node
            if present_tentacle_state is TentacleState.Damaged:
                if not (situation_params.reinforcing in situation_params.adj_nodes):
                    situation_params.tentacle_within_pos = my_node_status[situation_params.reinforcing]['tentacle_within_pos']
                next_node_state = NodeState.Free
                next_tentacle_state = TentacleState.Forming
                situation_params.latest_tentacle_state = None
                situation_params.hold = False
                return next_tentacle_state, next_node_state
                # else:
                #     pass

            if present_tentacle_state is TentacleState.Reinforcing:
                pass

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        if present_node_state is NodeState.Orphan:

            # condition 17 - When Orphan reconnects to the Tentacle when returning to origin
            if present_tentacle_state is TentacleState.Forming:
                if situation_params.origin_connection:
                    next_node_state = NodeState.Free
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Complete:
                pass

            # condition 17 - When Orphan reconnects to the Tentacle when returning to origin
            if present_tentacle_state is TentacleState.Damaged:
                if situation_params.origin_connection:
                    next_tentacle_state = TentacleState.Forming
                    next_node_state = NodeState.Free
                    situation_params.global_count += 1
                    return next_tentacle_state, next_node_state

            if present_tentacle_state is TentacleState.Reinforcing:
                pass

            if present_tentacle_state is TentacleState.Next_Destination:
                pass

        return next_tentacle_state,next_node_state

    def virtual_origin_mode_state_manage(self, hyper_params, situation_params, node_params, my_node_status):
        present_tentacle_state = node_params.tentacle_state
        present_node_state = node_params.node_state
        next_tentacle_state = present_tentacle_state
        next_node_state = present_node_state

        virtual_origin_id = node_params.virtual_target

        if virtual_origin_id == node_params.node_id and node_params.node_state is not NodeState.Origin:
            return next_tentacle_state, next_node_state

        else:
            if situation_params.virtual_origin_trigger:
                situation_params.virtual_origin_trigger = False
                node_params.virtual_target = node_params.node_id
                situation_params.global_count += 1
            return next_tentacle_state, next_node_state
