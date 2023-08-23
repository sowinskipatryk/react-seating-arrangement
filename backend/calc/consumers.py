import asyncio
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import os
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pandas as pd
import random
import itertools

DATA_FILE_PATH = os.path.join(settings.BASE_DIR, 'calc', 'data_files', 'data.json')

def load_json_file(file_path):
    import json
    with open(file_path, 'r') as file:
        content = json.load(file)
        return content

# def get_table_number(seat_number):
#     counter = 1
#     for tid, table_size in enumerate(table_sizes):
#         if 0 < seat_number < counter + table_size:
#             return tid + 1
#         counter += table_size

# def reshape_to_table_seats(x):
#     table_seats = x.reshape(table_count, len(guest_list))
#     return table_seats

# def prob_accept(cost_old, cost_new, temp):
#     a = 1 if cost_new < cost_old else np.exp((cost_old - cost_new) / temp)
#     return a

# temp_graph = nx.Graph()
# for k, v in relationships_edges.items():
#     temp_graph.add_edge(k[0], k[1], weight=v)

# for node in guest_list:
#     if not temp_graph.has_node(node):
#         temp_graph.add_node(node)

# relationships_mat_unnormed = nx.to_numpy_matrix(temp_graph.to_undirected(), nodelist=guest_list)
# relationships_mat = relationships_mat_unnormed / 100

# class CalculationConsumer(AsyncWebsocketConsumer):
#     async def anneal_async(self, pos_current, temp=1.0, temp_min=0.00001, alpha=0.9, n_iter=100):
#         cost_old = self.calculate_cost(pos_current)

#         while temp > temp_min:
#             for i in range(0, n_iter):
#                 pos_new = self.take_step(pos_current)
#                 cost_new = self.calculate_cost(pos_new)
#                 p_accept = self.calculate_acceptance_probability(cost_old, cost_new, temp)
#                 if p_accept > np.random.random():
#                     pos_current = pos_new
#                     cost_old = cost_new
#                     await self.send_anneal_result(pos_current)
#                 await asyncio.sleep(0)  # Allow other tasks to run during the loop
#             temp *= alpha

#     async def run_simulated_annealing(self):
#         initial_pos = 0 # initialize initial position
#         await self.anneal_async(initial_pos)

#     async def calculate_cost(self, pos):
#         table_seats = reshape_to_table_seats(pos)
#         seat_costs = table_seats * relationships_mat
#         table_costs = seat_costs * table_seats.T
#         table_cost = np.trace(table_costs)
#         return table_cost

#     def calculate_acceptance_probability(self, cost_old, cost_new, temp):
#         a = 1 if cost_new < cost_old else np.exp((cost_old - cost_new) / temp)
#         return a


data = load_json_file(DATA_FILE_PATH)
num_seats_per_table = data['table_sizes']
guest_rel = data['guest_relations']
group_rel = data['group_relations']
group_mapping = data['groups']
guest_mapping = data['guests']

num_tables = len(num_seats_per_table)
total_seats = sum(num_seats_per_table)

# Adding free seats to the pool
for i in range(len(guest_mapping), total_seats):
    guest_mapping[str(i)] = {'name': 'Free Seat'}

relationship_matrix = np.zeros((98, 98))

# Populating matrix with person to person relations
for k,v in guest_rel.items():
    a,b = k.strip('()').split(',')
    relationship_matrix[int(a), int(b)] += int(v)
    relationship_matrix[int(b), int(a)] += int(v)

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

# print(relationship_matrix)

# Parameters
initial_temperature = 100.0
cooling_rate = 0.95
max_iterations = 1000

class CalculationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        if text_data == 'start calculation':
            await self.run_simulated_annealing()

    def calculate_cost(self, seating_arrangement):
        total_cost = 0
        seat_costs = np.zeros(total_seats)
        
        for i in range(total_seats):
            left_person = seating_arrangement[i]
            right_person = seating_arrangement[(i + 1) % total_seats]
            seat_costs[i] = relationship_matrix[left_person][right_person]
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
                "arrangement": [guest_mapping[str(x)]['name'] for x in best_arrangement.tolist()],
                "score": best_cost,
                "seatCosts": [float(x) for x in current_seat_costs.tolist()]
            }
            
            print(result_data)

            # Send result data to WebSocket client
            await self.send(json.dumps(result_data))
            await asyncio.sleep(0.1)