from replit import db
db["key"] = {
  'haha': 'jaja'
}
del db['key']
for key in db.keys():
  print(db[key]['author'])

    
    

