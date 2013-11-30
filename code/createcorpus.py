import pickle
import crawl
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from collections import Counter
import re
import nltk
import iso15919
import diactricsremover
import time

class createcorpus():
	
    _visitedlinks = set()
    _DEVANAGARI_UNICODE_START = u'\u0090'
    _DEVANAGARI_UNICODE_END = u'\u097F'
    VISITED_LINKS_FILE='visited_links'
	
    def _init_(self,linksfile='visited_links'):
        # Default location of files. Can be overriden 
    	#_WORD_COUNT_FILE='wordcount'
        self.VISITED_LINKS_FILE = linksfile 
	try:
	    self._visitedlinks = pickle.load(open(_VISITED_LINKS_FILE,"rb"))
	except EOFError:
	    self._visitedlinks = set() # Initialize to an empty set 
	    
	
    def _finalize(self):
	# Save the links
        pickle.dump(self._visitedlinks,open(self.VISITED_LINKS_FILE,'wb'))
        print 'Links saved to file'
        # Save the wordcount
        #pickle.dump(self._wordcount, open(self._WORD_COUNT_FILE,'wb'))
        #print 'Word count saved to file
    
    def _merge(self, a, b):
        '''Merges two dictionaries
           Adds the value of the common-keys'''
        for key,value in a.items():
            if key in b:
                a[key] += b[key]
        b.update(a)
        return b

    def _getlinks(self,starturl):
        crawler = crawl.crawler()
        links = crawler.crawl(starturl,200)
        return links

    def countwords(self,starturl,crawl=False):
        if crawl:
            links = self._getlinks(starturl)
        else:
            links = [starturl]
        for link in links:
            if not link in self._visitedlinks:
                print 'Link is ',link
                # Update the set of visited links
                self._visitedlinks.update(link)

                # Fetch the page
                try:
                    response = requests.get(link)
                except:
                    print 'Error encountered while fetching link ',link
                    continue
                soup = BeautifulSoup(response.text, "html5lib")
                pagetext = soup.get_text() # All the text of the page in Unicode

                # Tokenize the words
                words = nltk.word_tokenize(pagetext)

                # Filter the words out based on containing Devnagari content
                # If the word begins with a Devnagari letter, it can be generalized to be a devnagari word
                filtered_content = filter(lambda x: x[0] >= self._DEVANAGARI_UNICODE_START and x[0] <= self._DEVANAGARI_UNICODE_END,words)
                
                # Convert list to a string of words
                filtered_content = ' '.join(filtered_content)

                # Replaace the symbols like '/' to space
                filtered_content.replace('/',' ')
                
                # Transliterate the Devnagari text
                romanised_unicode = iso15919.transliterate(filtered_content)

                
                # Remove diatrics
                dr = diactricsremover.diactricsremover()
                # Initialize the list of transformations
                dr.createmap()
                romanised_unicode = dr.remove(romanised_unicode)
                
                # Compute Word Count
                # Convert string to list of words
                romanised = nltk.sent_tokenize(romanised_unicode)
                #Count = Counter(romanised)

                # Merge the two dictionaries to the single dictionary
                #self._wordcount = self._merge(self._wordcount, Count)
                
                # Write the file 
                filename = '../data/marathi/'+time.strftime("%Y%m%d-%H-%M")
                f = open(filename, 'a')
                f.write(' '.join(romanised).encode('UTF-16'))
                print "Written text to file-",filename
                f.close()

        # End the counting of words, calling finalize method
        self._finalize()



