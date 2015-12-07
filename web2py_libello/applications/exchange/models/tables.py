#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('books',
                Field('title', 'text'),
                Field('authors', 'list:string'),
                Field('year_pub', 'text'),
                Field('isbn', 'text'),
                Field('publisher', 'text'),
                Field('price', 'text'),
                Field('cond', 'integer'),
                Field('cover', 'text'),
                Field('descript', 'text'),
                Field('user_id', db.auth_user, default=auth.user_id),
)

