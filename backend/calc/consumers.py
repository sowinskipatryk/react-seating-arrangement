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

# REFRESH_RATE = 5  # in seconds
# RUNTIME = 1  # in minutes

# # def load_text_file(file_name):
# #     file_path = os.path.join(settings.BASE_DIR, 'calc', 'data_files', file_name)
# #     with open(file_path, 'r') as file:
# #         content = file.readlines()
# #         content = [x.replace('\n', '') for x in content]
# #         return content

# data_file_path = os.path.join(settings.BASE_DIR, 'calc', 'data_files', 'data.xls')

# table_sizes = pd.read_excel(data_file_path, 'TableSizes')['TableSizes'].to_list()
# scores_df = pd.read_excel(data_file_path, 'GroupScores')

# scores_df_swapped = scores_df.rename(columns={'Group A': 'Group B', 'Group B': 'Group A'})

# merged_scores_df = pd.concat([scores_df, scores_df_swapped])

# unique_scores_df = merged_scores_df.drop_duplicates(subset=['Group A', 'Group B'])

# GuestListRaw = pd.read_excel(data_file_path, 'GuestList')

# guest_list=GuestListRaw["Guest"].values.tolist()

# pairs = list(itertools.combinations(GuestListRaw['Guest'], 2))

# PairsList = pd.DataFrame(pairs, columns=['Person A', 'Person B'])

# GroupRel = PairsList.merge(GuestListRaw, left_on='Person A', right_on='Guest').drop(columns=['Guest', 'Together', 'Apart', 'ScoreTogether', 'ScoreApart'])

# GroupRel = GroupRel.rename(columns={'Group': 'Group A'})
# GroupRel = GroupRel.merge(GuestListRaw, left_on='Person B', right_on='Guest').drop(columns=['Guest', 'Together', 'Apart', 'ScoreTogether', 'ScoreApart'])
# GroupRel = GroupRel.rename(columns={'Group': 'Group B'})
# GroupRel = GroupRel.merge(unique_scores_df, on=['Group A', 'Group B'], how='left')
# GroupRel = GroupRel[['Person A', 'Person B', 'Score']]
# GroupRel = GroupRel.dropna(subset=['Score'])

# RelMatrixRaw=GuestListRaw.dropna(thresh=2)

# Together=RelMatrixRaw[["Guest","Together","ScoreTogether"]].dropna(thresh=2)

# Apart=RelMatrixRaw[["Guest","Apart","ScoreApart"]].dropna(thresh=2)

# groups = unique_values = RelMatrixRaw['Group'].unique()

# relationships_edges={}

# # Group relationships are less important than direct relationships hence they go first
# for row in GroupRel.values.tolist():
#     relationships_edges.update({tuple(row[:2]): row[2]})

# for element in list(zip(Together["Guest"], Together["Together"], Together['ScoreTogether'])):
#         relationships_edges.update({element[:2]: element[2]})
#         relationships_edges.update({element[-2::-1]: element[2]})
        
# for element in list(zip(Apart["Guest"], Apart["Apart"], Apart['ScoreApart'])):
#         relationships_edges.update({element[:2]: element[2]})
#         relationships_edges.update({element[-2::-1]: element[2]})

# seats_num = sum(table_sizes)

# table_count = len(table_sizes)

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

# if sum(table_sizes) > len(guest_list):
#     guest_list.extend(['Wolne'] * (sum(table_sizes) - len(guest_list)))

# temp_graph = nx.Graph()
# for k, v in relationships_edges.items():
#     temp_graph.add_edge(k[0], k[1], weight=v)

# for node in guest_list:
#     if not temp_graph.has_node(node):
#         temp_graph.add_node(node)

# relationships_mat_unnormed = nx.to_numpy_matrix(temp_graph.to_undirected(), nodelist=guest_list)
# relationships_mat = relationships_mat_unnormed / 100

# RelationshipMatrix=pd.DataFrame(relationships_mat)
# RelationshipMatrix.index=guest_list
# RelationshipMatrix.columns=guest_list
# RelationshipMatrix = RelationshipMatrix[(RelationshipMatrix.T != 0).any()] # removes rows where all elements = 0 (no rel)
# RelationshipMatrix = RelationshipMatrix.loc[:, (RelationshipMatrix != 0).any(axis=0)] # removes columns where all elements = 0

# s = list(range(seats_num))
# random.shuffle(s)
# s = [ x+1 for x in s]
# s
# Table_Arrangement=pd.DataFrame(zip(guest_list,s),columns=["Guest Name","Assigned Seat No"])
# Table_Arrangement["Assigned Table No"]=Table_Arrangement["Assigned Seat No"].apply(get_table_number)

# for i in range(1,table_count+1):
#     Table_Arrangement["Table No "+str(i)]=np.where(Table_Arrangement['Assigned Table No']!= i, 0, 1)
    
# Table_Arrangement_Transpose=Table_Arrangement.T
# Table_Arrangement_Transpose=Table_Arrangement_Transpose.tail(len(Table_Arrangement_Transpose)-3)
# initial_random_arrangement=Table_Arrangement_Transpose.values

# initial_random_arrangement_costs = np.matrix(initial_random_arrangement) * relationships_mat * initial_random_arrangement.T

# class CalculationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def receive(self, text_data):
#         if text_data == 'start calculation':
#             await self.run_simmulated_annealing()

#     async def send_anneal_result(self, pos_current):
#         result = {'pos_current': pos_current}
#         await self.send(json.dumps(result))

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

#     def take_step(self, pos):
#         table_seats = reshape_to_table_seats(np.matrix(pos, copy=True))
#         # randomly swap two guests
#         table_from, table_to = np.random.choice(table_count, 2, replace=False)
        
#         table_from_guests = np.where(table_seats[table_from] == 1)[1]
#         table_to_guests = np.where(table_seats[table_to] == 1)[1]
        
#         table_from_guest = np.random.choice(table_from_guests)
#         table_to_guest = np.random.choice(table_to_guests)
        
#         table_seats[table_from, table_from_guest] = 0
#         table_seats[table_from, table_to_guest] = 1
#         table_seats[table_to, table_to_guest] = 0
#         table_seats[table_to, table_from_guest] = 1
#         return table_seats

#     def calculate_acceptance_probability(self, cost_old, cost_new, temp):
#         a = 1 if cost_new < cost_old else np.exp((cost_old - cost_new) / temp)
#         return a

num_tables = 6
num_seats_per_table = 20
total_seats = num_tables * num_seats_per_table
relationship_matrix = np.random.randint(0, 120, size=(total_seats, total_seats))

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
                "arrangement": [int(x) for x in best_arrangement.tolist()],
                "score": best_cost,
                "seatCosts": [int(x) for x in current_seat_costs.tolist()]
            }
            
            print(result_data)

            # Send result data to WebSocket client
            await self.send(json.dumps(result_data))
            await asyncio.sleep(0.1)