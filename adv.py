from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def traversal(player, world, graph):
    
    # Create a path list (p)
    p = []    
    
    # Create a room stack (s) and add the starting room
    s = []
    s.append(player.current_room.id)
    
    # Create a set for visited rooms (v) - set is both ordered and unique values
    v = set()    
        
    # While all of the rooms (len(v)) have not been visited
    while len(v) != len(world.rooms):
        # Get the current room from the stack (s)
        cur = s[-1]
        # Add the current room to visited (v)
        v.add(cur)
        
        # Handle the connecting rooms
        # Create a queue for a BFT (q)
        q = []        
        
        # Get the connecting rooms (cr) from the graph
        # i.e. {'n': 361, 'e': 321, 'w': 386}
        cr = graph[cur][1] 
        
        # Check for connected, unvisited rooms:
        # For any connected rooms 
        for x, y in cr.items():
            # if room (y) is not in visited (v) add it to the queue (q)
            if y not in v:
                q.append(y)
        
        # Get the next room:
        # If there are rooms in the queue (q), get the next room from the queue (q)       
        if len(q):
            # Dequeue the next room (q)
            nxt = q[0]
            # Add it to the stack (s)
            s.append(nxt)
        else:
            # Queue (q) is empty pop the current room from the stack (s) 
            s.pop()
            # Get next room (nxt) from the stack (s)
            nxt = s[-1]

        # Add the cardinal directions to the path (p)
        # For any connected rooms 
        for x, y in cr.items():
            # If room is next room (nxt) 
            if y == nxt:
                # Add the cardinal direction to the path (p)
                p.append(x)
    
    # Return the path (p) of cardinal directions   
    return p


traversal_path = traversal(player, world, room_graph)    


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
