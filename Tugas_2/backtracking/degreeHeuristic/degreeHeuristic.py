import global_data as gd

#menggunakan degree heuristic untuk memilih data yg belum diassign
def select_unassigned_variable_heuristic_degree():
    unassigned = [v for v in gd.variables if v not in gd.assignment]
    print("Belum diassign: ", unassigned)
    
    if not unassigned:
        return None
    
    constraints_graph = {
        "Ani": ["Budi"],
        "Budi": ["Ani"],
        "Citra": ["Dedi"],
        "Dedi": ["Citra"],
        "Eka": []
    }
    
    degree_var = None
    max_degree = -1
    
    # intinya mengecek seluruh variabel yang belum diassign memiliki berapa constraints
    for var in unassigned:
        degree = 0
        for constrained_var in constraints_graph[var]:
            if constrained_var in unassigned:
                degree += 1
        
        print(f"{var}: degree = {degree}")
        
        if degree > max_degree:
            max_degree = degree
            degree_var = var
    
    print(f"→ Selected {degree_var} (Degree with {max_degree} constraints)")
    return degree_var


def is_consistent(var, value):
    if var == "Ani" and "Budi" in gd.assignment:
        if gd.assignment["Budi"] == value:
            return False
    if var == "Budi" and "Ani" in gd.assignment:
        if gd.assignment["Ani"] == value:
            return False
    
    if var == "Citra" and "Dedi" in gd.assignment:
        if gd.assignment["Dedi"] != value:
            return False
    if var == "Dedi" and "Citra" in gd.assignment:
        if gd.assignment["Citra"] != value:
            return False
    
    return True

def is_complete_valid():
    if len(gd.assignment) != len(gd.variables):
        return False
    
    kelas = [[], []]
    for student, class_num in gd.assignment.items():
        kelas[class_num].append(student)
    
    for i in range(2):
        if "Eka" in kelas[i] and len(kelas[i]) == 1:
            return False
    
    for i in range(2):
        if len(kelas[i]) > 0 and len(kelas[i]) < 2:
            return False
    
    return True

def get_legal_values(var):
    legal = []
    for value in gd.domains[var]:
        if is_consistent(var, value):
            legal.append(value)
    return legal

def order_domain_values(var):
    legal_values = get_legal_values(var)
    
    if var == "Citra" and "Dedi" in gd.assignment:
        return [gd.assignment["Dedi"]]
    if var == "Dedi" and "Citra" in gd.assignment:
        return [gd.assignment["Citra"]]
    
    return legal_values

def backtrack():
    global backtrack_count, steps
    
    gd.steps += 1
    
    #cek apakah variabel sudah diassign semua
    if len(gd.assignment) == len(gd.variables):
        if is_complete_valid():
            return True
        else:
            return False
    
    print(f"\nStep {gd.steps}:")
    print(f"Current assignment: {gd.assignment}")
    var = select_unassigned_variable_heuristic_degree()
    
    #cek jika var sudah habis
    if var is None:
        return is_complete_valid()
    
    for value in order_domain_values(var):
        print(f"Trying {var} = Class {value}")
        
        gd.assignment[var] = value
        result = backtrack()
        
        if result:
            return True
        
        print(f"\n!!!!Backtracking from {var} = Class {value}")
        gd.backtrack_count += 1
        del gd.assignment[var]
    
    return False

def solve():
    result = backtrack()
    
    if result:
        print("\nSolusin = \n")
        
        kelas = [[], []]
        for student, class_num in gd.assignment.items():
            kelas[class_num].append(student)
        
        print(f"Class 0: {kelas[0]} ({len(kelas[0])} members)")
        print(f"Class 1: {kelas[1]} ({len(kelas[1])} members)")
        
    else:
        print("Tidak ada solusi!")
        print("=" * 60)
    
    return result

def Degree_Heuristic():
    gd.assignment = {}
    gd.backtrack_count = 0
    gd.steps = 0
    
    solve()
