import web
import os

urls = (
    '/',       'Index',
	'/browse', 'List',
	'/browse/(\d+)', 'Display',
    '/admin', 'Update',
	'/contact', 'Contact'
)

render = web.template.render('templates/')

class Index:
    def GET(self):
		return render.index()

class List:
	def GET(self):
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
						break
		return render.list1(filelist, idlist, n)

class Display:
	def GET(self, id):
		
		db = web.database(dbn='postgres', user='web', pw='1220lx', db='PicInfo')
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

class Update:
	def GET(self):
		return 'admin'

class Contact:
	def GET(self):
		return render.contact()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
