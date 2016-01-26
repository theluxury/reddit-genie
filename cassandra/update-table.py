import sys
from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table

inputFileName = sys.argv[1]

# User model
class Users(Model):
  user_id = columns.BigInt(primary_key=True)
  follows = columns.Set(columns.BigInt)
  def __repr__(self):
    return str(self.user_id) + ': ' + ', '.join(str(i) for i in self.follows) 

connection.setup(['127.0.0.1'], "user_graph")
sync_table(Users)
# gotta iterate over some giant ass file...
with open(inputFileName, 'r') as file:
  for line in file.readlines():
    print line
# Users.create(user_id=1, follows={2, 3})
#q = Users.get(user_id=1)
# print q
