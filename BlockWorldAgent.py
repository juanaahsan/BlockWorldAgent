import copy
Table = 'Table'
class BlockWorldAgent:
    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):

        total = self.total_blocks(initial_arrangement)
        current_config = copy.deepcopy(initial_arrangement)
        moves = []
        visited = {}

        while self.misplaced_blocks_calculation(current_config, goal_arrangement, total) > 0:
            current_signature = self.stack_to_tuple_conversion(current_config)
            if current_signature in visited:
                break
            visited[current_signature] = True

            updated_config, current_move = self.identify_best_move(current_config, goal_arrangement, total)
            if current_move is None:
                break

            current_config = updated_config
            moves.append(current_move)

        return moves

    def total_blocks(self, configuration):
        return sum(len(stack) for stack in configuration)

    def stack_to_tuple_conversion(self, initial_arrangement):
        return tuple(tuple(stack) for stack in initial_arrangement)

    def misplaced_blocks_calculation(self, current_state, goal_state, total):

        correct_placements = 0
        for curr_stack in current_state:
            for goal_stack in goal_state:
                index = 0
                while (index < len(curr_stack) and
                       index < len(goal_stack) and
                       curr_stack[index] == goal_stack[index]):
                    correct_placements += 1
                    index += 1
        return total - correct_placements

    def identify_best_move(self, current, goal, total):

        optimal_sequence = 0
        optimal_move = 0
        least_misplaced = float('inf')

        for curr_index, curr_stack in enumerate(current):
            if not curr_stack:
                continue  
     
            for goal_index in range(len(current)):
                if curr_index == goal_index:
                    continue 

                new_config, move = self.move_execution(current, curr_index, goal_index)
                misplaced = self.misplaced_blocks_calculation(new_config, goal, total)

                if misplaced < least_misplaced:
                    least_misplaced = misplaced
                    optimal_sequence = new_config
                    optimal_move = move

            if len(curr_stack) > 1:
                new_config, move = self.move_execution(current, curr_index, -1)
                misplaced = self.misplaced_blocks_calculation(new_config, goal, total)

                if misplaced <= least_misplaced:
                    least_misplaced = misplaced
                    optimal_sequence = new_config
                    optimal_move = move

        return optimal_sequence, optimal_move

    def move_execution(self, config, from_index, to_index):


        new_config = copy.deepcopy(config)
        moving_block = config[from_index][-1]

        new_config[from_index] = config[from_index][:-1]

        if to_index == -1:

            new_config.append([moving_block])
            goal = Table
        else:

            new_config[to_index] = config[to_index] + [moving_block]
            goal = config[to_index][-1] if config[to_index] else Table


        if not new_config[from_index]:
            del new_config[from_index]


        move = (moving_block, goal)
        return new_config, move
