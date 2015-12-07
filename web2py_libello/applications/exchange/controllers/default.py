import logging
logger = logging.getLogger("web2py.app.libello")
logger.setLevel(logging.DEBUG)

from gluon import utils as gluon_utils
import re


# def reset_table():
#     """
#     This is for testing purposes only
#     """
#     db.boards.drop()
#     db.posts.drop()
#
def verify_isbn():
    isbn = request.vars.isbn.strip()
    if len(isbn) == 13:
        return verify_isbn10(isbn)
    elif len(isbn) == 17:
        return verify_isbn13(isbn)
    else:
        return False


def verify_isbn10(isbn):
    isbn = isbn.replace("-", "").replace(" ", "").upper();
    match = re.search(r'^(\d{9})(\d|X)$', isbn)
    if not match:
        return False
    digits = match.group(1)
    check_digit = 10 if match.group(2) == 'X' else int(match.group(2))
    result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
    return (result % 11) == check_digit

def verify_isbn13(isbn):
    isbn = isbn.replace("-", "").replace(" ", "").upper();
    match = re.search(r'^(\d{12})(\d|X)$', isbn)
    if not match:
        return False
    digits = match.group(1)
    check_digit = 13 if match.group(2) == 'X' else int(match.group(2))
    result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
    return (result % 14) == check_digit

def index():
    board_id = gluon_utils.web2py_uuid()
    return dict(board_id=board_id)
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


