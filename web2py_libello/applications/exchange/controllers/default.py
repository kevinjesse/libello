import logging

logger = logging.getLogger("web2py.app.libello")
logger.setLevel(logging.DEBUG)

import isbnlib
import json


from gluon.tools import Mail
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'LibelloExchange@gmail.com'
mail.settings.login = 'LibelloExchange@gmail.com:libello7!'


def reset_table():
    """
    This is for testing purposes only
    """
    db.books.drop()

# def reset_book():
#     db(db.books.isbn ==  '9781458779878').delete()

@auth.requires_signature()
def info_isbn():
    isbn = request.vars.isbn
    data = isbnlib.meta(isbn, service='merge')
    cover = isbnlib.cover(isbn)
    desc = isbnlib.desc(isbn)
    return response.json(dict(cover=cover, meta=data, desc=desc))

def load_books():
    book_json = []
    isbns = []
    book_infos = db().select(db.books.title, db.books.authors, db.books.year_pub, db.books.isbn, db.books.publisher,
                       db.books.cover, db.books.descript, db.books.id)
    for temp_book in book_infos:
        user_infos = db(db.books.isbn == temp_book['isbn']).select(db.books.price, db.books.cond, db.books.user_id)
        sellers = []
        for temp_user in user_infos:
            sellers.append(dict(temp_user))
    #prevents multiple books from being added using the list of isbns
        if temp_book['isbn'] not in isbns:
             temp_book['sellers'] = sellers
             temp_book.pop('delete_record')
             temp_book.pop('update_record')
             book_json.append(dict(temp_book))
             isbns.append(temp_book['isbn'])
    # import pprint
    # logger.error(pprint.pprint(book_json))
    return response.json(book_json)

# def load_books():
#     books = {}
#     book_infos = db().select(db.books.title, db.books.authors, db.books.year_pub, db.books.isbn, db.books.publisher,
#                        db.books.cover, db.books.descript)
#     for temp_book in book_infos:
#         user_infos = db(db.books.isbn == temp_book['isbn']).select(db.books.price, db.books.cond, db.books.user_id)
#         sellers = {}
#         for temp_user in user_infos:
#             sellers[temp_user['user_id']] = dict(temp_user)
#
#         if temp_book['isbn'] not in books:
#             temp_book['sellers'] = sellers
#             book = {temp_book['isbn']: dict(temp_book)}
#             books.update(book)
#         else:
#             book = books[temp_book['isbn']]
#             book['sellers'].update(sellers)
#             books[temp_book['isbn']] = book
#     import pprint
#     logger.error(books)
#     return response.json(books)

@auth.requires_signature()
def info_search():
    search = str(request.vars.search)
    json_result = isbnlib.goom(search)
    data = json.dumps(json_result)
    search_return = []
    for book in json_result:
        temp = dict(book)
        temp['cover'] = isbnlib.cover(book['ISBN-13'])
        temp['desc'] = isbnlib.desc(book['ISBN-13'])
        temp['isbn'] = temp.pop('ISBN-13') #intercept and rename isbn to valid ractive
        #could include more information in search here
        search_return.append(temp)
    return response.json(search_return)

@auth.requires_signature()
def verify_isbn():
    isbn = request.vars.isbn.strip()
    return isbnlib.is_isbn10(isbn) or isbnlib.is_isbn13(isbn)


@auth.requires_signature()
def contact_seller():
    user_id = request.vars.user_id
    isbn = request.vars.isbn
    price = request.vars.price
    cond = request.vars.cond
    # do lookup of email from this
    book = db((db.books.isbn == isbn) & (db.books.user_id == user_id) &
              (db.books.price == price) & (db.books.cond == cond)).select(db.books.title, db.books.authors,
                                                                              db.books.isbn, db.books.year_pub, db.books.cond,
                                                                              db.books.price, limitby=(0, 1))

    user_info = db((db.auth_user.id == user_id)).select(db.auth_user.email, db.auth_user.first_name, db.auth_user.last_name)

    curr_user = db((db.auth_user.id == auth.user_id)).select(db.auth_user.email)

    # first = ""
    # last = ""
    for each in book:
        title = each['title']
        authors = ', '.join(each['authors'])
        isbn = each['isbn']
        year = each['year_pub']
        cond = each['cond']
        price = each['price']
        if cond == 4:
            cond = "Like New"
        elif cond == 3:
            cond = "Very Good"
        elif cond == 2:
            cond = "Good"
        elif cond == 1:
            cond = "Acceptable"


    for each in user_info:
        email = each['email']
        first = each['first_name']
        last = each['last_name']

    for each in curr_user:
        customer = each['email']

    mail.send(to=email,
          subject='Libello Book Exchange: ' + title,
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to=email,
          message="Hello " + first + " " + last + ",\n\n" + customer + ' is interested in: "' + title + "("+ year + ") by " +
     authors + '" for $' + price + " in " + cond + " condition.\n\n Thanks,\n The Libello Team")
    return "ok"


def index():
    return dict(user_id=auth.user_id)

@auth.requires_signature()
def book_add():
    title = request.vars['meta[Title]']
    authors = request.vars['meta[Authors]']
    year = request.vars['meta[Year]']
    isbn = request.vars['meta[ISBN-13]']
    pub = request.vars['meta[Publisher]']
    price = request.vars['price']
    cond = request.vars['cond']
    cover = ''.join(request.vars['cover[]'])
    desc = request.vars['desc']
    db.books.update_or_insert(((db.books.isbn == isbn) & (db.books.user_id == auth.user_id)),title=title,
                              authors=authors, year_pub=year, isbn=isbn, publisher=pub, price=price, cond=cond,
                              cover=cover, descript=desc, user_id=auth.user_id)
    # db.books.insert(title=title, authors=authors, year_pub=year, isbn=isbn, publisher=pub, price=price, cond=cond,
    #                            cover=cover, descript=desc, user_id=auth.user_id)
    return "ok"

# def book_update():
#     ident = request.vars['id']
#     title = request.vars['meta[Title]']
#     authors = request.vars['meta[Authors]']
#     year = request.vars['meta[Year]']
#     isbn = request.vars['meta[ISBN-13]']
#     pub = request.vars['meta[Publisher]']
#     price = request.vars['price']
#     cond = request.vars['cond']
#     cover = ''.join(request.vars['cover[]'])
#     desc = request.vars['desc']
#     db.books.update_or_insert((db.books.id == ident),title=title,
#                               authors=authors, year_pub=year, isbn=isbn, publisher=pub, price=price, cond=cond,
#                               cover=cover, descript=desc, user_id=auth.user_id)
#     # db.books.insert(title=title, authors=authors, year_pub=year, isbn=isbn, publisher=pub, price=price, cond=cond,
#     #                            cover=cover, descript=desc, user_id=auth.user_id)
#     return "ok"

@auth.requires_signature()
def book_delete():
    book_id = request.vars.id

    db(db.books.id == book_id).delete()
    return "ok"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


