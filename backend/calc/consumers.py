import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import os
import numpy as np

DATA_FILE_PATH = os.path.join(settings.BASE_DIR, 'calc', 'data_files', 'data.json')

def load_json_file(file_path):
    import json
    with open(file_path, 'r') as file:
        content = json.load(file)
        return content

data = load_json_file(DATA_FILE_PATH)
tables_structure = data['tables_structure']
guest_rel = data['guest_relations']
group_rel = data['group_relations']
group_mapping = data['groups']
guest_mapping = data['guests']

num_guests = len(data['guests'])
num_tables = len(tables_structure)
total_seats = sum(sum(row) for row in tables_structure)

def get_neighbours(idx):
    remaining_idx = idx
    found_seat = False
    for table_id, table_seats in enumerate(tables_structure):
        if found_seat:
            break
        for direction_idx, seats_num in enumerate(table_seats):
            if remaining_idx >= seats_num :
                remaining_idx -= seats_num 
            else:
                found_seat = True
                target_table_id = table_id
                target_table_seats = table_seats
                break

    if remaining_idx == 0 and (direction_idx == 0 or (direction_idx > 0 and target_table_seats[direction_idx - 1] == 0)):
        left = None
    else:
        left = idx - 1

    if remaining_idx + 1 == target_table_seats[direction_idx] and (direction_idx + 1 == len(target_table_seats) or (direction_idx + 1 < len(target_table_seats) and target_table_seats[direction_idx + 1] == 0)):
        right = None
    else:
        right = idx + 1

    return left, right

seat_neighbours = {}
for i in range(total_seats):
    seat_neighbours[i] = get_neighbours(i)

relationship_matrix = np.zeros((98, 98))

# Populating matrix with person to person relations
for k,v in guest_rel.items():
    a,b = k.strip('()').split(',')
    relationship_matrix[int(a), int(b)] += int(v)
    relationship_matrix[int(b), int(a)] += int(v)

# Adding free seats to the pool
for i in range(len(guest_mapping), total_seats):
    guest_mapping[str(i)] = {'name': 'Free Seat', 'group': '10'}

group_indices = {}
for idx, item in guest_mapping.items():
    if 'group' in item:
        group = item['group']
        if group not in group_indices:
            group_indices[group] = []
        group_indices[group].append(idx)

# Populating matrix with group relations
for k,v in group_rel.items():
    a,b = k.strip('()').split(',')
    group_a = group_indices[a]
    group_b = group_indices[b]
    for x in group_a:
        for y in group_b:
            relationship_matrix[int(x), int(y)] += int(v)

sex_indices = {}
for idx, item in guest_mapping.items():
    if 'sex' in item:
        sex = item['sex']
        if sex not in sex_indices:
            sex_indices[sex] = []
        sex_indices[sex].append(idx)

females = sex_indices['female']
males = sex_indices['male']

# Populating matrix with opposite sex relations
for f in females:
    for m in males:
        relationship_matrix[int(f), int(m)] -= 10
        relationship_matrix[int(m), int(f)] -= 10

# Matrix Normalization
min_value = np.min(relationship_matrix)
max_value = np.max(relationship_matrix)
relationship_matrix = (relationship_matrix - min_value) / (max_value - min_value)
relationship_matrix = np.round(relationship_matrix, 3)

# # Adding free seats to the pool
# for i in range(num_guests, total_seats):
#     relationship_matrix[i, :] = 0
#     relationship_matrix[:, i] = 0

# Parameters
initial_temperature = 100.0
cooling_rate = 0.95
max_iterations = 1000

class CalculationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_stop_calculation = False
        self.running_task = None

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        if text_data == 'start':
            if self.running_task is None or self.running_task.done():
                self.should_stop_calculation = False
                self.running_task = asyncio.create_task(self.run_simulated_annealing())
        elif text_data == 'stop':
            self.should_stop_calculation = True
            if self.running_task:
                self.running_task.cancel()

    def calculate_cost(self, seating_arrangement):
        total_cost = 0
        seat_costs = np.zeros(total_seats)
        
        for i in range(total_seats):
            left_person_id, right_person_id = seat_neighbours[i]

            middle_person = seating_arrangement[i]

            if left_person_id:
                left_person = seating_arrangement[left_person_id]
                relationship_left = relationship_matrix[left_person][middle_person]
            else:
                relationship_left = 1

            if right_person_id:
                right_person = seating_arrangement[right_person_id]
                relationship_right = relationship_matrix[middle_person][right_person]
            else:
                relationship_right = 1

            seat_costs[i] = (relationship_left + relationship_right) / 2
            total_cost += seat_costs[i]
        
        return total_cost, seat_costs
    
    async def run_simulated_annealing(self):
        current_arrangement = np.arange(total_seats)
        np.random.shuffle(current_arrangement)
        current_cost, current_seat_costs = self.calculate_cost(current_arrangement)
        best_arrangement = current_arrangement.copy()
        best_cost = current_cost
        best_seat_costs = current_seat_costs
        temperature = initial_temperature
        
        for iteration in range(max_iterations):

            if self.should_stop_calculation:
                break  # Exit the loop if a stop signal is received

            new_arrangement = current_arrangement.copy()
            i, j = np.random.choice(total_seats, size=2, replace=False)
            new_arrangement[i], new_arrangement[j] = new_arrangement[j], new_arrangement[i]
            new_cost, new_seat_costs = self.calculate_cost(new_arrangement)
            
            if new_cost < current_cost or np.random.rand() < np.exp((current_cost - new_cost) / temperature):
                current_arrangement = new_arrangement
                current_cost = new_cost
                current_seat_costs = new_seat_costs
                
                if new_cost < best_cost:
                    best_arrangement = new_arrangement
                    best_cost = new_cost
                    best_seat_costs = new_seat_costs
            
            temperature *= cooling_rate

            # Prepare result data to send
            result_data = {
                "iteration": iteration + 1,
                "arrangement": [str(x) for x in best_arrangement.tolist()],
                "score": best_cost,
                "seatCosts": [float(x) for x in current_seat_costs.tolist()]
            }
            
            # print(result_data)

            # Send result data to WebSocket client
            await self.send(json.dumps(result_data))
            await asyncio.sleep(0.1)