import web
import json
import os

urls = (
    '/',       'Index',
	'/browse', 'List',
	'/browse/(.+)', 'Display',
    '/admin', 'Admin',
	'/login', 'Login',
	'/contact', 'Contact'
)

render = web.template.render('templates/')
app = web.application(urls, locals())
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session
db = web.database(dbn='postgres', user='web', pw='1220lx', db='PicInfo')

class Index:
    def GET(self):
		return render.index()

class List:
	def GET(self):
		titlelist = []
		path = 'static/data/'
		filelist = []
		idlist = []
		n = 0
		if os.path.isdir(path):
			for s in os.listdir(path):
				if s == '.DS_Store':
					continue
				newpath = path + s + '/'
				if os.path.isdir(newpath):
					for ss in os.listdir(newpath):
						if ss == '.DS_Store':
							continue
						now = '../' + newpath + ss
						n = n + 1
						filelist.append(now)
						idlist.append('browse/'+ s)
						str = 'select * from info where id = \'' + s + '\''
						now = db.query(str)
						title = ''
						for k in now:
							title = k.title
							break
						titlelist.append(title)
						break
		return render.list(filelist, idlist, titlelist, n)

class Display:
	def GET(self, id):
		print id
		str = 'select * from info where id = \'' + id + '\''
		now = db.query(str)
		title = ''
		dis = ''
		for k in now:
			title = k.title
			dis = k.detail
			break
		
		path = 'static/data/' + id + '/'
		filelist = []
		n = 0
		if os.path.isdir(path):
			for s in os.listdir(path):
				if s == '.DS_Store':
					continue
				newpath='../'+ path + s
				filelist.append(newpath)
				n = n + 1
		return render.display(filelist, n, title, dis)

class Admin:
	def GET(self):
		if session.count == 1:
			return render.admin('')
		else:
			raise web.seeother('/login')

	def POST(self):
		tit = web.input().title
		dis = web.input().dis
		date = web.input().date
		if (date == ''):
			return render.admin('Failed! Date should not be null.')
		path = 'static/data/' + date + '/'
		if os.path.isdir(path):
			return render.admin('Failed! Date already existed.')
		str = 'select * from info where id = \'' + date + '\''
		now = db.query(str)
		if len(now) > 0:
			return render.admin('Failed! Date already existed.')
		files = web.webapi.rawinput().get( "myfile" )
		if not isinstance(files, list):
			files = [files]
		for f in files:
			filename = f.filename
			name,ext = os.path.splitext(filename)
			ext = ext.lower()
			safeImageExts =('.png','.jpeg','.jpg','.gif')
			if not ext in safeImageExts:
				return render.admin('Failed! Files invalid.')
		print path
		if not os.path.exists(path):
			os.makedirs(path)
		for f in files:
			fout = open(path +'/'+ f.filename,'w')
			fout.write(f.file.read())
			fout.close()
		db.insert('info', id=date, title=tit, detail=dis)
		return render.admin('Succeed!')

class Login:
	def GET(self):
		return render.login()

	def POST(self):
		user = web.input().user
		passwd = web.input().passwd
		str = 'select * from users where id = \'' + user + '\''
		now = db.query(str)
		for k in now:
			if passwd == k.password:
				session.count = 1
				raise web.seeother('/admin')
				break
		session.count = 0
		raise web.seeother('/login')

class Contact:
	def GET(self):
		return render.contact()


if __name__ == "__main__":
    app.run()
