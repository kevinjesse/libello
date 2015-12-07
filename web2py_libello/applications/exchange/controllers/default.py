import logging

logger = logging.getLogger("web2py.app.libello")
logger.setLevel(logging.DEBUG)

import isbnlib
import json



def reset_table():
    """
    This is for testing purposes only
    """
    db.books.drop()


def info_isbn():
    isbn = request.vars.isbn
    data = isbnlib.meta(isbn, service='merge')
    cover = isbnlib.cover(isbn)
    desc = isbnlib.desc(isbn)
    return response.json(dict(cover=cover, meta=data, desc=desc))


def load_books():
    rows = db(db.books.id >= 0).select()
    d = {r.id: {'title': r.title, 'authors': r.authors, 'year': r.year_pub, 'isbn': r.isbn,
                'pub': r.publisher, 'price': r.price, 'cond': r.cond, 'cover': r.cover,
                'desc': r.descript, 'user_id': r.user_id}
         for r in rows}
    return dict(books=d)


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


def verify_isbn():
    isbn = request.vars.isbn.strip()
    return isbnlib.is_isbn10(isbn) or isbnlib.is_isbn13(isbn)


def index():
    return load_books()


def book_add():
    title = request.vars['meta[Title]']
    authors = request.vars['meta[Authors][]']
    year = request.vars['meta[Year]']
    isbn = request.vars['meta[ISBN-13]']
    pub = request.vars['meta[Publisher]']
    price = request.vars['price']
    cond = request.vars['cond']
    cover = ''.join(request.vars['cover[]'])
    desc = request.vars['desc']
    db.books.insert(title=title, authors=authors,year_pub=year, isbn=isbn, publisher=pub,
                    price=price, cond=cond, cover=cover, descript=desc, user_id=auth.user_id)
    return



#
# def load_boards():
#     """Loads all boards for the user."""
#     rows = db(db.boards.id >= 0).select()
#     d = {r.board_id: {'board_name': r.board_name, 'author': r.author}
#          for r in rows}
#     return response.json(dict(board_dict=d))
#
# @auth.requires_signature()
# def add_board():
#     db.boards.update_or_insert((db.boards.board_id == request.vars.board_id),
#             board_id=request.vars.board_id,
#             board_name=request.vars.board_name,
#             author=auth.user_id)
#     return "ok"
#
# @auth.requires_signature()
# def delete_board():
#     db(db.boards.board_id == request.vars.board_id).delete()
#     return "ok"
#
# @auth.requires_signature()
# def edit_board():
#     db(db.boards.board_id == request.vars.board_id).update(board_name=request.vars.board_name)
#     return "ok"
#
# def posts():
#     board_id = request.args(0)
#     post_id = gluon_utils.web2py_uuid()
#     return dict(board_id=board_id, post_id=post_id)
#
#
# def load_posts():
#     rows = db(db.posts.board_id == request.vars.board_id).select()
#     d = {r.post_id: {'post_content': r.post_content, 'post_name': r.post_name, 'board_id': r.board_id, 'author': r.author}
#          for r in rows}
#     return response.json(dict(post_dict=d))
#
#
# @auth.requires_signature()
# def add_post():
#     db.posts.update_or_insert((db.posts.post_id == request.vars.post_id),
#             post_id=request.vars.post_id,
#             post_name=request.vars.post_name,
#             post_content=request.vars.post_content,
#             board_id=request.vars.board_id,
#             author=auth.user_id)
#     return "ok"
#
# @auth.requires_signature()
# def delete_post():
#     db(db.posts.post_id == request.vars.post_id).delete()
#     return "ok"
#
# @auth.requires_signature()
# def edit_post_name():
#     db(db.posts.post_id == request.vars.post_id).update(post_name=request.vars.post_name)
#     return "ok"
#
# @auth.requires_signature()
# def edit_post_content():
#     db(db.posts.post_id == request.vars.post_id).update(post_content=request.vars.post_content)
#     return "ok"


#
# @auth.requires_signature()
# def delete_posts():
#     idlist = request.vars['list[]']
#     if type(idlist) is list:
#         for identifier in idlist :
#             db(db.posts.post_id == identifier).delete()
#     elif type(idlist) is str:
#         db(db.posts.post_id == idlist).delete()
#     return "ok"
#
# @auth.requires_signature()
# def edit_posts():
#     db(db.posts.post_id == request.vars.post_id).update(post_content=request.vars.post_content)
#     return "ok"
#
# @auth.requires_signature()
# def edit_postsd():
#     db(db.posts.post_id == request.vars.post_id).update(post_description=request.vars.post_description)
#     return "ok"
#
#
#







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


