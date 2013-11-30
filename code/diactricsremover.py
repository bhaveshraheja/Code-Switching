class diactricsremover():
	
        _dia = {}
	_diactricsmap = u'''\
        \u0031,1
        \u00e3,a
        \u00ea,e
        \u00ee,i
        \u00f1,n
        \u00f4,o
        \u00f4,o
        \u00fb,u
        \u0101,a
        \u0113,e
        \u0121,g
        \u012b,i
        \u014d,o
        \u015b,s
        \u016b,u
        \u0324, 
        \u0331, 
        \u1e0d,d
        \u1e25,h
        \u1e37,l
        \u1e39,l
        \u1e41,m
        \u1e45,n
        \u1e47,n
        \u1e5b,r
        \u1e5d,r
        \u1e5d,r
        \u1e63,s
        \u1e6d,t
        \u1e8f,y'''

	def createmap(self):
		# Converts the string-map into a dictionary
                diactrics = [row.strip().split(',') for row in self._diactricsmap.split('\n')]
		for char,trans in diactrics:
           		self._dia[char] = trans.encode('UTF-8')
        
	def remove(self, rawtext):
		# Converts text with diactrics into a non-diactrics format
		result = []
		for word in rawtext:
			if word in self._dia:
				result.append(self._dia[word])
			else:
				result.append(word)
		return ''.join(result)
         
