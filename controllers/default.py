# -*- coding: utf-8 -*- 

def index():
    return dict()


def user():
    return dict(form=auth())
    
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
    

#get database itens
def export_xml(rows,fields):
    users=[]
    for row in rows: users.append(TAG.user(*[TAG[f](row[f]) for f in fields]))
    return TAG.users(*users).xml()

#xml generate xml file for googlemaps script
def lista():
    response.headers['Content-Type']='application/xml'
    return export_xml(db(db.auth_user.id>0).select(), ['lat','lgt','first_name','country'])
