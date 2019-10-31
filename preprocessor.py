import nltk

class Preprocessor:
    def __init__(self, text):
        # tokenizes, tags, extracts entities from given string
        self.tokens = nltk.word_tokenize(text)
        self.tagged = nltk.pos_tag(self.tokens)
        self.entities = nltk.chunk.ne_chunk(self.tagged)
    
    @classmethod
    def fromTxtFile(filePath):
        # read the file and parse to string
        parsedText = ''
        return Preprocessor(parsedText)
    
preprocessor = Preprocessor("Donald Trump knows what the fuck is up. Except not in the White House because Biden is the king over there. CIA and such. Emily Dion?")
