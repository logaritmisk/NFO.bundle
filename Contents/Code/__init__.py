import os, re

class movienfo(Agent.Movies):
	name='Movie NFO Agent'
	primary_provider=False
	languages = [Locale.Language.English]
	contributes_to = ['com.plexapp.agents.imdb']
	
	def search(self, results, media, lang):
		metadata=(media.primary_metadata)
		m = re.search('(tt[0-9]+)', media.guid)
		if m:
			id=m.groups(1)[0]
		score=100
		name="NFO_temp"
		results.Append(MetadataSearchResult(id=id,name=name,year=metadata.year,score=100))
		
	def update(self, metadata, media, lang):
		results=MediaContainer()
		(id, metadata)=self.parseNfo(metadata, media, lang)
		name=metadata.title
		year=metadata.year
		results.Append(MetadataSearchResult(id=id,name=name,year=year,score=100))
		
	def parseNfo(self, metadata, media, lang):
		Log("+++Parsing NFO+++")
		filename = media.items[0].parts[0].file.decode('utf-8')
		Log("Movie filename: " + filename)
		nfoFile=os.path.splitext(filename)[0]+".nfo"
		Log("NFO filename: " + nfoFile)
		nfoText=Core.storage.load(nfoFile)
		nfoXML=XML.ElementFromString(nfoText)
		#title
		try: metadata.title=nfoXML.xpath('./title')[0].text
		except: pass
		Log("Title: " + metadata.title)
		#tagline
		try: metadata.tagline=nfoXML.xpath('./tagline')[0].text
		except:pass
		Log("Disk: " + metadata.tagline)
		#summary
		try: metadata.summary=nfoXML.xpath('./plot')[0].text
		except:pass
		Log("Plot: " + metadata.summary)
		#studio
		try: metadata.studio=nfoXML.xpath('./studio')[0].text
		except:pass
		Log("Studio: " + metadata.studio)
		#year
		try: metadata.year=int(nfoXML.xpath('./year')[0].text)
		except:pass
		Log("Year:")
		Log(metadata.year)
		#rating
		try: metadata.rating=float(nfoXML.xpath('./rating')[0].text)
		except:pass
		Log("Rating:")
		Log(metadata.rating)
		#directors
		try:
			tempdirectors=nfoXML.xpath('./director')[0].text
			directors=tempdirectors.split("/")
		except:pass
		Log("Directors:")
		Log(directors)
		if directors != "":
			metadata.directors.clear()
			for r in directors:
				metadata.directors.add(r)
		#actors
		metadata.roles.clear()
		for actor in nfoXML.findall('./actor'):
			role=metadata.roles.new()
			try: role.role=actor.xpath("role")[0].text
			except: pass
			try: role.actor=actor.xpath("name")[0].text
			except: pass
		Log("Actors:")
		for r in metadata.roles:
			Log("Actor: " + r.actor + " | Role: " + r.role)
		Log("+++Done Parsing NFO+++")

		return id, metadata