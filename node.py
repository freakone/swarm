
class Node:
  def __init__(self, id):
    self.id = id
    self.current_data = []
    self.filtered_history = []
    self.selected_points = []
    self.availible = False
    self.MAX_CURRENT = 20
    self.MAX_FILTERED = 500
    self.a_counter = 0

  def availibility(self, state):
    self.availible = state
    if not state:
      self.a_counter +=  1
    #   if self.a_counter > 10:
    #     self.current_data = []
    #     self.filtered_history = []


  def add_data(self, distance):
    self.current_data.append(distance)
    if len(self.current_data) > self.MAX_CURRENT:
        self.current_data.pop(0)

    filtered = sum(self.current_data) / len(self.current_data)
    self.filtered_history.append(filtered)
    if len(self.filtered_history) > self.MAX_FILTERED:
       self.filtered_history.pop(0)

    return filtered


  def probe(self):
    try:
      self.selected.insert(self.filtered_history[-1])
    except:
      print("# probe error")
