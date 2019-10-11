import numpy as np
import pygame


class brutal_ai:
    '''
    AI powered by the classic path finding algorithm - A star algorithm
    '''
    
    def __init__(self, map_instance):
        
        self._ref_map = map_instance
        self._sqrDist = self._ref_map.get_scale()
        self._direction_rep = {(self._sqrDist, 0): "D", (-self._sqrDist, 0): "A", (0, self._sqrDist): "S", (0, -self._sqrDist): "W"}
        
    def get_path(self):
        
        def cost_function(here: tuple, there: tuple):
            return np.sqrt((here[0] - there[0])**2 + (here[1] - there[1])**2)
            
        def construct_path(cameFrom, Current):
            total_path = [Current]
            while Current in cameFrom.keys():
                Current = cameFrom[Current]
                total_path.append(Current)

            get_vector = lambda f, i: self._direction_rep[tuple(np.array(f) - np.array(i))]
            
            path_lenth = len(total_path) - 1
            total_path = [get_vector(total_path[n], total_path[n+1]) for n in range(path_lenth)]
            
            return total_path
        
        fCost, sCost = dict(), dict()
        for cor in self._ref_map.get_map():
            sCost[tuple(cor)], fCost[tuple(cor)] = 10**9, 10**9
        
        
        start = tuple(self._ref_map.get_snk_pos())
        end = tuple(self._ref_map.get_food_pos())
        snk_body = self._ref_map.get_snk_body()
        tail_index = 0
        
        camefrom = dict()
        sCost[start] = 0
        fCost[start] = cost_function(start, end)

        openSet = [start]
        closedSet = []
        
        while openSet:
            current = openSet[np.argmin([fCost[n] for n in openSet])]

            if current == end:
                return construct_path(camefrom, current)
                
            openSet.remove(current)
            closedSet.append(current)
            
            neighbors = self._ref_map.get_neighbors(current)
            
            for key, neighbor in neighbors.items():
                
                if neighbor == None:
                    continue
                
                elif neighbor in closedSet:
                    continue
                
                elif neighbor in snk_body[1:]:
                    tail_index = max([tail_index, snk_body.index(neighbor)])
                    continue
                
                tentative_sCost = sCost[current] + self._sqrDist
                
                if neighbor not in openSet:
                    openSet.append(neighbor)
                
                elif tentative_sCost >= fCost[neighbor]:
                    continue
                
                camefrom[neighbor] = current
                sCost[neighbor] = tentative_sCost
                fCost[neighbor] = sCost[neighbor] + cost_function(neighbor, end)
        
        
        if len(closedSet) <= 1:
            return []
        
        while tail_index > 0:
            end = snk_body[tail_index]
            neighbors = self._ref_map.get_neighbors(end)
            for key, neighbor in neighbors.items():
                if neighbor in closedSet and neighbor not in snk_body:
                    end = neighbor[:]
            
            try:
                current = end[:]
                path_dict = dict()
                while current != start:
                    path_dict[current] = camefrom[current][:]
                    current = camefrom[current]
                
                
                v = end[:]
                u = path_dict[end[:]][:]
            except:
                tail_index -= 1
                continue
            
            while True:
                
                # determine the direction for path padding
                vec = tuple([v[0] - u[0], v[1] - u[1]])
                if self._direction_rep[vec] in 'AD':
                    # y axis
                    neighbors_of_v = self._ref_map.get_neighbors(v)
                    neighbors_of_u = self._ref_map.get_neighbors(u)
                    neighbors_of_v = [neighbors_of_v["W"], neighbors_of_v["S"]]
                    neighbors_of_u = [neighbors_of_u["W"], neighbors_of_u["S"]]
                else:
                    # x axis
                    neighbors_of_v = self._ref_map.get_neighbors(v)
                    neighbors_of_u = self._ref_map.get_neighbors(u)
                    neighbors_of_v = [neighbors_of_v["A"], neighbors_of_v["D"]]
                    neighbors_of_u = [neighbors_of_u["A"], neighbors_of_u["D"]]
                    
                for i, neighbor in enumerate(neighbors_of_v):
                    if neighbors_of_v[i] not in snk_body and neighbors_of_u[i] not in snk_body and neighbors_of_v[i] and neighbors_of_u[i] and neighbors_of_v[i] not in path_dict.keys() and neighbors_of_u[i] not in path_dict.keys():
                        path_dict[v[:]] = neighbors_of_v[i][:]
                        path_dict[neighbors_of_v[i][:]] = neighbors_of_u[i][:]
                        path_dict[neighbors_of_u[i][:]] = u[:]
                
                v = path_dict[v[:]][:]
                if v == start:
                    break
                u = path_dict[v[:]][:]
                
                
            return construct_path(path_dict, end)




if __name__ == "__main__":
    pass
    
